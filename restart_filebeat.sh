#!/bin/bash

if [[ $1 = cPanel ]];
    then
    for i in `cat ipcpanel.txt`
    do
    ssh -p 15959 $i 'systemctl restart filebeat'
    echo $i done
    done
elif [[ $1 = Plesk ]];
    then
    for i in `cat ipplesk.txt`
    do
    ssh -p 16969 $i 'systemctl restart filebeat'
    echo $i done
    done
else
echo "Usage: sh /usr/local/bin/scan_alert_hosting_diskusage.sh cPanel / Plesk"
break
exit
fi