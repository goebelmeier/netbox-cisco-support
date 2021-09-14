from django.db import models
from netbox.models import ChangeLoggedModel
from utilities.querysets import RestrictedQuerySet


class CiscoDeviceTypeSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device_type = models.OneToOneField(
        to="dcim.DeviceType",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s Support" % self.device_type

    end_of_sale_date = models.DateField(
        help_text='Last date to order the requested product through Cisco point-of-sale mechanisms. The product is no '
                  'longer for sale after this date.',
        blank=True,
        null=True
    )

    end_of_sw_maintenance_releases = models.DateField(
        help_text='Last date that Cisco Engineering might release any software maintenance releases or bug fixes to '
                  'the software product. After this date, Cisco Engineering no longer develops, repairs, maintains, or '
                  'tests the product software.',
        blank=True,
        null=True
    )

    end_of_security_vul_support_date = models.DateField(
        help_text='Last date that Cisco Engineering may release a planned maintenance release or scheduled software '
                  'remedy for a security vulnerability issue.',
        blank=True,
        null=True
    )

    end_of_routine_failure_analysis_date = models.DateField(
        help_text='Last date Cisco might perform a routine failure analysis to determine the root cause of an '
                  'engineering-related or manufacturing-related issue.',
        blank=True,
        null=True
    )

    end_of_service_contract_renewal = models.DateField(
        help_text='Last date to extend or renew a service contract for the product. The extension or renewal period '
                  'cannot extend beyond the last date of support.',
        blank=True,
        null=True
    )

    last_date_of_support = models.DateField(
        help_text='Last date to receive service and support for the product. After this date, all support services for '
                  'the product are unavailable, and the product becomes obsolete.',
        blank=True,
        null=True
    )

    end_of_svc_attach_date = models.DateField(
        help_text='Last date to order a new service-and-support contract or add the equipment and/or software to an '
                  'existing service-and-support contract for equipment and software that is not covered by a '
                  'service-and-support contract.',
        blank=True,
        null=True
    )


class CiscoSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device = models.OneToOneField(
        to="dcim.Device",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s Support" % self.device

    coverage_end_date = models.DateField(
        help_text='End date of the contract coverage for the specifed serial number'
    )

    warranty_end_date = models.DateField(help_text='End date of the warranty for the specified serial number')

    is_covered = models.BooleanField(help_text='Indicates whether the specified serial number is covered by a service contract', default=False)
