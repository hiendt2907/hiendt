#!/usr/bin/env python3
import subprocess
from os import system, sys, path, listdir, makedirs
import getpass
import random
import string

LETTERS = string.ascii_letters

def random_user(length=6):
    printable = f"{LETTERS}"
    printable = list(printable)
    random.shuffle(printable)
    random_user = random.choices(printable, k=length)
    random_user = ''.join(random_user).lower()
    return(random_user)

def add_user():
    username = str("mbsystem.xyz".split(".")[0]) + str(random_user())
    password = getpass.getpass()
    print(username, password)
    try:
        # executing useradd command using subprocess module 
        subprocess.run(['useradd', '-p', password, username, '-d /var/www/vhosts/' ])       
    except:
        print(f"Failed to add user.")                      
        sys.exit(1)
add_user()