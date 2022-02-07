#!/usr/bin/env python3
import subprocess
from os import system, sys, path, listdir, makedirs
import getpass
#import netifaces as ni
import string
import random
from mb import start

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
        conf_path = root_path + "system/" + domain_name + "/conf/"
        if not path.exists(domain_path):
            makedirs(domain_path)
            makedirs(conf_path)
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
                subprocess.run(['useradd', '-p', password, username, '-s', '/bin/false', '-d', domain_path])       
            except:
                print(f"Failed to add user.")
                sys.exit(1)
            f = open(conf_path + "nginx.conf", "a")
            f.write("""#ATTENTION!
                #
                #DO NOT MODIFY THIS FILE BECAUSE IT WAS GENERATED AUTOMATICALLY,
                #SO ALL YOUR CHANGES WILL BE LOST THE NEXT TIME THE FILE IS GENERATED.

                server {
                    listen """ + IP + """:443 ssl http2;

                    server_name """ + domain_name + """;
                    server_name www.""" + domain_name + """;
                    server_name ipv4.""" + domain_name + """;

                    ssl_certificate             /var/www/vhosts/ssl/""" + ssl_path + """;
                    ssl_certificate_key         /var/www/vhosts/ssl/""" + key_path + """;

                    client_max_body_size 128m;

                    proxy_read_timeout 300;
                    root "/var/www/vhosts/""" + domain_name + """/public_html";
                    access_log "/var/log/nginx/access_log";
                    error_log "/var/log/nginx/error_log";

                    #extension wp-toolkit begin
                    # "Block unauthorized access to wp-config.php"
                    # To remove this rule, revert this security measure on each WordPress installation on this domain
                    location ~* wp-config.php { deny all; }

                    # "Forbid execution of PHP scripts in the wp-content/uploads directory"
                    # To remove this rule, revert this security measure for WordPress installation #70
                    location ~* "^(?:/)wp-content/uploads/.*\.php" { deny all; }

                    # "Forbid execution of PHP scripts in the wp-includes directory"
                    # To remove this rule, revert this security measure for WordPress installation #70
                    location ~* "^(?:/)wp-includes/(?!js/tinymce/wp\-tinymce\.php$).*\.php" {
                        deny all;
                    }

                    # "Disable scripts concatenation for WordPress admin panel"
                    # To remove this rule, revert this security measure for WordPress installation #70
                    location ~* "^(?:/)wp-admin/(load-styles|load-scripts)\.php" { deny all; }

                    # "Enable hotlink protection"
                    # To remove this rule, revert this security measure for WordPress installation #70
                    if ($http_referer !~* "^$|^https?://(.*\.)?(thietbidocongnghiep\.net|google\.com)(:|/|$)") {
                        rewrite "^(?:/)wp-content/uploads/.*\.(gif|png|jpeg|jpg|svg)$" "/fake-hotlink-stub" last;
                    }

                    location = "/fake-hotlink-stub" {
                        internal;
                        if (!-f "/var/www/vhosts/domain_name/public_html/wpt-hotlinked-image-stub.png") {
                            return 403;
                        }
                        rewrite ^ "/wpt-hotlinked-image-stub.png" last;
                    }

                    # "Block author scans"
                    # To remove this rule, revert this security measure for WordPress installation #70
                    if ($query_string ~ "author=\d+") {
                        rewrite "^/(?!wp-admin/)" "/fake-author-scan" last;
                    }

                    # "Disable PHP execution in cache directories"
                    # To remove this rule, revert this security measure on each WordPress installation on this domain
                    location ~* ".*/cache/.*\.ph(?:p[345]?|t|tml)" {
                        access_log off;
                        log_not_found off;
                        deny all;
                    }

                    # "Block author scans"
                    # To remove this rule, revert this security measure on each WordPress installation on this domain
                    location = /fake-author-scan {
                        internal;
                        deny all;
                    }

                    # "Block author scans"
                    # To remove this rule, revert this security measure on each WordPress installation on this domain
                    location ~* "(?:wp-config\.bak|\.wp-config\.php\.swp|(?:readme|license|changelog|-config|-sample)\.(?:php|md|txt|htm|html))" {
                        return 403;
                    }

                    # "Block access to potentially sensitive files"
                    # To remove this rule, revert this security measure on each WordPress installation on this domain
                    location ~* ".*\.(?:psd|log|cmd|exe|bat|csh|ini|sh)$" {
                        return 403;
                    }

                    # "Block access to .htaccess and .htpasswd"
                    # To remove this rule, revert this security measure on each WordPress installation on this domain
                    location ~* /\.ht {
                        deny all;
                    }

                    # "Enable bot protection"
                    #To remove this rule, revert this security measure on each WordPress installation on this domain
                    if ($http_user_agent ~* "(?:acunetix|BLEXBot|domaincrawler\.com|LinkpadBot|MJ12bot/v|majestic12\.co\.uk|AhrefsBot|TwengaBot|SemrushBot|nikto|winhttp|Xenu\s+Link\s+Sleuth|Baiduspider|HTTrack|clshttp|harvest|extract|grab|miner|python-requests)") {
                        return 403;
                    }

                    # WordPress permalink
                    # To remove this rule, add "WordpressPermalinkHandlingFeature = false" in the [ext-wp-toolkit] section of panel.ini
                    set $sef_entry_point /;
                    if ($uri ~* "^/") {
                        set $sef_entry_point "/index.php?$args";
                    }
                    if ($uri ~* "^/OLD/") {
                        set $sef_entry_point "/OLD/index.php?$args";
                    }
                    error_page 404 = $sef_entry_point;

                    #extension wp-toolkit end

                    #extension letsencrypt begin
                    location ^~ /.well-known/acme-challenge/ {
                        root /var/www/vhosts/default/htdocs;

                        types { }
                        default_type text/plain;

                        satisfy any;
                        auth_basic off;
                        allow all;

                        location ~ ^/\.well-known/acme-challenge.*/\. {
                            deny all;
                        }
                    }
                    #extension letsencrypt end

                    #extension sslit begin

                    #extension sslit end

                    location ~ /\.ht {
                        deny all;
                    }

                    location ~ ^/~(.+?)(/.*?\.php)(/.*)?$ {
                        fastcgi_read_timeout 300;
                        fastcgi_split_path_info ^((?U).+\.php)(/?.+)$;
                        fastcgi_param PATH_INFO $fastcgi_path_info;
                        fastcgi_pass "unix:/var/run/php/""" + php_ver + """.sock";
                        include /etc/nginx/fastcgi.conf;

                    }

                    location ~ \.php(/.*)?$ {
                        fastcgi_read_timeout 300;
                        fastcgi_split_path_info ^((?U).+\.php)(/?.+)$;
                        fastcgi_param PATH_INFO $fastcgi_path_info;
                        fastcgi_pass "unix:/var/run/php/""" + php_ver + """.sock";
                        include /etc/nginx/fastcgi.conf;

                    }

                    location ~ /$ {
                        index "index.html" "index.cgi" "index.pl" "index.php" "index.xhtml" "index.htm" "index.shtml";
                    }

                    disable_symlinks if_not_owner "from=/var/www/vhosts/""" + domain_name + """;

                    include "/var/www/vhosts/system/""" + domain_name + """/conf/vhost_nginx.conf";
                }

                server {
                    listen """ + IP + """:80;

                    server_name """+ domain_name + """;
                    server_name www.""" + domain_name + """;
                    server_name ipv4.""" + domain_name + """;

                    client_max_body_size 128m;

                    proxy_read_timeout 300;

                    location / {
                        return 301 https://$host$request_uri;
                    }
                }""")
            f.close()
            system("chown -R root." + username + " " + domain_path)
        else:
            print("Domain {} already exist".format(domain_name))
            domain()
    # print("Hostname: {}, Domain: {}, ssl_path: {}, key_path {}, PHP version: {}".format(IP, domain_name, ssl_path, key_path, php_ver))
    elif choice == "2":
        list_domain = listdir("/var/www/vhosts/")
        print("List domain in server: {}".format(list_domain))
        domain()
    elif choice == "4":
        exit()
        system("mb")

def main():
    domain()

if __name__ == "__main__":
    main()
main()