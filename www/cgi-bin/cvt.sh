#!/bin/sh

# Version: 7.0.0 2020-05-15

VERSION="# Version: 7.0.0 $(date "+%Y-%m-%d")"

cat $1 | sed \
	-e '/_row_shade/ d' \
	-e '/table/ d' \
	-e '/fieldset/ d' \
	-e '/pcp_banner/ d' \
	-e '/pcp_running_script/ d' \
	-e '/pcp_picoreplayers_toolbar/ d' \
	-e "s|^# Version: \(.*\)|$VERSION| g" \
	-e 's|pcp_navigation|pcp_navbar| g' \
	-e 's/<tr>/<div>/ g' \
	-e 's|</tr>|</div>| g' \
	-e 's/<td>/<div>/ g' \
	-e 's|</td>|</div>| g' \
	-e 's|td  class=|div class=| g' \
	-e 's|tr class=|div class=| g' \
	-e "s|echo '\[ INFO \] |pcp_message INFO \"| g" \
	-e "s|echo '\[ ERROR \] |pcp_message ERROR \"| g" \
	-e "s|echo '\[ DEBUG \] |pcp_message DEBUG \"| g" \
	-e 's|pcp_textarea_inform|pcp_textarea| g' \
	-e 's|pcp_table_top|pcp_heading5| g' \
	-e 's|pcp_table_end|pcp_infoxbox_end| g' \
	-e "s|class=\"less|class=\"'\$COLLAPSE'| g" \
	-e "s|id=\"'\$ID'|id=\"dt'\$ID'| g" \
	-e "s|'\$ROWSHADE'|row| g" \
	-e "s|echo '\(.*\)<legend>\(.*\)</legend>'|pcp_heading5 \"\2\"| g" \
	-e 's|<td class="\(.*\)">|<div class="XXXX">| g' \
	-e 's|<td colspan="\(.*\)">|<div class="XXXX">| g' \
	-e "s|<a id=\"dt'\$ID'a\" class=\"moreless\" href=# onclick=\"return more('\\'''\$ID''\\'')\">more></a>'|GREG| g"

exit

COLUMN2_1="col-sm-2 text-md-right"
COLUMN2_1="col-sm-2 text-md-center"
COLUMN2_2="col-10"

pcp_infobox_begin
pcp_infobox_end

pcp_heading5

echo '  <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'

echo '  <div class="form-group '$COLUMN2_1'">'
echo '    <input class="form-control form-control-sm"'

echo '      <div class="input-group '$COLUMN3_2'">'
echo '        <select class="custom-select custom-select-sm" id="audiocard" name="AUDIO">'
