from extras.plugins import PluginConfig
from .version import __version__


class CiscoSupportConfig(PluginConfig):
    name = 'netbox_cisco_support'
    verbose_name = 'Cisco Support APIs'
    description = 'Gathering device info using Cisco Support APIs'
    version = __version__
    author = 'Timo Reimann'
    author_email = 'timo@goebelmeier.de'
    base_url = 'cisco-support'
    min_version = '3.0.3'
    required_settings = ['cisco_client_id', 'cisco_client_secret']
    default_settings = {
        'device_ext_page': 'right'
    }


config = CiscoSupportConfig
