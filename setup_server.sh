#!/bin/bash
# Kich ban
# 1. Update all
# 2. Gen SSH-Key
# 3. Install Plesk
# 4. Firewall

# 1. Update
echo "Updating ..."
yum clean all > /dev/null 2>&1
yum update -y > /var/log/SA_Update.log
echo "Update completed !"
# 1.1 Install python 3
if [ ! -f /usr/bin/python3 ]; then
    echo "Install Python3"
    yum install -y python3 > /var/log/SA_Update.log
    echo Install completed !
else
    echo Python 3 already exist
fi
# 1.2 Run Python scripts
echo "Running Python for new server $(hostname -I | awk {'print$1'})"
setup_server.py