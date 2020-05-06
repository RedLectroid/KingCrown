#!/usr/bin/env python3

import subprocess
import argparse
import time
import os
import base64
import coreUtils
import fileinput

#Global scope
starString = "****************************************************************************************************************************"

def ServerInstall():
	
	done = False
	looper = False
	port = ""
	domain = ""
	path = ""
	email = ""
	
	while looper != True:

		os.system('clear')
		print("****************************************************************")
		print("*                                                              *")
		print("*                       Server Setup                           *")
		print("*                                                              *")
		print("*                                                              *")
		print("* Require options are:                                         *")
		print("*                                                              *")
		print("* 1. Domain Name                                               *")
		print("* 2. Install Path for KingPhisher                              *")
		print("* 3. KingPhisher Web Server Port                               *")
		print("* 4. Email to use for certbot (doesn't need to be real)        *")
		print("*                                                              *")
		print("*                                                              *")
		print("****************************************************************")
		print("\n")

		menu = {}
		menu['0'] = " Info"
		menu['1'] = " Set Domain Name"
		menu['2'] = " Install Path for KingPhisher"
		menu['3'] = " Set KingPhisher Web Server Port"
		menu['4'] = " Set Email for Certbot"
		menu['5'] = " Begin KingPhisher Server installation"
		menu['42'] = "Return to menu"
		menu['99'] = "Exit"

		options = menu.keys()
		sorted(options)
		for entry in options:
			print (entry, menu[entry])

		print("\n\n")
		if domain != "":
			print("Domain set to ->  " + domain)
		if path != "":
			print("KingPhisher install path set to ->  " + path)
		if port != "":
			print("KingPhisher Web Server port set to ->  " + port)
		if email != "":
			print("Email for certbot set to ->  " + email)
		if domain != "" and path != "" and port != "" and email != "":
			print("\n***All options are set and you are ready to install***")

		selection = input("\nPlease Select: ")

		if selection == '1':
			domain = input("Please enter the domain name to be used:  ")
		elif selection == '2':
			path = input("Please enter the full path for the KingPhisher installation (including /KingPhisher):  ")
		elif selection == '3':
			port = input("Please enter the port for the KingPhisher Web Server:  ")
		elif selection == '4':
			email = input("Please enter the email to be used for certbot (Does not have to be real):  ")
		elif selection == '5':
			if done == False:
				print("\nYou have not set all the options")
				input("Press Enter to return to the menu and set all the options")
			else:
				looper = True
		elif selection == '42':
			os.system('clear')
			break
		elif selection == '99':
			exit()
		elif selection == '0':
			ServerInfo()
		else:
			ErrorMessage()

		if domain != "" and path != "" and port != "" and email != "":
			done = True

		if done == True and looper == True:
			print("\n***Please confirm you have port 80 open on the firewall for certbot to setup the SSL certificate***\n")
			print("***Please confirm you have updated the DNS record for " + domain + " to point to the IP address of this server***\n")
			input("Press Enter to begin the installation")
			coreUtils.DownloadKP(path)
			time.sleep(10)
			coreUtils.installKP("server",path)
			dkimSetup(path,domain)
			certBotSetup(domain,email)
			server_ConfigSetup(domain,path,port)
			postfixSetup(domain)
			setupGenericFile(domain)
			mainCFsetup(domain)
			subprocess.call(["service","king-phisher","start"])

			print(starString)
			print(starString)
			print(starString)
			print("****************************************************************************************************************************")
			print("*****************************************KingPhisher install and setup complete!!!******************************************")
			print("**************************openDKIM files default.private and default.txt located in /etc/opendkim/keys**********************")
			print("**************************************Please press enter to return to the main menu*****************************************")
			print("****************************************************************************************************************************")
			print(starString)
			print(starString)
			print(starString)
			print("\n")
			print("Contents of default.txt for DNS entry:")
			printDKIM(domain)
			input()


def printDKIM(domain):
	in_file = open("/etc/opendkim/keys/"+str(domain)+"/default.txt", "r") 
	buf = in_file.readlines()
	buf = str(buf)
	begin, middle = buf.split('(')
	middle = str(middle)
	middle2,end = middle.split(')')
	output = middle2.replace(" ","")
	output = output.replace("\\t","")
	output = output.replace("\\n","")
	output = output.replace("\'","")
	output = output.replace("\"","")
	output = output.replace(",","")
	print(str(output))

def dkimSetup(path,domain):

	print(starString + "\n\n" + "Downloading openDKIM \n\n")
	subprocess.call(["apt-get","install","opendkim","opendkim-tools","-y"])
	time.sleep(10)
	print(starString + "\n\n" + "Running openDKIM \n\n")
	
	if not (os.path.isdir("/etc/opendkim/")):
		os.makedirs("/etc/opendkim/")
		os.makedirs("/etc/opendkim/keys")
		
	subprocess.call(["chown","-R","opendkim:opendkim","/etc/opendkim/"])
	subprocess.call(["chmod","go-rw","/etc/opendkim/keys"])

	file = "/etc/opendkim/signing.table"
	with open(file,'w') as filetowrite:
		filetowrite.write("*@" + str(domain) + "\tdefault._domainkey." + str(domain))


	file = "/etc/opendkim/key.table"
	with open(file,'w') as filetowrite:
		filetowrite.write("default._domainkey." + str(domain) + "\t" + str(domain) + ":default:/etc/opendkim/keys/" + str(domain) + "/default.private")

	file = "/etc/opendkim/trusted.hosts"
	with open(file,'w') as filetowrite:
		filetowrite.write("127.0.0.1\nlocalhost\n*." + str(domain))

	os.makedirs("/etc/opendkim/keys/" + str(domain))

	keypath = "/etc/opendkim/keys/" + str(domain)

	subprocess.call(["opendkim-genkey","-b","2048","-d",str(domain),"-D",keypath,"-s","default","-v"])
	time.sleep(10)
	
	print(starString + "\n\n" + "Writing /etc/opendkim.conf \n\n")
	file='/etc/opendkim.conf'

	with open(file, "r") as in_file:
		buf = in_file.readlines()

	os.rename(file, file + "BAK")

	with open(file,'w') as out_file:
		for line in buf:
			if line.startswith("Domain                  "):
				line = "Domain                  " + domain
			if line.startswith("#Canonicalization	simple"):
				line = "Canonicalization   relaxed/simple"
			if line.startswith("#SubDomains		no"):
				line = line + "AutoRestart     	yes\n"
				line = line + "AutoRestartRate     	10/1M\n"
				line = line + "Background      	yes\n"
				line = line + "DNSTimeout      	5\n"
				line = line + "SignatureAlgorithm  	rsa-sha256\n"

			out_file.write(line)

	privateFilePath = str(os.getcwd()) + "/" + str(domain) + "default.private"
	defaultFilePath = str(os.getcwd()) + "/" + str(domain) + "default.txt"

	subprocess.call(["chown","opendkim:opendkim",keypath + "/default.private"])
	subprocess.call(["chown","opendkim:opendkim",keypath + "/default.txt"])


def certBotSetup(domain,email):
	print(starString + "\n\n" + "Stopping KingPhisher service \n\n")
	subprocess.call(["service","king-phisher","stop"])
	time.sleep(5)
	print(starString + "\n\n" + "Installing Certbot \n\n")
	subprocess.call(["apt-get","install","certbot","-y"])
	time.sleep(5)
	print(starString + "\n\n" + "Running certbot \n\n")
	time.sleep(2)
	subprocess.call(["certbot","certonly","--standalone","--preferred-challenges","http","-d",str(domain),"-n","--agree-tos","--email",str(email)])
	time.sleep(5)

def server_ConfigSetup(domain,path,port):
	print(starString + "\n\n" + "Writing " + path + "/server_config.yml \n\n")
	#KPconfigFile=path+"/server_config.yml"
	

	with open(path+"/server_config.yml", "r") as in_file:
		buf = in_file.readlines()

	os.rename(path+"/server_config.yml", path+"/server_config.ymlBAK")

	with open(path+"/server_config.yml", "w") as out_file:
		for line in buf:
			if line.startswith("   # - host"):
				line = "    - host: 0.0.0.0\n"
			if line.startswith("   #   port: 80"):
				line = "      port: 80\n"
			elif line.startswith("    #  port: 443"):
				line = "      port: " + str(port) + "\n"
			elif line.startswith("    #  ssl:"):
				line = "      ssl: true"
			elif line.startswith("  #    ssl_cert: "):
				line = "  ssl_cert: /etc/letsencrypt/live/" + str(domain) + "/fullchain.pem\n"
			elif line.startswith("  #    ssl_key: "):
				line ="  ssl_key: /etc/letsencrypt/live/" + str(domain) + "/privkey.pem\n"
			out_file.write(line)
	

def setupGenericFile(domain):
	postfixCommand = "postfix"
	print(starString + "\n\n" + "Installing postfix and writing generic file \n\n")
	subprocess.call(["apt-get","install","certbot","-y"])
	time.sleep(5)
	file="/etc/postfix/generic"
	with open(file,'w+') as filetowrite:
		line = "root mailbox@" + domain + "\n"
		line = line + "sysadmin mailbox@" + domain + "\n"
		line = line + "redteam mailbox@" + domain + "\n"
		filetowrite.write(line)
	subprocess.call(["postfix","/etc/postfix/generic"])

def mainCFsetup(domain):
	print(starString + "\n\n" + "Writing /etc/postfix/main.cf \n\n")
	file="/etc/postfix/main.cf"

	with open(file,'r') as in_file:
		buf = in_file.readlines()
	
	os.rename(file,file + "BAK")

	with open(file,'w') as out_file:
		for line in buf:
			if line.startswith("myhostname = mail."):
				line = "myhostname = mail." + domain
			elif line.startswith("mydestination = $myhostname, mail."):
				line = "mydestination = $myhostname, mail." + domain + ", localhost.owxelmbkelkexgpsfis1xlhhpf.gx.internal.cloudapp.net, localhost"
			out_file.write(line)
		line = "\n# Milter configuration\n"
		line = line + "milter_default_action = accept\n"
		line = line + "milter_protocol = 6\n"
		line = line + "smtpd_milters = local:opendkim/opendkim.sock\n"
		line = line + "non_smtpd_milters = $smtpd_milters\n"
		out_file.write(line)
	out_file.close()

	subprocess.call(["systemctl","restart","opendkim","postfix"])

def postfixSetup(domain):
	print(starString + "\n\n" + "Installing Postfix \n\n")
	subprocess.call("echo \"postfix	postfix/mailname string " + domain + "\" | debconf-set-selections",shell=True)
	subprocess.call("echo \"postfix postfix/main_mailer_type string 'Internet Site'\" | debconf-set-selections", shell=True)
	time.sleep(3)
	subprocess.call(["apt-get","-y","install","postfix"])
	time.sleep(3)

	file = "/etc/postfix/master.cf"

	with open(file,"a") as in_file:
		in_file.write("policyd-spf  unix  -       n       n       -       0       spawn\n")
		in_file.write("    user=policyd-spf argv=/usr/bin/policyd-spf\n")
	in_file.close()



