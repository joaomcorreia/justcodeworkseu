"""
Website Builder App Configuration
"""
from django.apps import AppConfig


class WebsiteBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website_builder'
    verbose_name = 'Website Builder'
    
    def ready(self):
        """
        App initialization - register signals, etc.
        """
        pass