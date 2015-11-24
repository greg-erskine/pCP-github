#/bin/sh

#========================================================================================
# This script copies www and it's sub directories from the local piCorePlayer to a
# remote piCorePlayer. It also does a backup.
#
# You will be prompted for the remote piCorePlayer's password twice.
#
# NOTE: This requires the dropbear bug fix to be done on both the local and
#       remote piCorePlayers.
#----------------------------------------------------------------------------------------

# Version: 0.01 2015-06-30 GE
#	Original.

if [ "x" == $1"x" ]; then
    echo "Usage: $0 192.168.1.xxx"
    exit 1
else
    scp -r -p /home/tc/www/* tc@$1:/home/tc/www/
    ssh tc@$1 sudo filetool.sh -b
fi

exit 0
