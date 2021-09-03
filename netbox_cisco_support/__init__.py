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
    min_version = '2.11.1'
    required_settings = []
    default_settings = {
        'device_ext_page': 'right'
    }


config = CiscoSupportConfig
