#!/bin/sh

# Version: 6.0.0 2019-06-30

#========================================================================================
# This script copies www and it's sub directories from the local piCorePlayer to a
# remote piCorePlayer. It also does a backup.
#
# You will be prompted for the remote piCorePlayer's password twice.
#----------------------------------------------------------------------------------------

if [ x"" = x"$1" ]; then
	echo "Usage: $0 192.168.1.xxx"
	exit 1
else
	scp -r -p /home/tc/www/* tc@$1:/home/tc/www/
	ssh tc@$1 sudo filetool.sh -b
fi

exit 0
