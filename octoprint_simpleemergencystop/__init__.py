# coding=utf-8

"""if __name__ == '__main__':

	loop = asyncio.get_event_loop()
	app = App()
	asyncio.ensure_future(app.run())
	loop.run_forever()"""


from __future__ import absolute_import, division, print_function, unicode_literals

import octoprint.plugin
import asyncio
import logging
import random

from nextion import TJC, EventType

class SimpleemergencystopPlugin(octoprint.plugin.StartupPlugin,
                                octoprint.plugin.TemplatePlugin,
                                octoprint.plugin.SettingsPlugin,
                                octoprint.plugin.AssetPlugin,
                                octoprint.plugin.SimpleApiPlugin):
    def __init__(self):
        self.emergencyGCODE = ""
        self.client = TJC('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 115200, self.event_handler)
        self.loop = asyncio.new_event_loop()
        self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        
        # Note: async event_handler can be used only in versions 1.8.0+ (versions 1.8.0+ supports both sync and async versions)
    async def event_handler(self, type_, data):
        if type_ == EventType.STARTUP:
            print('We have booted up!')
        elif type_ == EventType.TOUCH:
            print('A button (id: %d) was touched on page %d' % (data.component_id, data.page_id))
    
        logging.info('Event %s data: %s', type, str(data))
        #print('Event %s data: %s', type, str(data))
        #await self.client.set('t3.txt', '1.67')
        #print(await self.client.get('x0.txt'))
        if data.component_id == 5:
            print("G28")
            self._printer.commands("G28")
    
    async def run(self):
        await self.client.connect()
        #await self.client.set('t3.txt', '1.45')
        #await client.sleep()
        #await client.wakeup()
    
        # await client.command('sendxy=0')
    
        #print(await self.client.get('sleep'))
        #print(await self.client.get('field1.txt'))
        #await self.client.set('xO.txt', random.randint(0, 100))
    
        #await self.client.set('field1.txt', "%.1f" % (random.randint(0, 1000) / 10))
        #await self.client.set('field2.txt', "%.1f" % (random.randint(0, 1000) / 10))
        
        #await self.client.set('field3.txt', random.randint(0, 100))
    
        print('finished')

    def get_settings_defaults(self):
        return dict(
            emergencyGCODE="G28",
            confirmationDialog=False,
            big_button=False,
            enableMargin=False,
            marginValue=0,
        )

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.emergencyGCODE = self._settings.get(["emergencyGCODE"])

    def on_after_startup(self):
        self.emergencyGCODE = self._settings.get(["emergencyGCODE"])

    def get_template_configs(self):
        return [
            # dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

    def get_api_commands(self):
        return dict(
            emergencyStop=[]
        )

    def on_api_command(self, command, data):
        # check if there is a : in line
        find_this = ":"
        if find_this in str(self.emergencyGCODE):

            # if : found then, split, then for each:
            gcode_list = str(self.emergencyGCODE).split(':')
            for gcode in gcode_list:
                self._printer.commands(gcode)
        else:
            self._printer.commands(self.emergencyGCODE)

    def get_assets(self):

        return dict(
            js=["js/simpleemergencystop.js"],
            css=["css/simpleemergencystop.css", "css/fontawesome.all.min.css"]
        )

    # Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            simpleemergencystop=dict(
                displayName="Simple Emergency Stop",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="BrokenFire",
                repo="OctoPrint-SimpleEmergencyStop",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/BrokenFire/OctoPrint-SimpleEmergencyStop/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Simple Emergency Stop"
__plugin_pythoncompat__ = ">=2.7,<4"

print(__name__)

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = SimpleemergencystopPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

if __name__ == '__SimpleemergencystopPlugin__':
	logging.basicConfig(
		format='%(asctime)s - %(levelname)s - %(message)s',
		level=logging.DEBUG,
		handlers=[
			logging.StreamHandler()
		])
	loop = asyncio.get_event_loop()
	app = SimpleemergencystopPlugin()
	asyncio.ensure_future(app.run())
	loop.run_forever()