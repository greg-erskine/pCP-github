#!/bin/ksh
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
#
PATH=/usr/local/bin:$PATH

HOSTNAME=$(hostname -s)

print -u2 "Connect: $(date +%Y%m%d%H%M%S)"

# ##############################################################
## read http request
##

read method url proto
print -u2 "$method $url $proto"

if echo "$proto" | grep -q 'HTTP/1.'
then
  read a
  print -u2 "$a"
  while echo -n "$a" | egrep -q :
  do
    read a
    print -u2 "$a"
  done
fi


## ##############################################################
## output arguments using CRLF line termination
##

output () {
    print "$@\r"
}

## ##############################################################
## only GET requests supported
##

case "$method" in
   "GET" )
      ;;
   * )
      print -u2 "unsupported method: $method"
      output "$proto 404 Not Found"
      output
      exit 404
      ;;
esac

## ##############################################################
## only HTTP/1.0 and 1.1 supported
## remove trailing CR at end of proto
## (what else?)
##

case "$proto" in
   
   "HTTP/1.0"* )
      proto="HTTP/1.0"
      ;;
      
   "HTTP/1.1"* )
      proto="HTTP/1.1"
      ;;

   * )
      print -u2 "unsupported protocol: $proto"
      output "$proto 404 Not Found"
      output
      exit 404
      ;;
esac 

## ##############################################################
## setup for encoding
## http://picoreplayer:9100/S16_LE/44100/2/F
##
FORMAT=$(echo ${url} | awk -F/ '{printf "%s", $2}')
RATE=$(echo ${url} | awk -F/ '{printf "%s", $3}')
CHLS=$(echo ${url} | awk -F/ '{printf "%s", $4}')
CODEC=$(echo ${url} | awk -F/ '{printf "%s", $5}')
ORDERING=little
ENCODING=signed-integer

case "$FORMAT" in
    S16_LE)
        BITS=16
	;;
    S24_LE)
        BITS=24
	;;
    S32_LE)
        BITS=32
	;;
    *)
        print -u2 "$FORMAT not supported."
        print -u2 ""
        output "$url 404 Not Found"
        output
        exit 404
        ;;
esac

case "$CODEC" in
   "F" )
      outdesc="(flac)"
      outformat="--type flac --compression 4"
      type="audio/x-flac"
      bits=$(((${RATE} * ${BITS} * ${CHLS}) * 0.65))
      bits=${bits%.*}
      ;;
   "M" )
      outdesc="(mp3)"
      outformat="--type mp3 --compression 320"
      type="audio/mpeg"
      bits=320
      ;;
    * )
      print -u2 "unsupported url: $url"
      output "$url 404 Not Found"
      output
      exit 404
      ;;
esac

name="pCP ${HOSTNAME} line-in ${outdesc}"

post="sox --type raw --bits ${BITS} --channels ${CHLS} --rate ${RATE} --encoding ${ENCODING} --endian ${ORDERING} - ${outformat} -"

record="arecord --file-type=raw --duration=0 --channels=${CHLS} --format=${FORMAT} --rate=${RATE} --buffer-time=20000000 --device=pcpinput"

## ##############################################################
## generate audio data on stdout

pcm () {
    $record
}


## ##############################################################
## generate http headers
##
output "${proto} 200 OK"
print -u2 "${proto} 200 OK"

output "Content-Type: ${type}"
print -u2 "Content-Type: ${type}"

output "icy-br: ${bits}"
print -u2 "icy-br: ${bits}"

output "icy-name: ${name}"
print -u2 "icy-name: ${name}"

output "icy-metadata: 0"
print -u2 "icy-metadata: 0"

output

## ##############################################################
## LMS opens a url twice without '#slim:noscan=1' appended to
## the url. The first scan sometimes leaves the record command
## running, causing the second open to fail with device busy.
##
## If the record command is already running, kill it
##
recordpid="$(pgrep -f "$record")"

if [ ! -z $recordpid ]; then
	print -u2 "Killing previous record cmd with pid:$recordpid".
	kill $recordpid
	sleep 2
fi

pcm | $post

print -u2 "Disconnect: $(date +%Y%m%d%H%M%S)"
print -u2 ""
