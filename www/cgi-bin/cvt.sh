#!/bin/sh

# Version: 7.0.0 2020-05-15

#sed -i "s/\(WIFI=\).*/\1\"$WIFI\"/" 

#cat $1 | sed -n '{
#			/pcp_start_row_shade/ d
#			/pcp_toggle_row_shade/ d
#			}'

cat $1 | sed \
	-e '/_row_shade/ d' \
	-e '/table/ d' \
	-e '/fieldset/ d' \
	-e '/pcp_banner/ d' \
	-e 's|pcp_navigation|pcp_navbar| g' \
	-e 's/<tr>/<div>/ g' \
	-e 's|</tr>|</div>| g' \
	-e 's/<td>/<div>/ g' \
	-e 's|</td>|</div>| g' \
	-e 's|td  class=|div class=| g' \
	-e 's|tr class=|div class=| g' \
	-e 's|pcp_textarea_inform|pcp_textarea| g' \
	-e "s|class=\"less|class=\"'\$COLLAPSE'| g" \
	-e "s|id=\"'\$ID'|id=\"dt'\$ID'| g" \
	-e "s|'\$ROWSHADE'|row| g" \
	-e "s|echo '\(.*\)<legend>\(.*\)</legend>'|pcp_heading5 \"\2\"| g" \
	-e 's|<td class="\(.*\)">|<div class="XXXX">| g' \
	-e 's|<td colspan="\(.*\)">|<div class="XXXX">| g' \
	-e "s|<a id=\"dt'\$ID'a\" class=\"moreless\" href=# onclick=\"return more('\\'''\$ID''\\'')\">more></a>'|GREG| g"



exit