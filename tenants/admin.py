from django.contrib import admin
from .models import Tenant, Domain, TenantUser


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'subscription_plan', 'industry', 'country', 'is_active', 'created_on']
    list_filter = ['subscription_plan', 'is_active', 'industry', 'country']
    search_fields = ['name', 'description', 'industry']
    readonly_fields = ['created_on', 'updated_on', 'schema_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Business Details', {
            'fields': ('industry', 'country', 'language')
        }),
        ('Subscription', {
            'fields': ('subscription_plan',)
        }),
        ('Technical', {
            'fields': ('schema_name',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['domain', 'tenant__name']
    
    
@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'tenant', 'role', 'is_active', 'created_on']
    list_filter = ['role', 'is_active', 'created_on']
    search_fields = ['user__username', 'user__email', 'tenant__name']
    readonly_fields = ['created_on']
