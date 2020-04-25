#!/bin/sh

# Version: 6.0.0 2020-01-25

. pcp-functions

pcp_html_head "Write to config.txt" "SBP"

pcp_banner
pcp_running_script
pcp_remove_query_string
pcp_httpd_query_string

REBOOT_REQUIRED=TRUE
#========================================================================================
# Write to BOOTMNT/config.txt
#----------------------------------------------------------------------------------------
case $ACTION in

	Rotation)
		pcp_table_top "Rotate screen"
		echo '<p class="info">[ INFO ] Setting screen rotate to '$SCREENROTATE'</p>'

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
				echo '<p class="error">[ ERROR ] Error setting screen rotate to '$SCREENROTATE'</p>'
			;;
		esac
	;;
	Size)
		[ "$JL_SCREEN_WIDTH" = "" ] && JL_SCREEN_WIDTH=0
		[ "$JL_SCREEN_HEIGHT" = "" ] && JL_SCREEN_HEIGHT=0
		pcp_table_top "Setting Frame Buffer Screen Size"
		pcp_mount_bootpart
		if [ "$JL_SCREEN_WIDTH" != "0" -a "$JL_SCREEN_HEIGHT" != "0" ]; then
		echo '<p class="info">[ INFO ] Setting Jivelite screen width to '$JL_SCREEN_WIDTH'</p>'
		echo '<p class="info">[ INFO ] Setting Jivelite screen height to '$JL_SCREEN_HEIGHT'</p>'
			sed -i 's/#framebuffer_height/framebuffer_height/' $CONFIGTXT
			sed -i "s/\(framebuffer_height=\).*/\1$JL_SCREEN_HEIGHT/" $CONFIGTXT
			sed -i 's/#framebuffer_width/framebuffer_width/' $CONFIGTXT
			sed -i "s/\(framebuffer_width=\).*/\1$JL_SCREEN_WIDTH/" $CONFIGTXT
		else
			echo '<p class="info">[ INFO ] Setting Jivelite screen size to default values</p>'
			# Reset to default disabled.
			sed -i 's/.*\(framebuffer_height\).*/#framebuffer_height=720/' $CONFIGTXT
			sed -i 's/.*\(framebuffer_width\).*/#framebuffer_width=1280/' $CONFIGTXT
		fi
		pcp_umount_bootpart
	;;
	FrameBuffer)
		pcp_table_top "Setting Frame Buffer"
		echo '<p class="info">[ INFO ] Setting Frame Buffer device to '$JL_FRAME_BUFFER'</p>'
		echo '<p class="info">[ INFO ] Setting Frame Buffer refresh rate to '$JL_FRAME_RATE'</p>'
		echo '<p class="info">[ INFO ] Setting Frame Buffer color depth to '$JL_FRAME_DEPTH'</p>'
		echo '<p class="info">[ INFO ] Restart Jivelite for settings to take effect.</p>'
		unset REBOOT_REQUIRED
	;;
esac

pcp_save_to_config
pcp_backup
pcp_table_middle
pcp_redirect_button "Go to Tweaks" "tweaks.cgi" 10
pcp_table_end

pcp_footer
pcp_copyright
[ $REBOOT_REQUIRED ] && pcp_reboot_required

echo '</body>'
echo '</html>'