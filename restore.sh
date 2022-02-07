#!/bin/bash
backup=$(ls -lf /tmp/db | grep sql | cut -d "." -f1)
db=$(cat /tmp/db_information.txt | awk {'print$1'})
for i in $backup
do
    for j in $db
    do
        if [[ $i != $j ]];
        then
            echo "database $db does not have backup file"
        else
            echo $i == $j
        fi
    done
done

file=$(ls -lf /tmp/db | grep sql | cut -d "." -f1)
db=$(cat /tmp/db_information.txt | awk {'print$1'})