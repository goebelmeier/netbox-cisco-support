# NetBox Cisco Support API Plugin
[NetbBx](https://github.com/netbox-community/netbox) plugin using Cisco Support APIs to gather EoX and Contract coverage information for Cisco devices.

## Compatibility
This plugin in compatible with [NetBox](https://netbox.readthedocs.org/) 2.11 and later.

## Installation
The plugin is available as a Python package in pypi and can be installed with pip

```
pip install netbox-cisco-support
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_cisco_support']
```
Restart NetBox and add `netbox-cisco-support` to your local_requirements.txt

## Configuration
The following options are available:
* `cisco_client_id`: String - Client ID of your plugin installation. Generate it inside [Cisco API Console](https://apiconsole.cisco.com/)
* `cisco_client_secret`: String - Client Secret of your plugin installation. Generate it inside [Cisco API Console](https://apiconsole.cisco.com/)

## Screenshots
