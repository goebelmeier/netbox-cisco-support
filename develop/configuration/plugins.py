# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

# Enable installed plugins. Add the name of each plugin to the list.
PLUGINS = [
    "netbox_cisco_support"
    ]

# Plugins configuration settings. These settings are used by various plugins that the user may have installed.
# Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
PLUGINS_CONFIG = {
    'netbox_cisco_support': {
        'cisco_client_id': 'bar',       # Client ID of your plugin installation. Generate it inside Cisco API Console
        'cisco_client_secret': 'bazz',  # Client Secret of your plugin installation. Generate it inside Cisco API Console
        'manufacturer': 'Cisco Systems' # Optional setting for definiing the manufacturer
    }
}
