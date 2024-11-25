$(function() {
    function servowebcamViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];
        self.settings = parameters[1];

        self.onToggleTimelapseEnable = function() {
            console.log("current setting: " + self.settings.settings.plugins.servowebcam.enabled());
            self.settings.settings.plugins.servowebcam.enabled(!self.settings.settings.plugins.servowebcam.enabled());
            self.settings.saveData();
        };
    }

    // This is how our plugin registers itself with the application, by adding some configuration information to
    // the global variable ADDITIONAL_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        servowebcamViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request here is the order
        // in which the dependencies will be injected into your view model upon instantiation via the parameters
        // argument
        ["loginStateViewModel", "settingsViewModel"],

        // Finally, this is the list of all elements we want this view model to be bound to.
        ["#navbar_plugin_servowebcam", "#settings_plugin_servowebcam"]
    ]);
});