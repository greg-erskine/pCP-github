local tostring				 = tostring
local os                     = require("os")
local oo                     = require("loop.simple")
local Applet                 = require("jive.Applet")
local Event                  = require("jive.ui.Event")
local Icon                   = require("jive.ui.Icon")
local Label                  = require("jive.ui.Label")
local Popup                  = require("jive.ui.Popup")
local SimpleMenu             = require("jive.ui.SimpleMenu")
local Window                 = require("jive.ui.Window")

module(...)
oo.class(_M, Applet)

function menu(self, menuItem)

	local menu = SimpleMenu("menu",
		{
			{ text = self:string("MENU_REBOOT"),
				callback = function(event, menuItem)
					self:rebootPi(menuItem)
				end
			},
			{ text = self:string("MENU_SHUTDOWN"),
				callback = function(event, menuItem)
					self:shutdownPi(menuItem)
				end
			},
			{ text = self:string("MENU_SAVE_SETTINGS"),
				callback = function(event, menuItem)
					self:saveToSDCard(menuItem)
				end
			},
		})
		
	-- create a window object
	local window = Window("window", "piCorePlayer") 

	-- add the SimpleMenu to the window
	window:addWidget(menu)

	self:tieAndShowWindow(window)
	return window
end

function rebootPi(self, menuItem)

	local popup = Popup("waiting_popup")

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
							icon:setStyle("icon_popup_box_power")
							label:setValue("")
							text:setValue(self:string("LABEL_REBOOTING"))
				       elseif state == -1 then
							os.execute("/home/tc/.local/bin/pcp rb")
				       end
				       state = state - 1
			       end)

	self:tieAndShowWindow(popup)
	return popup
end

function shutdownPi(self, menuItem)

	local popup = Popup("waiting_popup")

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
							os.execute("/home/tc/.local/bin/pcp sd")
				       end
				       state = state - 1
			       end)

	self:tieAndShowWindow(popup)
	return popup
end

function saveToSDCard(self, menuItem)

	local popup = Popup("toast_popup_text")
	
	popup:setTransparent(true)

	local text = Label("text", self:string("LABEL_SETTINGS_SAVED"))
	
	popup:addWidget(text)

	-- save piCorePlayer settings
	os.execute("/home/tc/.local/bin/pcp bu")
	
	-- display the message for 1.2 seconds
	popup:addTimer(1200, function()
						popup:hide(Window.transitionFadeOut)
			       end)

	self:tieAndShowWindow(popup, Window.transitionFadeIn)
	return popup
end
