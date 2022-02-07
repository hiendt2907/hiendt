#!/bin/bash
mysql -Ne "select db.host, db.db, db.user, user.password from db inner join user on user.host=db.host;"
host=$(cat /tmp/db_information.txt | awk {'print$1'})
database=$(cat /tmp/db_information.txt | awk {'print$2'})
user=$(cat /tmp/db_information.txt | awk {'print$3'})
password=$(cat /tmp/db_information.txt | awk {'print$4'})
password = $(openssl rand -base64 12)
for i in list_user
do
mysql -Ne "CREATE USER '$i'@localhost IDENTIFIED BY '$password'"
done
for j in list_db
do
mysql -Ne "CREATE DATABASE IF NOT EXIST $j"
done