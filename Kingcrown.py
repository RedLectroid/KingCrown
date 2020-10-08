#!/usr/bin/env python3

import subprocess
import argparse
import time
import os
import base64
import coreUtils
import serverUtils
import domainUtils


#Global Scope
starString = "****************************************************************************************************************************"


def checkPermissions():
	if os.geteuid() != 0:
		exit("\nYou need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.\n")

def mainMenu():

	checkPermissions()

	port = ""
	domain = ""
	path = ""

	menu = {}
	menu['0']="Tool Information"
	menu['1']="Install and configure KingPhisher server"
	menu['2']="Update existing KingPhisher Server with new domain"
	menu['99']="Exit"

	while True:
		coreUtils.bannerMain()
		options=menu.keys()
		sorted(options)
		for entry in options: 
			print (entry, menu[entry])

		selection=input("\nPlease Select: ") 
		if selection =='1': 
			serverUtils.ServerInstall(domain,path,port)
		elif selection == '2':
			domainUtils.domainChange()
		elif selection == '0':
			coreUtils.generalInfo()
		elif selection == '99': 
			exit()
		else: 
			coreUtils.ErrorMessage()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
parser.add_argument("-d","--domain", help="The domain to assign an SSL cert to with certbot")
parser.add_argument("-i","--path", help="The path to download and install KingPhisher to")
parser.add_argument("-p","--port", help="Webserver port for KingPhisher")
args = parser.parse_args()

domain = args.domain
path = args.path
port = args.port

if args.domain != None:
	print("Silent install")
	serverUtils.ServerInstall(domain,path,port)
else:
	mainMenu()
