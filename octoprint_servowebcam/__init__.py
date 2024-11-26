# coding=utf-8
from __future__ import absolute_import
import time

import re

import math

import octoprint.plugin
import threading

import RPi.GPIO as GPIO

import flask



class ServoWebcamdPlugin(octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.StartupPlugin,
                      octoprint.plugin.ShutdownPlugin,
                      octoprint.plugin.SimpleApiPlugin):
    def __init__(self):
        ppp = 0

        
        
    def on_after_startup(self):
        self._logger.info("Servo Webcam! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(url="https://en.wikipedia.org/wiki/Hello_world")

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="generic", template="servowebcam.jinja2", custom_bindings=True),
            dict(type="settings", custom_bindings=False)
        ]

    def get_assets(self):
        return dict(
            js=["js/servowebcam.js"],
        )
    def on_api_get(self, request):
       return flask.jsonify(foo="bar")
   
__plugin_name__ = "Servo Webcam"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = ServoWebcamdPlugin()

""""
def __plugin_load__():
	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.process_gcode,
		"octoprint.comm.protocol.gcode.sending": __plugin_implementation__.read_gcode
	}
"""

