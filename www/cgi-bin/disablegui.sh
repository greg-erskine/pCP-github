#!/bin/sh
# First stop webserver httpd and then also remove it from starting via do_rebootstuff

. pcp-functions
pcp_variables

#Stop web server NOW
sudo /usr/local/etc/init.d/httpd stop

#Toggle # on and off in do_rebootstuff.sh
sed -i 's/\/usr\/local\/etc\/init.d\/httpd start/\#\/usr\/local\/etc\/init.d\/httpd start/' $pCPHOME/do_rebootstuff.sh

#Save changes
pcp_backup

