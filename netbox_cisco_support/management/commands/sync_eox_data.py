import requests
import json
import django.utils.text

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned
from datetime import datetime
from requests import api
from dcim.models import Manufacturer
from dcim.models import Device, DeviceType
from netbox_cisco_support.models import CiscoDeviceTypeSupport, CiscoSupport


class Command(BaseCommand):
    help = 'Sync local devices with Cisco EoX Support API'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--manufacturer',
            action='store_true',
            default='Cisco',
            help='Manufacturer name (default: Cisco)',
        )

    # Updates a single device with current EoX Data
    def update_device_eox_data(self, device):
        self.stdout.write(self.style.SUCCESS("Trying to update device %s" % device['sr_no']))

        # Get the device object from NetBox
        try:
            d = Device.objects.get(serial=device['sr_no'])
        except MultipleObjectsReturned:

            # Error if netbox has multiple SN's and skip updating
            self.stdout.write(self.style.NOTICE("ERROR: Multiple objects exist within Netbox with Serial Number " + device['sr_no']))
            return

        # Check if a CiscoSupport object already exists, if not, create a new one
        try:
            ds = CiscoSupport.objects.get(device=d)
        except CiscoSupport.DoesNotExist:
            ds = CiscoSupport(device=d)

        # Control variable to only save the object if something has changed
        value_changed = False

        # A "YES" string is not quite boolean :-)
        covered = True if device['is_covered'] == "YES" else False

        self.stdout.write(self.style.SUCCESS("%s - covered: %s" % (device['sr_no'], covered)))

        # Check if the Coverage in the CiscoSupport object equals API answer. If not, change it
        if ds.is_covered != covered:
            ds.is_covered = covered
            value_changed = True

        try:
            if not device['warranty_end_date']:
                self.stdout.write(self.style.NOTICE("%s has no warranty_end_date" % device['sr_no']))
            else:
                warranty_end_date_string = device['warranty_end_date']
                warranty_end_date = datetime.strptime(warranty_end_date_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - warranty_end_date: %s" % (device['sr_no'], warranty_end_date)))

                if ds.warranty_end_date != warranty_end_date:
                    ds.warranty_end_date = warranty_end_date
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no warranty_end_date" % device['sr_no']))

        try:
            if not device['covered_product_line_end_date']:
                self.stdout.write(self.style.NOTICE("%s has no covered_product_line_end_date" % device['sr_no']))
            else:
                coverage_end_date_string = device['covered_product_line_end_date']
                coverage_end_date = datetime.strptime(coverage_end_date_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - coverage_end_date: %s" % (device['sr_no'], coverage_end_date)))

                if ds.coverage_end_date != coverage_end_date:
                    ds.coverage_end_date = coverage_end_date
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no coverage_end_date" % device['sr_no']))

        if value_changed:
            ds.save()

        return

    def update_device_type_eox_data(self, pid, eox_data):

        try:
            # Get the device type object for the supplied PID
            dt = DeviceType.objects.get(part_number=pid)

        except MultipleObjectsReturned:

            # Error if netbox has multiple PN's
            self.stdout.write(self.style.NOTICE("ERROR: Multiple objects exist within Netbox with Part Number " + pid))
            return

        # Check if CiscoDeviceTypeSupport record already exists
        try:
            dts = CiscoDeviceTypeSupport.objects.get(device_type=dt)
        # If not, create a new one for this Device Type
        except CiscoDeviceTypeSupport.DoesNotExist:
            dts = CiscoDeviceTypeSupport(device_type=dt)

        # Only save if something has changed
        value_changed = False

        try:
            # Check if JSON contains EndOfSaleDate with value field
            if not eox_data["EOXRecord"][0]["EndOfSaleDate"]["value"]:
                self.stdout.write(self.style.NOTICE("%s has no end_of_sale_date" % pid))
            else:
                end_of_sale_date_string = eox_data["EOXRecord"][0]["EndOfSaleDate"]["value"]
                # Cast this value to datetime.date object
                end_of_sale_date = datetime.strptime(end_of_sale_date_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - end_of_sale_date: %s" % (pid, end_of_sale_date)))

                # Check if CiscoDeviceTypeSupport end_of_sale_date differs from JSON EndOfSaleDate, update if true
                if dts.end_of_sale_date != end_of_sale_date:
                    dts.end_of_sale_date = end_of_sale_date
                    value_changed = True

        # Do nothing when JSON field does not exist
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no end_of_sale_date" % pid))

        try:
            if not eox_data["EOXRecord"][0]["EndOfSWMaintenanceReleases"]["value"]:
                self.stdout.write(self.style.NOTICE("%s has no end_of_sw_maintenance_releases" % pid))
            else:
                end_of_sw_maintenance_releases_string = eox_data["EOXRecord"][0]["EndOfSWMaintenanceReleases"]["value"]
                end_of_sw_maintenance_releases = datetime.strptime(end_of_sw_maintenance_releases_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - end_of_sw_maintenance_releases: %s" % (pid, end_of_sw_maintenance_releases)))

                if dts.end_of_sw_maintenance_releases != end_of_sw_maintenance_releases:
                    dts.end_of_sw_maintenance_releases = end_of_sw_maintenance_releases
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no end_of_sw_maintenance_releases" % pid))

        try:
            if not eox_data["EOXRecord"][0]["EndOfSecurityVulSupportDate"]["value"]:
                self.stdout.write(self.style.NOTICE("%s has no end_of_security_vul_support_date" % pid))
            else:
                end_of_security_vul_support_date_string = eox_data["EOXRecord"][0]["EndOfSecurityVulSupportDate"]["value"]
                end_of_security_vul_support_date = datetime.strptime(end_of_security_vul_support_date_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - end_of_security_vul_support_date: %s" % (pid, end_of_security_vul_support_date)))

                if dts.end_of_security_vul_support_date != end_of_security_vul_support_date:
                    dts.end_of_security_vul_support_date = end_of_security_vul_support_date
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no end_of_security_vul_support_date" % pid))

        try:
            if not eox_data["EOXRecord"][0]["EndOfRoutineFailureAnalysisDate"]["value"]:
                self.stdout.write(self.style.NOTICE("%s has no end_of_routine_failure_analysis_date" % pid))
            else:
                end_of_routine_failure_analysis_date_string = eox_data["EOXRecord"][0]["EndOfRoutineFailureAnalysisDate"]["value"]
                end_of_routine_failure_analysis_date = datetime.strptime(end_of_routine_failure_analysis_date_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - end_of_routine_failure_analysis_date: %s" % (pid, end_of_routine_failure_analysis_date)))

                if dts.end_of_routine_failure_analysis_date != end_of_routine_failure_analysis_date:
                    dts.end_of_routine_failure_analysis_date = end_of_routine_failure_analysis_date
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no end_of_routine_failure_analysis_date" % pid))

        try:
            if not eox_data["EOXRecord"][0]["EndOfServiceContractRenewal"]["value"]:
                self.stdout.write(self.style.NOTICE("%s has no end_of_service_contract_renewal" % pid))
            else:
                end_of_service_contract_renewal_string = eox_data["EOXRecord"][0]["EndOfServiceContractRenewal"]["value"]
                end_of_service_contract_renewal = datetime.strptime(end_of_service_contract_renewal_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - end_of_service_contract_renewal: %s" % (pid, end_of_service_contract_renewal)))

                if dts.end_of_service_contract_renewal != end_of_service_contract_renewal:
                    dts.end_of_service_contract_renewal = end_of_service_contract_renewal
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no end_of_service_contract_renewal" % pid))

        try:
            if not eox_data["EOXRecord"][0]["LastDateOfSupport"]["value"]:
                self.stdout.write(self.style.NOTICE("%s has no last_date_of_support" % pid))
            else:
                last_date_of_support_string = eox_data["EOXRecord"][0]["LastDateOfSupport"]["value"]
                last_date_of_support = datetime.strptime(last_date_of_support_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - last_date_of_support: %s" % (pid, last_date_of_support)))

                if dts.last_date_of_support != last_date_of_support:
                    dts.last_date_of_support = last_date_of_support
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no last_date_of_support" % pid))

        try:
            if not eox_data["EOXRecord"][0]["EndOfSvcAttachDate"]["value"]:
                self.stdout.write(self.style.NOTICE("%s has no end_of_svc_attach_date" % pid))
            else:
                end_of_svc_attach_date_string = eox_data["EOXRecord"][0]["EndOfSvcAttachDate"]["value"]
                end_of_svc_attach_date = datetime.strptime(end_of_svc_attach_date_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS("%s - end_of_svc_attach_date: %s" % (pid, end_of_svc_attach_date)))

                if dts.end_of_svc_attach_date != end_of_svc_attach_date:
                    dts.end_of_svc_attach_date = end_of_svc_attach_date
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE("%s has no end_of_svc_attach_date" % pid))

        if value_changed:
            dts.save()

        return

    def get_device_types(self, manufacturer):
        # trying to get the right manufacturer for this plugin
        try:
            m = Manufacturer.objects.get(name=manufacturer)
        except Manufacturer.DoesNotExist:
            raise CommandError('Manufacturer "%s" does not exist' % manufacturer)

        self.stdout.write(self.style.SUCCESS('Found manufacturer "%s"' % m))

        # trying to get all device types and it's base PIDs associated with this manufacturer
        try:
            dt = DeviceType.objects.filter(manufacturer=m)
        except DeviceType.DoesNotExist:
            raise CommandError('Manufacturer "%s" has no Device Types' % m)

        return dt

    def get_product_ids(self, manufacturer):
        product_ids = []

        # Get all device types for supplied manufacturer
        dt = self.get_device_types(manufacturer)

        # Iterate all this device types
        for device_type in dt:

            # Skip if the device type has no valid part number. Part numbers must match the exact Cisco Base PID
            if not device_type.part_number:
                self.stdout.write(self.style.WARNING('Found device type "%s" WITHOUT Part Number - SKIPPING' % (device_type)))
                continue

            # Found Part number, append it to the list (PID collection for EoX data done)
            self.stdout.write(self.style.SUCCESS('Found device type "%s" with Part Number "%s"' % (device_type, device_type.part_number)))
            product_ids.append(device_type.part_number)

        return product_ids

    def get_serial_numbers(self, manufacturer):
        serial_numbers = []

        # Get all device types for supplied manufacturer
        dt = self.get_device_types(manufacturer)

        # Iterate all this device types
        for device_type in dt:
            # trying to get all devices and its serial numbers for this device type (for contract data)
            try:
                d = Device.objects.filter(device_type=device_type)

                for device in d:
                    # Skip if the device has no valid serial number.
                    if not device.serial:
                        self.stdout.write(self.style.WARNING('Found device "%s" WITHOUT Serial Number - SKIPPING' % (device)))
                        continue

                    # TODO - Add serial number to a list and do something with it rather than displaying.
                    self.stdout.write(self.style.SUCCESS('Found device "%s" with Serial Number "%s"' % (device, device.serial)))
                    serial_numbers.append(device.serial)
            except Device.DoesNotExist:
                raise CommandError('Device with device type "%s" does not exist' % dt)

        return serial_numbers

    def logon(self):
        PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_cisco_support", dict())
        CISCO_CLIENT_ID = PLUGIN_SETTINGS.get("cisco_client_id", "")
        CISCO_CLIENT_SECRET = PLUGIN_SETTINGS.get("cisco_client_secret", "")

        token_url = "https://id.cisco.com/oauth2/default/v1/token"
        data = {'grant_type': 'client_credentials', 'client_id': CISCO_CLIENT_ID, 'client_secret': CISCO_CLIENT_SECRET}

        access_token_response = requests.post(token_url, data=data)

        tokens = json.loads(access_token_response.text)

        api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token'], 'Accept': 'application/json'}

        return api_call_headers

    # Main entry point for the sync_eox_data command of manage.py
    def handle(self, *args, **kwargs):
        PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_cisco_support", dict())
        MANUFACTURER = PLUGIN_SETTINGS.get("manufacturer", "Cisco")

        # Logon one time and gather the required API key
        api_call_headers = self.logon()

        # Step 1: Get all PIDs for all Device Types of that particular manufacturer
        product_ids = self.get_product_ids(MANUFACTURER)
        self.stdout.write(self.style.SUCCESS('Gathering data for these PIDs: ' + ', '.join(product_ids)))

        i = 1
        for pid in product_ids:
            url = 'https://apix.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/%s?responseencoding=json' % pid
            api_call_response = requests.get(url, headers=api_call_headers)
            self.stdout.write(self.style.SUCCESS('Call ' + url))

            # sanatize file name
            filename = django.utils.text.get_valid_filename('%s.json' % pid)

            # debug API answer to text file
            # with open('/source/netbox_cisco_support/api-answer/%s' % filename, 'w') as outfile:
            #    outfile.write(api_call_response.text)

            # Validate response from Cisco 
            if api_call_response.status_code == 200:

                # Deserialize JSON API Response into Python object "data"
                data = json.loads(api_call_response.text)

                # Call our Device Type Update method for that particular PID
                self.update_device_type_eox_data(pid, data)

                i += 1

            else:

                # Show an error
                self.stdout.write(self.style.ERROR('API Error: ' + api_call_response.text))


        # Step 2: Get all Serial Numbers for all Devices of that particular manufacturer
        serial_numbers = self.get_serial_numbers(MANUFACTURER)
        self.stdout.write(self.style.SUCCESS('Gathering data for these Serial Numbers: ' + ', '.join(serial_numbers)))

        i = 1
        while serial_numbers:
            # Pop the first items_to_fetch items of serial_numbers into current_slice and then delete them from serial
            # numbers. We want to pass x items to the API each time we call it
            items_to_fetch = 10
            current_slice = serial_numbers[:items_to_fetch]
            serial_numbers[:items_to_fetch] = []

            url = 'https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s' % ','.join(current_slice)
            api_call_response = requests.get(url, headers=api_call_headers)
            self.stdout.write(self.style.SUCCESS('Call ' + url))

            # Validate response from Cisco 
            if api_call_response.status_code == 200:

                # Deserialize JSON API Response into Python object "data"
                data = json.loads(api_call_response.text)

                # Iterate through all serial numbers included in the API response
                for device in data['serial_numbers']:

                    # Call our Device Update method for that particular Device
                    self.update_device_eox_data(device)

                i += 1
            
            else:

                # Show an error
                self.stdout.write(self.style.ERROR('API Error: ' + api_call_response.text))
