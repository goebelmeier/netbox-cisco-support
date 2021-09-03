from datetime import datetime

from django.shortcuts import get_object_or_404

from extras.plugins import PluginTemplateExtension
from .models import CiscoDeviceTypeSupport, CiscoSupport


class CiscoDeviceTypeSupportInformation(PluginTemplateExtension):
    model = 'dcim.devicetype'

    def right_page(self):
        try:
            cisco_device_type_support = CiscoDeviceTypeSupport.objects.get(device_type=self.context['object'])
        except CiscoDeviceTypeSupport.DoesNotExist:
            print("No Cisco Device Type Support Entry found")
            cisco_device_type_support = None

        return self.render('netbox_cisco_support/cisco_support_device_type.html', {
            'cisco_device_type_support': cisco_device_type_support
        })


class CiscoDeviceSupportInformation(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        try:
            cisco_device_support = CiscoSupport.objects.get(device=self.context['object'])
        except CiscoSupport.DoesNotExist:
            print("No Cisco Device Support Entry found")
            cisco_device_support = None

        try:
            cisco_device_type_support = CiscoDeviceTypeSupport.objects.get(device_type=self.context['object'].device_type)
        except CiscoDeviceTypeSupport.DoesNotExist:
            print("No Cisco Device Type Support Entry found")
            cisco_device_type_support = None

        return self.render('netbox_cisco_support/cisco_support_device.html', {
            'cisco_device_support': cisco_device_support,
            'cisco_device_type_support': cisco_device_type_support
        })


template_extensions = [CiscoDeviceTypeSupportInformation, CiscoDeviceSupportInformation]
