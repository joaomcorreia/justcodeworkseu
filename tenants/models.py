from django.db import models
from django.contrib.auth.models import User
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    """
    Tenant model for website owners (simplified for development)
    """
    name = models.CharField(max_length=100)
    schema_name = models.CharField(max_length=63, unique=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Business information
    company_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Subscription info
    plan = models.CharField(
        max_length=50, 
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium'),
            ('enterprise', 'Enterprise'),
        ],
        default='free'
    )
    
    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    Domain model for tenant domains (simplified for development)
    """
    domain = models.CharField(max_length=253, unique=True, db_index=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='domains')
    is_primary = models.BooleanField(default=True)
    
    def __str__(self):
        return self.domain
