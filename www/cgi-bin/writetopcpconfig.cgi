#!/bin/sh

# Version: 6.0.0 2019-11-03

# This function is for writting to the pcp.cfg in the background.

. pcp-functions

pcp_httpd_query_string

if [ "$PCP_CUR_REPO" != "" ]; then
	case $PCP_CUR_REPO in
		1) 	echo $PCP_REPO_1 > /opt/tcemirror;;
		2) 	echo $PCP_REPO_2 > /opt/tcemirror;;
	esac
fi

pcp_save_to_config
echo "OK"


