# coding=utf-8
from __future__ import absolute_import, print_function
from octoprint.server import user_permission

import octoprint.plugin
import flask
import RPi.GPIO as GPIO


class GpioControlPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.RestartNeedingPlugin,
):
    mode = None

    def on_startup(self, *args, **kwargs):
        GPIO.setwarnings(False)

        self.mode = GPIO.getmode()

        if self.mode is None:
            self.mode = GPIO.BCM
            GPIO.setmode(self.mode)

        self._logger.info("Detected GPIO mode: {}".format(self.mode))

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=True),
            dict(
                type="sidebar",
                custom_bindings=True,
                template="gpiocontrol_sidebar.jinja2",
                icon="map-signs",
            ),
        ]

    def get_assets(self):
        return dict(
            js=["js/gpiocontrol.js", "js/fontawesome-iconpicker.min.js"],
            css=["css/gpiocontrol.css", "css/fontawesome-iconpicker.min.css"],
        )

    def get_settings_defaults(self):
        return dict(gpio_configurations=[])

    def on_settings_save(self, data):
        for configuration in self._settings.get(["gpio_configurations"]):
            self._logger.info(
                "Cleaned GPIO{}: {},{} ({})".format(
                    configuration["pin"],
                    configuration["active_mode"],
                    configuration["default_state"],
                    configuration["name"],
                )
            )

            pin = self.get_pin_number(int(configuration["pin"]))

            if pin > 0:
                GPIO.cleanup(pin)

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        for configuration in self._settings.get(["gpio_configurations"]):
            self._logger.info(
                "Reconfigured GPIO{}: {},{} ({})".format(
                    configuration["pin"],
                    configuration["active_mode"],
                    configuration["default_state"],
                    configuration["name"],
                )
            )

            pin = self.get_pin_number(int(configuration["pin"]))

            if pin > 0:
                GPIO.setup(pin, GPIO.OUT)

                if configuration["active_mode"] == "active_low":
                    if configuration["default_state"] == "default_on":
                        GPIO.output(pin, GPIO.LOW)
                    elif configuration["default_state"] == "default_off":
                        GPIO.output(pin, GPIO.HIGH)
                elif configuration["active_mode"] == "active_high":
                    if configuration["default_state"] == "default_on":
                        GPIO.output(pin, GPIO.HIGH)
                    elif configuration["default_state"] == "default_off":
                        GPIO.output(pin, GPIO.LOW)

    def on_after_startup(self):
        for configuration in self._settings.get(["gpio_configurations"]):
            self._logger.info(
                "Configured GPIO{}: {},{} ({})".format(
                    configuration["pin"],
                    configuration["active_mode"],
                    configuration["default_state"],
                    configuration["name"],
                )
            )

            pin = self.get_pin_number(int(configuration["pin"]))

            if pin != -1:
                GPIO.setup(pin, GPIO.OUT)

                if configuration["active_mode"] == "active_low":
                    if configuration["default_state"] == "default_on":
                        GPIO.output(pin, GPIO.LOW)
                    elif configuration["default_state"] == "default_off":
                        GPIO.output(pin, GPIO.HIGH)
                elif configuration["active_mode"] == "active_high":
                    if configuration["default_state"] == "default_on":
                        GPIO.output(pin, GPIO.HIGH)
                    elif configuration["default_state"] == "default_off":
                        GPIO.output(pin, GPIO.LOW)

    def get_api_commands(self):
        return dict(turnGpioOn=["id"], turnGpioOff=["id"], getGpioState=["id"])

    def on_api_command(self, command, data):
        if not user_permission.can():
            return flask.make_response("Insufficient rights", 403)

        configuration = self._settings.get(["gpio_configurations"])[int(data["id"])]
        pin = self.get_pin_number(int(configuration["pin"]))

        if command == "getGpioState":
            if pin < 0:
                return flask.jsonify("")
            elif configuration["active_mode"] == "active_low":
                return flask.jsonify("off" if GPIO.input(pin) else "on")
            elif configuration["active_mode"] == "active_high":
                return flask.jsonify("on" if GPIO.input(pin) else "off")
        elif command == "turnGpioOn":
            if pin > 0:
                self._logger.info("Turned on GPIO{}".format(configuration["pin"]))

                if configuration["active_mode"] == "active_low":
                    GPIO.output(pin, GPIO.LOW)
                elif configuration["active_mode"] == "active_high":
                    GPIO.output(pin, GPIO.HIGH)
        elif command == "turnGpioOff":
            if pin > 0:
                self._logger.info("Turned off GPIO{}".format(configuration["pin"]))

                if configuration["active_mode"] == "active_low":
                    GPIO.output(pin, GPIO.HIGH)
                elif configuration["active_mode"] == "active_high":
                    GPIO.output(pin, GPIO.LOW)

    def on_api_get(self, request):
        states = []

        for configuration in self._settings.get(["gpio_configurations"]):
            pin = self.get_pin_number(int(configuration["pin"]))

            if pin < 0:
                states.append("")
            elif configuration["active_mode"] == "active_low":
                states.append("off" if GPIO.input(pin) else "on")
            elif configuration["active_mode"] == "active_high":
                states.append("on" if GPIO.input(pin) else "off")

        return flask.jsonify(states)

    def get_update_information(self):
        return dict(
            gpiocontrol=dict(
                displayName="GPIO Control",
                displayVersion=self._plugin_version,
                type="github_release",
                user="catgiggle",
                repo="OctoPrint-GpioControl",
                current=self._plugin_version,
                stable_branch=dict(
                    name="Stable",
                    branch="master",
                    comittish=["master"],
                ),
                prerelease_branches=[
                    dict(
                        name="Prerelease",
                        branch="development",
                        comittish=["development", "master"],
                    )
                ],
                pip="https://github.com/catgiggle/OctoPrint-GpioControl/archive/{target_version}.zip",
            )
        )

    PIN_MAPPINGS = [-1, -1, 3, 5, 7, 29, 31, 26, 24, 21, 19, 23, 32, 33, 8, 10, 36, 11, 12, 35, 38, 40, 15, 16, 18, 22, 37, 13]

    def get_pin_number(self, pin):
        if 2 <= pin <= 27:
            if self.mode == GPIO.BCM:
                return pin

            if self.mode == GPIO.BOARD:
                return self.PIN_MAPPINGS[pin]

        return -1


__plugin_name__ = "GPIO Control"
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = GpioControlPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
