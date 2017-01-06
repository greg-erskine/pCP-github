--
-- v2 adds pcp command in os.execute, backlight off when shutting down and Dutch translation
-- v3 adds version number checking
-- v4 adds backlight brightness adjustment for the official Raspberry Pi display rev. 1.1
-- v5 adds option to rescan LMS media library for pCP 2.x

-- Lua/Jive/JiveLite bugs/problems encountered:
--     - keyboard cursor key up moves volume slider down
--     - keyboard cursor key down moves volume slider up
--     - inconsistent behaviour when pressing 'right' on the remote or keyboard and the -first- menu item opens a popup which has a
--       brightness_slider or settings_slider -> looks like the 'right' press is ignored until you first press down and up!

local tostring			= tostring
local tonumber			= tonumber
local string			= require("string")
local math				= require("math")
local os				= require("os")
local io				= require("io")
local oo				= require("loop.simple")
local Event				= require("jive.ui.Event")
local Icon				= require("jive.ui.Icon")
local Label				= require("jive.ui.Label")
local Popup				= require("jive.ui.Popup")
local SimpleMenu		= require("jive.ui.SimpleMenu")
local Window			= require("jive.ui.Window")
local Slider			= require("jive.ui.Slider")
local Textarea			= require("jive.ui.Textarea")
local Group				= require("jive.ui.Group")
local Framework			= require("jive.ui.Framework")
local Font				= require("jive.ui.Font")

local Applet			= require("jive.Applet")
local System			= require("jive.System")
local Surface			= require("jive.ui.Surface")
local appletManager		= appletManager

module(..., Framework.constants)
oo.class(_M, Applet)

local pCP_1_22_reboot_cmd = "/home/tc/.local/bin/pcp rb"
local pCP_1_22_shutdown_cmd = "/home/tc/.local/bin/pcp sd"
local pCP_1_22_save_cmd = "/home/tc/.local/bin/pcp bu"

local pCP_2_0_reboot_cmd = "/usr/local/sbin/pcp rb"
local pCP_2_0_shutdown_cmd = "/usr/local/sbin/pcp sd"
local pCP_2_0_save_cmd = "/usr/local/sbin/pcp bu"

local pCP_default_reboot_cmd = "sudo reboot"
local pCP_default_shutdown_cmd = "sudo poweroff"
local pCP_default_save_cmd = "sudo filetool.sh -b"

local pCP_2_0_rescan_LMS_media_library = "/usr/local/sbin/pcp rescan"

function menu(self, menuItem)

	local window = Window("text_list", "piCorePlayer")
	local menu = SimpleMenu("menu")

	menu:addItem({ text = self:string("MENU_REBOOT"),
			callback = function(event, menuItem)
				self:rebootPi(menuItem)
			end })

	menu:addItem({ text = self:string("MENU_SHUTDOWN"),
			callback = function(event, menuItem)
				self:shutdownPi(menuItem)
			end })

	menu:addItem({ text = self:string("MENU_RESCAN_LMS_MEDIA_LIBRARY"),
			callback = function(event, menuItem)
				self:rescanLMSMediaLibrary(menuItem)
			end })

	menu:addItem({ text = self:string("MENU_ADJUST_BRIGHTNESS"),
			callback = function(event, menuItem)
				self:adjustDisplayBrightness(menuItem)
			end })

	menu:addItem({ text = self:string("MENU_SAVE_SETTINGS"),
			callback = function(event, menuItem)
				self:saveToSDCard(menuItem)
			end })

	window:addWidget(menu)

	self:tieAndShowWindow(window)
	return window
end

function adjustDisplayBrightness(self, menuItem)
	-- test if we can read from /sys/class/backlight/rpi_backlight/brightness
	local currentBrightness = tonumber(_read("/sys/class/backlight/rpi_backlight/brightness"))
		
	if currentBrightness ~= nil then
		-- read max brightness value from /sys/class/backlight/rpi_backlight/max_brightness
		local maxBrightness = tonumber(_read("/sys/class/backlight/rpi_backlight/max_brightness"))

		local popup = Popup("black_popup")

		popup:setAllowScreensaver(false)
		popup:setAlwaysOnTop(true)
		popup:setAutoHide(false)
		popup:setTransparent(false)

		popup:ignoreAllInputExcept({"esc", "back", "go_home", "scanner_rew", "volume_up", "volume_down", "play_preset_1", "play_preset_2", "play_preset_3", "play_preset_4", "play_preset_5", "play_preset_6", "play_preset_7", "play_preset_8", "play_preset_9", "play_preset_0"})
		
		local cancelBrightnessAction = function()
				popup:hide()
				return EVENT_CONSUME
			end

		popup:addActionListener("esc", self, cancelBrightnessAction)
		popup:addActionListener("back", self, cancelBrightnessAction)
		popup:addActionListener("go_home", self, cancelBrightnessAction)
		popup:addActionListener("scanner_rew", self, cancelBrightnessAction)
		
		local labelText = tostring(self:string("LABEL_ADJUST_BRIGHTNESS"))

		local label = Label("text", labelText .. " " .. tostring(currentBrightness))
		local help = Textarea("help_text", self:string("HELP_TEXT_ADJUST_BRIGHTNESS"))

		local slider = Slider("brightness_slider", 0, maxBrightness, currentBrightness,
			function(slider, value)
				label:setValue(labelText .. " " .. tostring(value))
				_write("/sys/class/backlight/rpi_backlight/brightness", tostring(value))
			end)

		local brightnessUpAction = function()
				if slider:getValue() < maxBrightness then
					slider:setValue(slider:getValue() + 1)
					label:setValue(labelText .. " " .. tostring(slider:getValue()))
					_write("/sys/class/backlight/rpi_backlight/brightness", slider:getValue())
					return EVENT_CONSUME
				end
				return EVENT_UNUSED
		end

		local brightnessDownAction = function()
				if slider:getValue() > 0 then
					slider:setValue(slider:getValue() - 1)
					label:setValue(labelText .. " " .. tostring(slider:getValue()))
					_write("/sys/class/backlight/rpi_backlight/brightness", slider:getValue())
					return EVENT_CONSUME
				end
				return EVENT_UNUSED
		end

		popup:addActionListener("volume_up", self, brightnessUpAction)
		popup:addActionListener("volume_down", self, brightnessDownAction)

		local brightnessPercentAction = function(self, event)
				local eventName = event:getAction()
				if eventName == "play_preset_0" then
					slider:setValue(maxBrightness)
					label:setValue(labelText .. " " .. tostring(slider:getValue()))
					_write("/sys/class/backlight/rpi_backlight/brightness", slider:getValue())
					return EVENT_CONSUME
				else
					local presetNumber = tonumber(string.sub(eventName, -1))
					slider:setValue(math.floor((maxBrightness / 100) * (10 * presetNumber)))
					label:setValue(labelText .. " " .. tostring(slider:getValue()))
					_write("/sys/class/backlight/rpi_backlight/brightness", slider:getValue())
					return EVENT_CONSUME
				end
				return EVENT_UNUSED
		end

		popup:addActionListener("play_preset_1", self, brightnessPercentAction)
		popup:addActionListener("play_preset_2", self, brightnessPercentAction)
		popup:addActionListener("play_preset_3", self, brightnessPercentAction)
		popup:addActionListener("play_preset_4", self, brightnessPercentAction)
		popup:addActionListener("play_preset_5", self, brightnessPercentAction)
		popup:addActionListener("play_preset_6", self, brightnessPercentAction)
		popup:addActionListener("play_preset_7", self, brightnessPercentAction)
		popup:addActionListener("play_preset_8", self, brightnessPercentAction)
		popup:addActionListener("play_preset_9", self, brightnessPercentAction)
		popup:addActionListener("play_preset_0", self, brightnessPercentAction)

		popup:addListener(EVENT_MOUSE_PRESS,
			function(event)
				 popup:hide()
				 return EVENT_CONSUME
			end)

		popup:addWidget(label)
		popup:addWidget(help)
		popup:addWidget(Group("slider_group", {
					 min = Icon("brightness_group.down"),
					 slider = slider,
					 max = Icon("brightness_group.up")
				 }))

		self:tieAndShowWindow(popup)
		return popup
	else
		local popup = Popup("toast_popup_text")

		popup:setAllowScreensaver(false)
		popup:setTransparent(true)

		local text = Label("text", self:string("NO_DISPLAY_FOUND_ADJUST_BRIGHTNESS"))

		popup:addWidget(text)

		popup:showBriefly(1750, nil, Window.transitionFadeIn, Window.transitionFadeOut)
		return popup
	end
end

function rebootPi(self, menuItem)
	local pcpVersion = tonumber(getpCPVersion())

	local popup = Popup("black_popup")

	popup:setAllowScreensaver(false)
	popup:setAlwaysOnTop(true)
	popup:setAutoHide(false)
	popup:setTransparent(false)

	local icon = Icon("icon_connecting")
	local text = Label("text", self:string("LABEL_REBOOT_IN_PROGRESS"))
	local label = Label("subtext", self:string("LABEL_COUNTDOWN_5_SECONDS"))

	popup:addWidget(label)
	popup:addWidget(icon)
	popup:addWidget(text)

	local state = 4
	popup:addTimer(1000, function()
		   if state == 4 then
			   label:setValue(self:string("LABEL_COUNTDOWN_4_SECONDS"))
		   elseif state == 3 then
			   label:setValue(self:string("LABEL_COUNTDOWN_3_SECONDS"))
		   elseif state == 2 then
			   label:setValue(self:string("LABEL_COUNTDOWN_2_SECONDS"))
		   elseif state == 1 then
			   label:setValue(self:string("LABEL_COUNTDOWN_1_SECOND"))
		   elseif state == 0 then
				icon:setStyle("")
				label:setValue("")
				text:setValue(self:string("LABEL_REBOOTING"))
		   elseif state == -1 then
				if pcpVersion ~= nil then
					-- pcpVersion is a number
					if pcpVersion >= 2.00 then
						os.execute(pCP_2_0_reboot_cmd)
					elseif pcpVersion >= 1.22 then
						os.execute(pCP_1_22_reboot_cmd)
					else
						os.execute(pCP_default_reboot_cmd)
					end
				else
					os.execute(pCP_default_reboot_cmd)
				end
		   end
		   state = state - 1
	   end)

	self:tieAndShowWindow(popup)
	return popup
end

function shutdownPi(self, menuItem)
	local pcpVersion = tonumber(getpCPVersion())

	local popup = Popup("black_popup")

	popup:setAllowScreensaver(false)
	popup:setAlwaysOnTop(true)
	popup:setAutoHide(false)
	popup:setTransparent(false)

	local icon = Icon("icon_connecting")
	local text = Label("text", self:string("LABEL_SHUTDOWN_IN_PROGRESS"))
	local label = Label("subtext", self:string("LABEL_COUNTDOWN_5_SECONDS"))

	popup:addWidget(label)
	popup:addWidget(icon)
	popup:addWidget(text)

	local state = 4
	popup:addTimer(1000, function()
		   if state == 4 then
			   label:setValue(self:string("LABEL_COUNTDOWN_4_SECONDS"))
		   elseif state == 3 then
			   label:setValue(self:string("LABEL_COUNTDOWN_3_SECONDS"))
		   elseif state == 2 then
			   label:setValue(self:string("LABEL_COUNTDOWN_2_SECONDS"))
		   elseif state == 1 then
			   label:setValue(self:string("LABEL_COUNTDOWN_1_SECOND"))
		   elseif state == 0 then
				icon:setStyle("")
				label:setValue("")
				text:setValue(self:string("LABEL_SHUTTING_DOWN"))
		   elseif state == -1 then
				if pcpVersion ~= nil then
					-- pcpVersion is a number
					if pcpVersion >= 2.00 then
						-- turn off display!
						-- code from Ralphy's DisplayOffApplet.lua
						-- no need to remember the current state
						-- as the Pi is about to be powered off
						_write("/sys/class/backlight/rpi_backlight/bl_power", "1")
						os.execute(pCP_2_0_shutdown_cmd)
					elseif pcpVersion >= 1.22 then
						_write("/sys/class/backlight/rpi_backlight/bl_power", "1")
						os.execute(pCP_1_22_shutdown_cmd)
					else
						os.execute(pCP_default_shutdown_cmd)
					end
				else
					os.execute(pCP_default_shutdown_cmd)
				end
		   end
		   state = state - 1
	   end)

	self:tieAndShowWindow(popup)
	return popup
end

function rescanLMSMediaLibrary(self, menuItem)
	local pcpVersion = tonumber(getpCPVersion())

	local popup = Popup("toast_popup_text")

	popup:setAllowScreensaver(false)
	popup:setAutoHide(false)

	-- don't allow any keypress/touch command so user cannot interrupt the save command
	-- popup will hide when saving is done
	popup:ignoreAllInputExcept({""})

	local text = Label("text", tostring(self:string("LABEL_RESCAN_LMS_MEDIA_LIBRARY")))

	popup:addWidget(text)

	local state = "init"
	popup:addTimer(1000, function()
			if state == "init" then
				if pcpVersion ~= nil then
					-- pcpVersion is a number
					if pcpVersion >= 2.00 then
						os.execute(pCP_2_0_rescan_LMS_media_library)
					end
				end
				state = "done"
			elseif state == "done" then
				state = "hide"
			elseif state == "hide" then
				popup:hide(Window.transitionFadeOut)
			end
		end)

	self:tieAndShowWindow(popup, Window.transitionFadeIn)
	return popup
end

function saveToSDCard(self, menuItem)
	local pcpVersion = tonumber(getpCPVersion())

	local popup = Popup("toast_popup_text")

	popup:setAllowScreensaver(false)
	popup:setAutoHide(false)

	-- don't allow any keypress/touch command so user cannot interrupt the save command
	-- popup will hide when saving is done
	popup:ignoreAllInputExcept({""})

	local text = Label("text", tostring(self:string("LABEL_SAVING_SETTINGS")))

	popup:addWidget(text)

	local state = "not saved"
	popup:addTimer(1000, function()
			if state == "not saved" then
				--read current brightness value from /sys/class/backlight/rpi_backlight/brightness and save settings to settings\piCorePlayer.lua
				self:getSettings()['pcp_rpi_display_brightness'] = tonumber(_read("/sys/class/backlight/rpi_backlight/brightness"))
				self:storeSettings()
				if pcpVersion ~= nil then
					-- pcpVersion is a number
					if pcpVersion >= 2.00 then
						os.execute(pCP_2_0_save_cmd)
					elseif pcpVersion >= 1.22 then
						os.execute(pCP_1_22_save_cmd)
					else
						os.execute(pCP_default_save_cmd)
					end
				else
					os.execute(pCP_default_save_cmd)
				end
				text:setValue(self:string("LABEL_SETTINGS_SAVED"))
				state = "done"
			elseif state == "done" then
				state = "hide"
			elseif state == "hide" then
				popup:hide(Window.transitionFadeOut)
			end
		end)

	self:tieAndShowWindow(popup, Window.transitionFadeIn)
	return popup
end

function getpCPVersion()
	local fh, err = io.open("/usr/local/sbin/piversion.cfg","r")
	if err then
		return nil
	end
	local pcpv = fh:read("*all")
	fh:close()

	if string.find(pcpv, "%d+%.%d+") ~= nil then
		pcpv = string.sub(pcpv, string.find(pcpv, "%d+%.%d+"))
	else
		return nil
	end
	return pcpv
end

function _write(file, val)
	local fh, err = io.open(file, "w")
	if err then
		return
	end
	fh:write(val)
	fh:close()
end

function _read(file)
	local fh, err = io.open(file, "r")
	if err then
		return nil
	end
	local fc = fh:read("*all")
	fh:close()
	return fc
end
