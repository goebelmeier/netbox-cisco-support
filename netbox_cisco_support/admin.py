from django.contrib import admin
from .models import CiscoDeviceTypeSupport, CiscoSupport


@admin.register(CiscoDeviceTypeSupport)
class CiscoSupportAdmin(admin.ModelAdmin):
    list_display = (
        "device_type",
        "end_of_sale_date",
        "end_of_sw_maintenance_releases",
        "end_of_security_vul_support_date",
        "end_of_routine_failure_analysis_date",
        "end_of_service_contract_renewal",
        "last_date_of_support",
        "end_of_svc_attach_date"
    )


@admin.register(CiscoSupport)
class CiscoSupportAdmin(admin.ModelAdmin):
    list_display = (
        "device",
        "is_covered",
        "coverage_end_date",
        "warranty_end_date"
    )
