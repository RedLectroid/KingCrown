#!/usr/bin/env python3

import subprocess
import argparse
import time
import os
import base64
import serverUtils

#Global scope
starString = "****************************************************************************************************************************"

def checkPermissions():
	if os.geteuid() != 0:
		exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

def ErrorMessage():
	input("\n\n***That is not a valid option! Press Enter to acknowledge your mistake***\n\n")


def bannerMain():

	os.system('clear')
	banner = "**********************************************************\n"
	banner +="*    _  ___              _____                           *\n"
	banner +="*   | |/ (_)            / ____|                          *\n"
	banner +="*   | ' / _ _ __   __ _| |     _ __ _____      ___ __    *\n"
	banner +="*   |  < | | '_ \\ / _` | |    | '__/ _ \\ \\ /\\ / / '_ \\   *\n"
	banner +="*   | . \\| | | | | (_| | |____| | | (_) \\ V  V /| | | |  *\n"
	banner +="*   |_|\\_\\_|_| |_|\\__, |\\_____|_|  \\___/ \\_/\\_/ |_| |_|  *\n"
	banner +="*                  __/ |                                 *\n"
	banner +="*                  |___/                                 *\n"
	banner +="*                                                        *\n"
	banner +="**********************************************************\n"
	print(banner)

def installKP(installOption,path):
	if installOption == "client":
		print(starString)
		print("Installing the client\n\n")
		subprocess.call([path+"/tools/install.sh","-y","--skip-server"])
		print(starString)
	elif installOption == "server":
		time.sleep(10)
		print(starString)
		print("Installing the server\n\n")
		print(starString)
		subprocess.call([path+"/tools/install.sh","-y","--skip-client"])

def DownloadKP(path):
	if not os.path.exists(path):
		os.makedirs(path)
		
	print(starString + "\n\n" + "Downloading KingPhisher to " + path + "\n\n")
	subprocess.call(["git","clone","https://github.com/securestate/king-phisher.git",path])

def generalInfo():
	print("\n\nThis is General Info reporting\n\n")
	input("\nPress Enter to return\n")
