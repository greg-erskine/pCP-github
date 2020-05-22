#!/usr/bin/micropython

# Version: 7.0.0 2020-05-22

# Title: Micropython
# Description: Micropython test

import uos as os
#import usubprocess as subprocess

def pcp_html_head(TITLE, AUTHOR, DESCRIPTION):
	print('''
<!DOCTYPE html>
<!-- Start of pcp_html_head -->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>pCP - ''' + TITLE + '''</title>
  <meta name="author" content="''' + AUTHOR + '''">
  <meta name="description" content="''' + DESCRIPTION + '''">
  <link rel="stylesheet" type="text/css" href="../css/piCorePlayer.css?5.1.0-b2">
  <link rel="icon" href="../images/pCP.png" type="image/x-icon" />
  <script src="../js/piCorePlayer.js"></script>
</head>

<body>
<!-- End of pcp_html_head -->''')

def pcp_banner():
	print('''
<!-- Start of pcp_banner -->
<table class="bgblack">
  <tr>
    <td style="height:148px">
      <p class="banner">
        <img src="../images/banner.png" alt="piCorePlayer" usemap="#hotspot" />
        <map name="hotspot">
          <area shape="rect" coords="0,0,790,140" href="about.cgi" alt="pCP Logo">
          <area shape="circle" coords="790,74,3" href="debug.cgi?m=100" alt="pCP Logo">
          <area shape="circle" coords="790,100,3" href="debug.cgi?a=0" alt="pCP Logo">
          <area shape="circle" coords="790,125,3" href="debug.cgi" alt="pCP Logo">
        </map>
      </p>
    </td>
  </tr>
</table>
<!-- End of pcp_banner -->''')

def pcp_footer1():
#	GREG = str(subprocess.check_output('version'))
	print('''
<!-- Start of pcp_footer -->
<table class="bgblack">
  <tr>
    <td>
      <p class="footer">
          '$NAME' |
          piCorePlayer v'$(pcp_picoreplayer_version)' |
          linux '$(pcp_linux_release)' |
          piCore v''' + GREG + ''' |
          Squeezelite v'$(pcp_squeezelite_version)'</p>
    </td>
  </tr>
</table>
<!-- End of pcp_footer -->''')

def pcp_footer():
	GREG = str(os.system('version'))

	print('''
<!-- Start of pcp_footer -->
<table class="bgblack">
  <tr>
    <td>
      <p class="footer">
          NAME |
          piCorePlayer v |
          piCore v''' + GREG + ''' |
          Squeezelite v</p>
    </td>
  </tr>
</table>
<!-- End of pcp_footer -->''')


def pcp_picore_version():
	print('yeaH')

#========================================================================================
# Main
#----------------------------------------------------------------------------------------
TITLE =  "uPython"
AUTHOR = "GE"
DESCRIPTION = "microPython Test"

#pcp_html_head(TITLE, AUTHOR, DESCRIPTION)

pcp_html_head("xxx", "AUTxxHOR", "DESCRIxxxPTION")


pcp_banner()

print('<p>Hello world</p>')
print('<p>' + AUTHOR + ' wrote this ' + DESCRIPTION + '</p>')

pcp_footer()
