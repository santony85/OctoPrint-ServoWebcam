##############################################
#                            V6.1.1
# the settigns all work
#
# added timout and reset
# added job folders
# added file numbering
# added timelapse FFmpeg file creation and output
# added copy timelpase video to main folder
# added octopring.log configs output
# added check to use any "~" folder other then "pi"
# added comments
#
#also added to settings
# * Img for the printer delay
# * button "Make an LDR cable" with png of cable
# * "i" buttons for more info
#
#also added to navbar
# * servowebcam On/OFF button <----------- WORKING
# 
##############################################
import os
import flask
from octoprint.plugin import StartupPlugin, TemplatePlugin, SettingsPlugin, AssetPlugin, SimpleApiPlugin
import RPi.GPIO as GPIO
import threading
import logging
import time
import requests
import subprocess
import shutil

from gpiozero import Servo




#### Set up logging
log = logging.getLogger("octoprint.plugins.servo_webcam")

#### Plugin class definition
class ServoWebcamPlugin(StartupPlugin, TemplatePlugin, SettingsPlugin, AssetPlugin, SimpleApiPlugin):
    def __init__(self):
        super().__init__()
        # Initialize plugin state variables
        self.enabled = False  # Track whether the plugin is enabled or disabled

    #### Define default settings for the plugin
    def get_settings_defaults(self):
        return dict(
            gpio_pin=21,
            photo_delay=PHOTO_DELAY,
            snapshot_folder=os.path.expanduser("~/timelapse"),  # Dynamic folder path
            enabled=False,  # Plugin disabled by default
            timeout=INACTIVE_TIMEOUT,
            avi_folder=os.path.expanduser("~/timelapse")  # Default path for AVI files
        )

    #### Method called after the plugin has been initialized
     #### Method called after the plugin has been initialized
    def on_after_startup(self):
        # Retrieve enabled state from settings and set up GPIO if enabled
        self.enabled = self._settings.get_boolean(["enabled"])
        if self.enabled:
            self._setup_gpio()

        # Log plugin configuration settings
        gpio_pin = self._settings.get_int(["gpio_pin"])
        photo_delay = self._settings.get_int(["photo_delay"])
        snapshot_folder = self._settings.get(["snapshot_folder"])
        timeout = self._settings.get_int(["timeout"])
        avi_folder = self._settings.get(["avi_folder"])
    ########### BOOT LOG'S #######################
        log.info(f"servowebcam Config - GPIO Pin retrieved from settings: {gpio_pin}")
        log.info(f"servowebcam Config - Photo Delay retrieved from settings: {photo_delay}")
        log.info(f"servowebcam Config - Store Folder retrieved from settings: {snapshot_folder}")
        log.info(f"servowebcam Config - Timeout value from settings: {timeout}")
        log.info(f"servowebcam Config - AVI Folder retrieved from settings: {avi_folder}")

    #### Method called when settings are saved
    def on_settings_save(self, data):
        old_enabled = self.enabled
        # Call parent method to handle settings save
        SettingsPlugin.on_settings_save(self, data)
        # Check if enabled state has changed
        new_enabled = self._settings.get_boolean(["enabled"])
        if old_enabled != new_enabled:
            self.enabled = new_enabled
            # Set up or clean up GPIO based on new enabled state
            if self.enabled:
                self._setup_gpio()
            else:
                self._cleanup()


    ##### Method to provide configuration for templates
    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=True, template="servowebcam_settings.jinja2"),
            dict(type="navbar", custom_bindings=True, template="servowebcam_navbar.jinja2"),
            dict(type="tab", custom_bindings=True, template="servowebcam_tab.jinja2", data_bind="allowBind: true")
        ]

    ##### Method to provide assets (JavaScript files)
    def get_assets(self):
        return dict(
            js=["js/servowebcam.js"]
        )

#### Plugin metadata
__plugin_name__ = "Servo Webcam"
__plugin_pythoncompat__ = ">=3.7,<4"

#### Plugin load function
def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ServoWebcamPlugin()
