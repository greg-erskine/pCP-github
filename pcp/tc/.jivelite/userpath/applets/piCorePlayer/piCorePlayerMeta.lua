local io			= require("io")
local oo            		= require("loop.simple")
local AppletMeta    		= require("jive.AppletMeta")
local appletManager 		= appletManager
local jiveMain      		= jiveMain

module(...)
oo.class(_M, AppletMeta)

function jiveVersion(meta)
   return 1, 1
end

function registerApplet(meta)
   jiveMain:addItem(meta:menuItem('piCorePlayerApplet', 'settings', "piCorePlayer", function(applet, ...) applet:menu(...) end, 100))
end

function defaultSettings(meta)
        return { 
	}
end

function configureApplet(meta)
	if meta:getSettings()['pcp_rpi_display_brightness'] then
		_write("/sys/class/backlight/rpi_backlight/brightness", meta:getSettings()['pcp_rpi_display_brightness'])
	end
end

function _write(file, val)
	local fh, err = io.open(file, "w")
	if err then
		return
	end
	fh:write(val)
	fh:close()
end
