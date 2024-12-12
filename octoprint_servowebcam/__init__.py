# coding=utf-8
from __future__ import absolute_import
import time

import re

import math

import octoprint.plugin
import threading

import flask



class ServoWebcamdPlugin(octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.StartupPlugin,
                      octoprint.plugin.ShutdownPlugin,
                      octoprint.plugin.SimpleApiPlugin):
    def __init__(self):
        try:
            p=0
        except (ImportError, RuntimeError):
            self._hasGPIO = False

        
        
    def on_after_startup(self):
        self._logger.info("Servo Webcam! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(
            url="https://en.wikipedia.org/wiki/Hello_world",
            
            )
        
    def on_settings_initialized(self):
        self._logger.error("Error importing RPi.GPIO. OK")
                
    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
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



