#!/bin/sh

# Version: 7.0.0 2020-06-03

VERSION="# Version: 7.0.0 $(date "+%Y-%m-%d")"

cat $1 | sed \
	-e '/_row_shade/ d' \
	-e '/<table/ d' \
	-e '/<fieldset/ d' \
	-e '/pcp_banner/ d' \
	-e '/pcp_running_script/ d' \
	-e '/pcp_picoreplayers_toolbar/ d' \
	-e '/COLUMN\(.*\)"col\(.*\)/ d' \
	-e '/pcp_table_middle/ d' \
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
	-e "s|<td class=\"\(.*\)\">|<div class=\"'\$COLUMN3_1'\">| g" \
	-e "s|<td colspan=\"\(.*\)\">|<div class=\"'\$COLUMN3_1'\">| g"

exit


COLUMN2_1="col-sm-2 text-md-right"
COLUMN2_1="col-sm-2 text-md-center"
COLUMN2_2="col-10"

COLUMN3_1="col-sm-2"
COLUMN3_2="col-sm-3"
COLUMN3_3="col-sm-7"

COLUMN4_1="col-sm-1 text-sm-right"
COLUMN4_2="col-sm-3"
COLUMN4_3="col-sm-2"
COLUMN4_4="col-sm-6"

pcp_infobox_begin "" 10
pcp_infobox_end

pcp_textarea_begin "" 10
pcp_textarea_end

echo '  <div class="'$BORDER'">'

pcp_heading5

pcp_helpbadge
echo '  <a type="button" data-toggle="collapse" data-target="#dt'$ID'">'$HELPBADGE'</a>'

echo '  <div class="form-group '$COLUMN2_1'">'
echo '    <input class="form-control form-control-sm"'

echo '  <div class="input-group '$COLUMN3_2'">'
echo '    <select class="custom-select custom-select-sm" id="audiocard" name="AUDIO">'

echo '  <div class="form-check form-check-inline">'
echo '    <input class="form-check-input" id="rad1" type="radio" name="d" value="1" '$D1SELECTED'>'
echo '    <label class="form-check-label" for="rad1">On</label>'

class="'$BUTTON'"



