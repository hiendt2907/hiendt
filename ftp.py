#!/usr/bin/env python3
import subprocess
from os import system, sys, path

def ftp():
    print("Installing FTP Server ...")
    if str(path.exists("/var/run/proftpd.pid")) == "True":
        print("FTP already exist on server !")
    else:
        print("Install FTP server")
        system("apt install proftpd -y")
        print("Install FTP server completed")

def main():
    ftp()


if __name__ == "__main__":
    main()