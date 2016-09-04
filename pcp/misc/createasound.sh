cat /proc/asound/card[0-9]*/id | \
awk ' \
{ print \
"pcm."$1" { type hw; card "$1"; }\
ctl."$1" { type hw; card "$1"; }" }
END
{ print \
"pcm.!default pcm."default_card"\
ctl.!default ctl."default_card}'
