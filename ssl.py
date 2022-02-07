#!/usr/bin/env python3
import subprocess
from os import system, sys, path, listdir, makedirs
import getpass
import string
import random
# from adddomain import domain
# import numpy as np

def manage_ssl():
    print("Please enter your choice:\n1. Install Certbot\t2. Install SSL Let's Encrypt\t3. Back")
    choice = input()
    sys.stdout.write("\033[F")
    if choice == "1":
        install_certbot()
    elif choice == "2":
        install_ssl()
    elif choice == "3":
        quit
    else:
        manage_ssl()

def install_certbot():
    print("Do you want to install Certbot ?[Y/n]")
    reply = input()
    sys.stdout.write("\033[F")
    if reply == "Y" or reply == "y":
        if path.exists("/usr/bin/certbot"):
            print("Certbot already exist on server, go back !!!")
            install_certbot()
        else:
            print("Installing Certbot ...")
            system("apt-get install certbot -y >/dev/null 2>&1; apt-get install python-certbot-nginx -y >/dev/null 2>&1")
    elif reply == "N" or reply == "n":
        print("You do not want to install Certbot, exit !!!")
        manage_ssl()
    else:
        manage_ssl()

def install_ssl():
    print("Please select domain:")
    list_domain = listdir("/var/www/vhosts/")
    if path.exists("/var/www/vhosts/system/"):
        list_domain.remove("system")
        list_domain = enumerate(list_domain)
            # print("List domain in server: 1. {}\t2. {}".format(list_domain))
        list(list_domain)
        for idx, domain in enumerate(list_domain, 1):
            print(str(idx) + ".", domain)
        choice = input()
        if choice == "1":
            select_domain = (enumerate(domain))
            print(list(select_domain))
    else:
        # for i in list_domain:
            # print("List domain in server: 1. {}\t2. {}".format(list_domain))
        list(list_domain)
        for idx, domain in enumerate(list_domain, 1):
            print(str(idx) + ".", domain)
        choice = input()
        if choice == "1":
            select_domain = (enumerate(domain))
            print(select_domain)
    

def main():
    manage_ssl()

if __name__ == "__main__":
    main()