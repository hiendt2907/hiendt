#/bin/bash
list_user=$(plesk bin subsciption --list)
for i in $list_user
do
path="/var/www/vhost"
    if [ -e $path/wp-config.php ]; then
        echo $i using WP
    elif [ -e $path/configuration.php ]; then
        echo $i using Joomla
    elif [ -e $path/.env ]; then
        echo $i using Laravel
    elif [ -e $path/timthumb.php ]; then
        echo $i using nina
    elif [ -e $path/app/Mage.php ]; then
        echo $i using Magento
    elif [ -e $path/course/admin.php ]; then
        echo $i using Moodle
    else
        echo $i not using any Framework
    fi
done


#/bin/bash
list_user=$(plesk bin subscription --list)
for i in $list_user
do
path="/var/www/vhosts/$i/httpdocs"
    if [ -e $path/wp-config.php ]; then
        echo $i using WP
    elif [ -e $path/configuration.php ]; then
        echo $i using Joomla
    elif [ -e $path/.env ]; then
        echo $i using Laravel
    elif [ -e $path/timthumb.php ]; then
        echo $i using nina
    elif [ -e $path/app/Mage.php ]; then
        echo $i using Magento
    elif [ -e $path/course/admin.php ]; then
        echo $i using Moodle
    else
        echo $i not using any Framework
    fi
done