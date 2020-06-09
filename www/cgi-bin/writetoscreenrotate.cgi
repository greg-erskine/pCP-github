#!/bin/sh

# Version: 7.0.0 2020-06-09

. pcp-functions

pcp_html_head "Write to config.txt" "SBP"

pcp_navbar
pcp_remove_query_string
pcp_httpd_query_string

REBOOT_REQUIRED=TRUE
#========================================================================================
# Write to $BOOTMNT/config.txt
#----------------------------------------------------------------------------------------
case $ACTION in

	Rotation)
		pcp_heading5 "Rotate screen"
		pcp_infobox_begin
		pcp_message INFO "Setting screen rotate to $SCREENROTATE" "text"

		case "$SCREENROTATE" in
			0|no)
				pcp_mount_bootpart
				sed -i "s/\(lcd_rotate=\).*/\10/" $CONFIGTXT
				pcp_umount_bootpart
			;;
			180|yes)
				pcp_mount_bootpart
				sed -i "s/\(lcd_rotate=\).*/\12/" $CONFIGTXT
				pcp_umount_bootpart
			;;
			*)
				pcp_message ERROR "Error setting screen rotate to $SCREENROTATE" "text"
			;;
		esac
	;;
	Size)
		[ "$JL_SCREEN_WIDTH" = "" ] && JL_SCREEN_WIDTH=0
		[ "$JL_SCREEN_HEIGHT" = "" ] && JL_SCREEN_HEIGHT=0
		pcp_heading5 "Setting Frame Buffer Screen Size"
		pcp_infobox_begin
		pcp_mount_bootpart
		if [ "$JL_SCREEN_WIDTH" != "0" -a "$JL_SCREEN_HEIGHT" != "0" ]; then
			pcp_message INFO "Setting Jivelite screen width to $JL_SCREEN_WIDTH" "text"
			pcp_message INFO "Setting Jivelite screen height to $JL_SCREEN_HEIGHT" "text"
			sed -i 's/#framebuffer_height/framebuffer_height/' $CONFIGTXT
			sed -i "s/\(framebuffer_height=\).*/\1$JL_SCREEN_HEIGHT/" $CONFIGTXT
			sed -i 's/#framebuffer_width/framebuffer_width/' $CONFIGTXT
			sed -i "s/\(framebuffer_width=\).*/\1$JL_SCREEN_WIDTH/" $CONFIGTXT
		else
			pcp_message INFO "Setting Jivelite screen size to default values" "text"
			# Reset to default disabled.
			sed -i 's/.*\(framebuffer_height\).*/#framebuffer_height=720/' $CONFIGTXT
			sed -i 's/.*\(framebuffer_width\).*/#framebuffer_width=1280/' $CONFIGTXT
		fi
		pcp_umount_bootpart
	;;
	FrameBuffer)
		pcp_heading5 "Setting Frame Buffer"
		pcp_infobox_begin
		pcp_message INFO "Setting Frame Buffer device to $JL_FRAME_BUFFER" "text"
		pcp_message INFO "Setting Frame Buffer refresh rate to $JL_FRAME_RATE" "text"
		pcp_message INFO "Setting Frame Buffer color depth to $JL_FRAME_DEPTH" "text"
		pcp_message INFO "Restart Jivelite for settings to take effect." "text"
		unset REBOOT_REQUIRED
	;;
esac

pcp_save_to_config
pcp_backup "text"
pcp_infobox_end
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 10

pcp_html_end
[ $REBOOT_REQUIRED ] && pcp_reboot_required
exit
