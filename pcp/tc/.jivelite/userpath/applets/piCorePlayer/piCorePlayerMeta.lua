local oo            = require("loop.simple")
local AppletMeta    = require("jive.AppletMeta")
local jiveMain      = jiveMain

module(...)
oo.class(_M, AppletMeta)

function jiveVersion(meta)
   return 1, 1
end

function registerApplet(meta)
   jiveMain:addItem(meta:menuItem('piCorePlayerApplet', 'settings', "piCorePlayer", function(applet, ...) applet:menu(...) end, 100))
end
