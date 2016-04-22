#!/bin/sh
# put other system startup commands here

GREEN="$(echo -e '\033[1;32m')"

echo
echo "${GREEN}Running bootlocal.sh..."
/home/tc/www/cgi-bin/do_rebootstuff.sh | tee -a /var/log/pcp_boot.log
