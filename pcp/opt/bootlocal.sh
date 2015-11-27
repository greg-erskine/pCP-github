#!/bin/sh
# put other system startup commands here

GREEN="$(echo -e '\033[1;32m')"

[ -f /home/tc/www/cgi-bin/autoresize.sh ] && . /home/tc/www/cgi-bin/autoresize.sh

echo
echo "${GREEN}Running bootlocal.sh..."
/home/tc/www/cgi-bin/do_rebootstuff.sh
