#!/bin/sh
urlencode() {
        echo -e $1 |awk '
BEGIN {
	for (i = 0; i <= 255; i++)
		ord[sprintf("%c", i)] = i
}
# Encode string with application/x-www-form-urlencoded escapes.
function escape(str,    c, len, res) {
	len = length(str)
	res = ""
	for (i = 1; i <= len; i++) {
		c = substr(str, i, 1);
		#if (c ~ /[0-9A-Za-z]/)
		if (c ~ /[-._*0-9A-Za-z]/)
			res = res c
#		else if (c == " ")
#			res = res "+"
		else
			res = res "%" sprintf("%02X", ord[c])
	}
	return res
}
# Escape every line of input.
{ print escape($0) }
'

}

TEST1="URL  SPACE  TEST"
TEST2="URL++SPACE++TEST"
TEST3="URL%20SPACE%20TEST"
TEST4="[]{}"
TEST5="This has a + in the code"
TEST6="This has a % in the code"

i=1
while [ $i -le 6 ]; do
	VAL=$(eval echo \${TEST${i}})
	busybox-httpd -f -d "$VAL"
	echo ""
	busybox-httpd -f -d "$(urlencode "$(busybox-httpd -f -d "$VAL")")"
#	urlencode "$1"
	echo ""
	i=$((i+1))
done

