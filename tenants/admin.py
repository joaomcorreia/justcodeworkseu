from django.contrib import admin
from .models import Tenant, Domain


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'schema_name', 'company_name', 'plan', 'is_active', 'created_on']
    list_filter = ['plan', 'is_active', 'created_on']
    search_fields = ['name', 'company_name', 'contact_email']
    readonly_fields = ['created_on']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['domain', 'tenant__name']
