#!/usr/bin/env python3
import subprocess
from os import system, sys, path, listdir, makedirs
import getpass
#import netifaces as ni
import string
import random

def domain():
    print("Welcome to Domain page, please enter your choice:\n1. Add new domain\t2. List domain\t\t3. Add alias\n4. Back")
    choice = input()
    sys.stdout.write("\033[F")
    if choice == "1":
        ni.ifaddresses('ens4')
        IP = ni.ifaddresses('ens4')[ni.AF_INET][0]['addr']
        domain_name = input("Please enter domain name: ")
        ssl_path = domain_name + ".crt"
        key_path = domain_name + ".key"
        root_path = "/var/www/vhosts/"
        domain_path = root_path + domain_name
        default_path_conf = "/etc/nginx/sites-available/"
        conf_path = default_path_conf + domain_name
        if not path.exists(domain_path):
            str(makedirs(domain_path))
            str(makedirs(domain_path + "/ssl/"))
            # makedirs(conf_path)
            print("Please select your php version:\n1. 7.2\t2. 7.3\t3. 7.4\t4. 8.0")
            php = input()
            sys.stdout.write("\033[F")
            if php == "1":
                php_ver = "php7.2-fpm.sock"
            elif php == "2":
                php_ver = "php7.3-fpm.sock"
            elif php == "3":
                php_ver = "php7.4-fpm.sock"
            elif php == "4":
                php_ver = "php8.0-fpm.sock"
            else:
                print("Please select again php version")
                php = input()
            
            LETTERS = string.ascii_letters
            def random_user(length=6):
                printable = f"{LETTERS}"
                printable = list(printable)
                random.shuffle(printable)
                random_user = random.choices(printable, k=length)
                random_user = ''.join(random_user).lower()
                return(random_user)

            username = str(domain_name.split(".")[0]) + str(random_user())
            password = getpass.getpass()
            print(username, password)
            try:
                # executing useradd command using subprocess module 
                subprocess.run(['useradd', '-p', password, username, '-d', domain_path])
            except:
                print(f"Failed to add user.")
                sys.exit(1)
            f = open(conf_path, "a")
            f.write("""server {
                listen  """ + IP + """:80;
                server_name  """ + domain_name + """;
                root         """ + domain_path + """;
                access_log /var/log/nginx/""" + domain_name + """-access.log;
                error_log  /var/log/nginx/""" + domain_name + """-error.log error;
                index index.html index.htm index.php;
                location / {
                            try_files $uri $uri/ /index.php$is_args$args;
                }
                location ~ \.php$ {
                      fastcgi_split_path_info ^(.+\.php)(/.+)$;
                      fastcgi_pass unix:/var/run/""" + php_ver + """;
                      fastcgi_index index.php;
                      include fastcgi.conf;
                }
                  }""")
            f.close()
            f = open(domain_path + "/index.html", "a")
            f.write("""<!doctype html>

                        <html lang="en">
                        <head>
                        <meta charset="utf-8">

                        <title>Welcome to MatBao page</title>
                        <meta name="description" content="MatBao page default">
                        <meta name="author" content="HienDT">

                        </head>

                        <body>
                            Welcome to MatBao default page !!!
                        </body>
                        </html>""")
            f.close()
            system("ln -s " + conf_path + " " + "/etc/nginx/sites-enabled/" + ";" + "systemctl restart nginx")
            system("chown -R root." + username + " " + domain_path)
            system('echo ' + "\"" + password + "\"" + " " + "|" + " " + 'ftpasswd opts --stdin --passwd --file=/etc/proftpd/ftpd.passwd --name=' + username + ' --uid=60 --gid=60 --home=' + domain_path + ' --shell=/bin/false')
            domain()
        else:
            print("Domain {} already exist".format(domain_name))
            domain()
    # print("Hostname: {}, Domain: {}, ssl_path: {}, key_path {}, PHP version: {}".format(IP, domain_name, ssl_path, key_path, php_ver))
    elif choice == "2":
        list_domain = listdir("/var/www/vhosts/")
        if path.exists("/var/www/vhosts/system/"):
            list_domain.remove("system")
        else:
            print("List domain in server: {}".format(list_domain))
        domain()
    elif choice == "4":
        quit
        # system("mb")
    else:
        print("Please enter your choice !!!")
        domain()
def main():
    domain()

if __name__ == "__main__":
    main()
