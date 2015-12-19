#!/bin/sh +x

# Reference:
#	http://pastebin.com/api

#========================================================================================
# API settings
#----------------------------------------------------------------------------------------
API_DEV_KEY="1acc46fbd0d045362c91ae88d6c46bc5"
API_USER_NAME="piCorePlayer"
API_USER_PASSWORD="picoreplayer"
API_PASTE_PRIVATE="2"
API_PASTE_NAME="pcp"
API_PASTE_EXPIRE_DATE="1D"

#========================================================================================
# urlencode is not installed by default in piCore/piCorePlayer
# Reference: http://stackoverflow.com/questions/296536/how-to-urlencode-data-for-curl-command/10660730#10660730
#----------------------------------------------------------------------------------------
encoding() {
	local string="${1}"
	local strlen=${#string}
	local encoded=""
	local pos=0

	while [ $pos -lt $strlen ]
	do
		c="${string:$pos:1}"
		case "$c" in
			[-_.~a-zA-Z0-9])
				o="${c}"
				;;
			*)
				o=%$(echo -n "${c}" | hexdump -e '/1 "%02x"')
				;;
		esac
		encoded=$encoded"${o}"
		pos=$(($pos + 1))
	done
	echo "${encoded}" 
}

#========================================================================================
# Get api_user_key
#----------------------------------------------------------------------------------------
get_api_user_key() {
	POST_DATA="api_dev_key=$API_DEV_KEY"
	POST_DATA=$POST_DATA"&api_user_name=$API_USER_NAME"
	POST_DATA=$POST_DATA"&api_user_password=$API_USER_PASSWORD"

	API_USER_KEY=$(wget -O - --post-data=$POST_DATA 'http://pastebin.com/api/api_login.php')

	echo api_user_key: $API_USER_KEY
}

#========================================================================================
# Listing Pastes Created By A User
#----------------------------------------------------------------------------------------
get_listing_by_user() {
	get_api_user_key

	POST_DATA="api_option=list"
	POST_DATA=$POST_DATA"&api_dev_key=$API_DEV_KEY"
	POST_DATA=$POST_DATA"&api_user_key=$API_USER_KEY"
	POST_DATA=$POST_DATA"&api_results_limit=10"

	$(wget -O /tmp/list.log --post-data=$POST_DATA 'http://pastebin.com/api/api_post.php')

	cat /tmp/list.log
}

#========================================================================================
# Paste text to pastebin
#----------------------------------------------------------------------------------------
get_api_user_key

API_POST_CODE=$(cat /usr/local/sbin/config.cfg)
API_POST_CODE=$(encoding "$API_POST_CODE")

POST_DATA="api_option=paste"
POST_DATA=$POST_DATA"&api_dev_key=$API_DEV_KEY"
POST_DATA=$POST_DATA"&api_paste_code=$API_POST_CODE"
POST_DATA=$POST_DATA"&api_paste_expire_date=$API_PASTE_EXPIRE_DATE"
POST_DATA=$POST_DATA"&api_paste_private=$API_PASTE_PRIVATE"
POST_DATA=$POST_DATA"&api_paste_name=$API_PASTE_NAME"
POST_DATA=$POST_DATA"&api_user_key=$API_USER_KEY"

PASTEBIN_URL=$(wget -O - --post-data=$POST_DATA 'http://pastebin.com/api/api_post.php')

echo url: $PASTEBIN_URL

get_listing_by_user
