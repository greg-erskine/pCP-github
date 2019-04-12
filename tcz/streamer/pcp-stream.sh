#!/bin/ksh
PATH=/usr/local/bin:$PATH

HOSTNAME=$(hostname -s)

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
## http://rpi:9100/S16_LE/48000/2/F
##
print -u2 "URL: $url"

SIZE=$(echo ${url} | awk -F/ '{printf "%s", $2}')
RATE=$(echo ${url} | awk -F/ '{printf "%s", $3}')
CHLS=$(echo ${url} | awk -F/ '{printf "%s", $4}')
FMT=$(echo ${url} | awk -F/ '{printf "%s", $5}')

record="arecord -d0 -c${CHLS} -f ${SIZE} -r ${RATE} -twav -D pcpinput"

case "$FMT" in
   "F" )
      name="pCP ${HOSTNAME} line-in (flac)"
      post="flac --totally-silent --compression-level-4 -c -"
      type="audio/x-flac"
      bits=768
      ;;
   "M" )
      name="pCP ${HOSTNAME} line-in (mp3)"
      post="lame --silent --preset insane -r - -"
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

## ##############################################################
## generate audio data on stdout

wav () {
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
print -u2 ""

recordpid="$(pgrep -f "$record")"

# If the record command is already running, kill it
if [ ! -z $recordpid ]; then
	print -u2 "Killing previous record cmd with pid:$recordpid".
	kill $recordpid
	sleep 2
fi

wav | $post
