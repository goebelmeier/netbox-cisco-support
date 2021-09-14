from develop.configuration import CISCO_CLIENT_ID, CISCO_CLIENT_SECRET
import requests
import json
import django.utils.text

from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from requests import api
from dcim.models import Manufacturer
from dcim.models import Device, DeviceType
from netbox_cisco_support.models import CiscoDeviceTypeSupport


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

    def update_device_type_eox_data(self, pid, eox_data):
        # Get the device type object for the supplied PID
        dt = DeviceType.objects.get(part_number=pid)

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
                end_of_sw_maintenance_releases_string = eox_data["EOXRecord"][0]["EndOfSaleDate"]["value"]
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
                last_date_of_support_string = eox_data["EOXRecord"][0]["EndOfSaleDate"]["value"]
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
        i = 0
        product_ids = []

        dt = self.get_device_types(manufacturer)

        for device_type in dt:

            # Skip if the device type has no valid part number. Part numbers must match the exact Cisco Base PID
            if not device_type.part_number:
                self.stdout.write(self.style.WARNING('Found device type "%s" WITHOUT Part Number - SKIPPING' % (device_type)))
                continue

            # Found Part number, append it to the list (PID collection for EoX data done)
            self.stdout.write(self.style.SUCCESS('Found device type "%s" with Part Number "%s"' % (device_type, device_type.part_number)))
            product_ids.append(device_type.part_number)

        return product_ids

    def get_serial_numbers(self, dtype):
        # trying to get all devices and its serial numbers for this device type (for contract data)
        try:
            d = Device.objects.filter(device_type=dtype)

            for device in d:

                # Skip if the device has no valid serial number.
                if not device.serial:
                    self.stdout.write(self.style.WARNING('Found device "%s" WITHOUT Serial Number - SKIPPING' % (device)))
                    continue

                # TODO - Add serial number to a list and do something with it rather than displaying.
                self.stdout.write(self.style.SUCCESS('Found device "%s" with Serial Number "%s"' % (device, device.serial)))
        except Device.DoesNotExist:
            raise CommandError('Device with device type "%s" does not exist' % dtype)
        return

    def logon(self):
        token_url = "https://cloudsso.cisco.com/as/token.oauth2"
        data = {'grant_type': 'client_credentials', 'client_id': CISCO_CLIENT_ID, 'client_secret': CISCO_CLIENT_SECRET}

        access_token_response = requests.post(token_url, data=data)
        # self.stdout.write(self.style.NOTICE(access_token_response.text))

        tokens = json.loads(access_token_response.text)
        # self.stdout.write(self.style.NOTICE("access token: %s" % tokens['access_token'])

        api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token'], 'Accept': 'application/json'}

        return api_call_headers

    def handle(self, *args, **kwargs):
        product_ids = self.get_product_ids(kwargs['manufacturer'])

        self.stdout.write(self.style.SUCCESS('Gathering data for these PIDs: ' + ', '.join(product_ids)))

        api_call_headers = self.logon()

        i = 1

        for pid in product_ids:
            # if i == 10:
            #     break

            url = 'https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/%s?responseencoding=json' % pid
            api_call_response = requests.get(url, headers=api_call_headers)
            self.stdout.write(self.style.SUCCESS('Call ' + url))

            # sanatize file name
            filename = django.utils.text.get_valid_filename('%s.json' % pid)

            # debug API answer to text file
            with open('/source/netbox_cisco_support/api-answer/%s' % filename, 'w') as outfile:
                outfile.write(api_call_response.text)

            data = json.loads(api_call_response.text)

            self.update_device_type_eox_data(pid, data)

            i += 1
