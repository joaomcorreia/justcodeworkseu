"""
Simplified tenant models for development with SQLite
"""
from django.db import models
from django.contrib.auth.models import User


class Tenant(models.Model):
    """
    Simplified tenant model for development (without multi-tenancy)
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
    
    # Dates
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Schema name (for future migration to multi-tenant)
    schema_name = models.CharField(max_length=63, unique=True, default='public')
    
    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
    
    def __str__(self):
        return self.name


class Domain(models.Model):
    """
    Simplified domain model for development
    """
    domain = models.CharField(max_length=253, unique=True, db_index=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='domains')
    is_primary = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"
    
    def __str__(self):
        return self.domain


class TenantUser(models.Model):
    """
    Association between Users and Tenants for development
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    # Role within the tenant
    role = models.CharField(
        max_length=20,
        choices=[
            ('owner', 'Owner'),
            ('admin', 'Administrator'),
            ('editor', 'Editor'),
            ('viewer', 'Viewer'),
        ],
        default='owner'
    )
    
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('user', 'tenant')
        verbose_name = "Tenant User"
        verbose_name_plural = "Tenant Users"
    
    def __str__(self):
        return f"{self.user.username} - {self.tenant.name} ({self.role})"