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
            global GPIO
            import RPi.GPIO as GPIO
            self._hasGPIO = True
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(12, GPIO.OUT)
            GPIO.setup(13, GPIO.OUT)
            self.pX = GPIO.PWM(12, 50) # GPIO 17 for PWM with 50Hz
            self.pX.start(2.5) # Initialization
            self.pY = GPIO.PWM(12, 50) # GPIO 17 for PWM with 50Hz
            self.pY.start(2.5) # Initialization
        except (ImportError, RuntimeError):
            self._hasGPIO = False

        
        
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



