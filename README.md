# NetBox Cisco Support API Plugin
[NetBox](https://github.com/netbox-community/netbox) plugin using Cisco Support APIs to gather EoX and Contract coverage information for Cisco devices.

## Compatibility
This plugin in compatible with [NetBox](https://netbox.readthedocs.org/) 3.0.3 and later.

## Installation
The plugin is available as a Python package in pypi and can be installed with pip

```
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox-cisco-support
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`:

```
# Enable installed plugins. Add the name of each plugin to the list.
PLUGINS = ['netbox_cisco_support']

# Plugins configuration settings. These settings are used by various plugins that the user may have installed.
# Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
PLUGINS_CONFIG = {
    'netbox_cisco_support': {
        'cisco_client_id': 'bar',     # Client ID of your plugin installation. Generate it inside Cisco API Console
        'cisco_client_secret': 'bazz' # Client Secret of your plugin installation. Generate it inside Cisco API Console
    }
}
```

Restart NetBox and add `netbox-cisco-support` to your `local_requirements.txt`

```
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py migrate
# sudo systemctl restart netbox
```

Sync Cisco EoX data for the first time
```
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py migrate

## Configuration
The following options are available:
* `cisco_client_id`: String - Client ID of your plugin installation. Generate it inside [Cisco API Console](https://apiconsole.cisco.com/)
* `cisco_client_secret`: String - Client Secret of your plugin installation. Generate it inside [Cisco API Console](https://apiconsole.cisco.com/)

## Screenshots
