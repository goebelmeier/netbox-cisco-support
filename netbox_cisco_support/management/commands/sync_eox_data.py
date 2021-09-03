from develop.configuration import CISCO_CLIENT_ID, CISCO_CLIENT_SECRET
import requests
import json
import django.utils.text

from django.core.management.base import BaseCommand, CommandError
from requests import api
from dcim.models import Manufacturer
from dcim.models import Device, DeviceType


class Command(BaseCommand):
    help = 'Sync local devices with Cisco EoX Support API'
    client_id = 'f4tje6chnxwcp9rrbxw8z8gk'
    client_secret = 'ytDqdCMuqVhK7yEpZpKqvubQ'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--manufacturer',
            action='store_true',
            default='Cisco',
            help='Manufacturer name (default: Cisco)',
        )

    def update_device_type_eox_data(self, pid, eox_data):
        print(eox_data['EOXRecord'][0]['EOXInputValue'])

        end_of_sale_date = eox_data['EOXRecord'][0]['EndOfSaleDate']['value']
        end_of_sw_maintenance_releases = eox_data['EOXRecord'][0]['EndOfSWMaintenanceReleases']['value']
        end_of_security_vul_support_date = eox_data['EOXRecord'][0]['EndOfSecurityVulSupportDate']['value']
        end_of_routine_failure_analysis_date = eox_data['EOXRecord'][0]['EndOfRoutineFailureAnalysisDate']['value']
        end_of_service_contract_renewal = eox_data['EOXRecord'][0]['EndOfServiceContractRenewal']['value']
        last_date_of_support = eox_data['EOXRecord'][0]['LastDateOfSupport']['value']
        end_of_svc_attach_date = eox_data['EOXRecord'][0]['EndOfSvcAttachDate']['value']

        print("End Of Sale: %s" % end_of_sale_date)
        print("End Of SW Maintenance: %s" % end_of_sw_maintenance_releases)
        print("End Of Security Vuln Support: %s" % end_of_security_vul_support_date)
        print("End Of Routine Failure Analysis: %s" % end_of_routine_failure_analysis_date)
        print("End Of Service Contract Renewal: %s" % end_of_service_contract_renewal)
        print("Last Date Of Support: %s" % last_date_of_support)
        print("End Of Service Attach Date: %s" % end_of_svc_attach_date)

        return

    def get_product_ids(self, manufacturer):
        i = 0
        product_ids = []

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

        for device_type in dt:

            # Skip if the device type has no valid part number. Part numbers must match the exact Cisco Base PID
            if not device_type.part_number:
                self.stdout.write(self.style.WARNING('Found device type "%s" WITHOUT Part Number - SKIPPING' % (device_type)))
                continue

            # Found Part number, append it to the list (PID collection for EoX data done)
            self.stdout.write(self.style.SUCCESS('Found device type "%s" with Part Number "%s"' % (device_type, device_type.part_number)))
            product_ids.append(device_type.part_number)

            # trying to get all devices and its serial numbers for this device type (for contract data)
            try:
                d = Device.objects.filter(device_type=device_type)
            except Device.DoesNotExist:
                raise CommandError('Device "%s" does not exist' % d)

            for device in d:
                if not device.serial:
                    self.stdout.write(self.style.WARNING('Found device "%s" WITHOUT Serial Number - SKIPPING' % (device)))
                    continue

                self.stdout.write(self.style.SUCCESS('%s: Found device "%s" with Serial Number "%s"' % (i, device, device.serial)))
                i += 1

        return product_ids

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

        # with open('/source/netbox_cisco_support/ACS.json') as json_file:
        #     data = json.load(json_file)

        # print(json.dumps(data, sort_keys=True, indent=4))

        # finished collecting data, making API calls

        api_call_headers = self.logon()

        for pid in product_ids:
            url = 'https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/%s?responseencoding=json' % pid
            api_call_response = requests.get(url, headers=api_call_headers)
            self.stdout.write(self.style.SUCCESS('Call ' + url))

            # sanatize file name
            filename = django.utils.text.get_valid_filename('%s.json' % pid)

            # debug API answer to text file
            with open('/source/netbox_cisco_support/api-answer/%s' % filename, 'w') as outfile:
                outfile.write(api_call_response.text)

            data = json.loads(api_call_response.text)
