"""
Tenant models for JustCodeWorks multi-tenant architecture
"""
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import User


class Tenant(TenantMixin):
    """
    Tenant model representing each customer's isolated environment
    """
    name = models.CharField(max_length=100, help_text="Company/Organization name")
    description = models.TextField(blank=True, help_text="Brief description of the business")
    
    # Business Information
    industry = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=10, default='en')
    
    # Subscription details
    subscription_plan = models.CharField(
        max_length=20,
        choices=[
            ('trial', 'Trial'),
            ('starter', 'Starter'),
            ('professional', 'Professional'),
            ('enterprise', 'Enterprise'),
        ],
        default='trial'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Auto-create schema when saving
    auto_create_schema = True
    auto_drop_schema = True
    
    class Meta:
        db_table = 'tenants_tenant'
    
    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    Domain model for tenant subdomains
    """
    pass
    
    class Meta:
        db_table = 'tenants_domain'


class TenantUser(models.Model):
    """
    Extended user model for tenant-specific information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    # User preferences
    preferred_language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Permissions
    is_tenant_admin = models.BooleanField(default=False)
    can_manage_content = models.BooleanField(default=True)
    can_manage_blog = models.BooleanField(default=True)
    can_use_ai_assistant = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'tenant')
        db_table = 'tenants_tenantuser'
    
    def __str__(self):
        return f"{self.user.username} @ {self.tenant.name}"
