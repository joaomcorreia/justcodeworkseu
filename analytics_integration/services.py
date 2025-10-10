# Analytics Integration Services

import requests
import json
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from .models import AnalyticsIntegration, AnalyticsProvider, WebsiteTracking


class AnalyticsIntegrationService:
    """Service class for managing analytics integrations"""
    
    def __init__(self):
        self.google_analytics_api_url = "https://analyticsreporting.googleapis.com/v4/reports:batchGet"
        self.facebook_graph_api_url = "https://graph.facebook.com/v18.0"
    
    def setup_google_analytics(self, user, gmail_address, property_id):
        """
        Setup Google Analytics integration
        
        Args:
            user: Django User instance
            gmail_address: Gmail address linked to GA account
            property_id: Google Analytics 4 Property ID
            
        Returns:
            dict: Integration status and details
        """
        try:
            # Get or create Google Analytics provider
            ga_provider, created = AnalyticsProvider.objects.get_or_create(
                name='google_analytics',
                defaults={
                    'display_name': 'Google Analytics',
                    'api_endpoint': self.google_analytics_api_url,
                    'documentation_url': 'https://developers.google.com/analytics'
                }
            )
            
            # Create or update integration
            integration, created = AnalyticsIntegration.objects.get_or_create(
                user=user,
                provider=ga_provider,
                defaults={
                    'google_email': gmail_address,
                    'property_id': property_id,
                    'measurement_id': property_id,  # GA4 uses same ID
                    'status': 'pending'
                }
            )
            
            if not created:
                # Update existing integration
                integration.google_email = gmail_address
                integration.property_id = property_id
                integration.measurement_id = property_id
                integration.status = 'pending'
                integration.save()
            
            # Verify the integration (in real implementation, this would call GA API)
            verification_result = self._verify_google_analytics_access(gmail_address, property_id)
            
            if verification_result['success']:
                integration.status = 'connected'
                integration.last_sync = datetime.now()
                integration.sync_error = None
            else:
                integration.status = 'error'
                integration.sync_error = verification_result['error']
            
            integration.save()
            
            # Auto-inject tracking code to all user websites
            if integration.auto_inject:
                self._inject_tracking_codes(user, integration)
            
            return {
                'success': True,
                'integration_id': integration.id,
                'status': integration.status,
                'tracking_code': integration.tracking_code,
                'message': f'Successfully connected Google Analytics for {gmail_address}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to setup Google Analytics: {str(e)}'
            }
    
    def setup_facebook_pixel(self, user, facebook_email, pixel_id):
        """
        Setup Facebook Pixel integration
        
        Args:
            user: Django User instance
            facebook_email: Facebook account email
            pixel_id: Facebook Pixel ID
            
        Returns:
            dict: Integration status and details
        """
        try:
            # Get or create Facebook Pixel provider
            fb_provider, created = AnalyticsProvider.objects.get_or_create(
                name='facebook_pixel',
                defaults={
                    'display_name': 'Facebook Pixel',
                    'api_endpoint': self.facebook_graph_api_url,
                    'documentation_url': 'https://developers.facebook.com/docs/facebook-pixel'
                }
            )
            
            # Create or update integration
            integration, created = AnalyticsIntegration.objects.get_or_create(
                user=user,
                provider=fb_provider,
                defaults={
                    'facebook_email': facebook_email,
                    'pixel_id': pixel_id,
                    'status': 'pending'
                }
            )
            
            if not created:
                integration.facebook_email = facebook_email
                integration.pixel_id = pixel_id
                integration.status = 'pending'
                integration.save()
            
            # Verify the pixel (in real implementation, this would call FB API)
            verification_result = self._verify_facebook_pixel_access(facebook_email, pixel_id)
            
            if verification_result['success']:
                integration.status = 'connected'
                integration.last_sync = datetime.now()
                integration.sync_error = None
            else:
                integration.status = 'error'
                integration.sync_error = verification_result['error']
            
            integration.save()
            
            # Auto-inject tracking code
            if integration.auto_inject:
                self._inject_tracking_codes(user, integration)
            
            return {
                'success': True,
                'integration_id': integration.id,
                'status': integration.status,
                'tracking_code': integration.tracking_code,
                'message': f'Successfully connected Facebook Pixel {pixel_id}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to setup Facebook Pixel: {str(e)}'
            }
    
    def _verify_google_analytics_access(self, gmail_address, property_id):
        """
        Verify Google Analytics access (mock implementation)
        In production, this would use Google Analytics Reporting API
        """
        # Mock verification - in reality, you would:
        # 1. Use OAuth2 to authenticate with the Gmail account
        # 2. Call GA API to verify property access
        # 3. Check if property exists and user has access
        
        if '@gmail.com' in gmail_address and property_id.startswith('G-'):
            return {'success': True}
        else:
            return {
                'success': False, 
                'error': 'Invalid Gmail address or Property ID format'
            }
    
    def _verify_facebook_pixel_access(self, facebook_email, pixel_id):
        """
        Verify Facebook Pixel access (mock implementation)
        In production, this would use Facebook Graph API
        """
        # Mock verification - in reality, you would:
        # 1. Use Facebook Login API to authenticate
        # 2. Call Graph API to verify pixel ownership
        # 3. Check pixel status and permissions
        
        if '@' in facebook_email and pixel_id.isdigit() and len(pixel_id) >= 15:
            return {'success': True}
        else:
            return {
                'success': False,
                'error': 'Invalid Facebook email or Pixel ID format'
            }
    
    def _inject_tracking_codes(self, user, integration):
        """
        Automatically inject tracking codes into user's websites
        """
        try:
            # Get all websites for the user
            websites = WebsiteTracking.objects.filter(user=user, auto_inject_enabled=True)
            
            for website in websites:
                # In a real implementation, you would:
                # 1. Access the website's template files
                # 2. Inject the tracking code in the <head> section
                # 3. Update database records
                # 4. Possibly trigger a website rebuild/deployment
                
                # For now, just create/update the integration status
                from .models import WebsiteIntegrationStatus
                status, created = WebsiteIntegrationStatus.objects.get_or_create(
                    website=website,
                    integration=integration,
                    defaults={'is_active': True}
                )
                
                if not created:
                    status.is_active = True
                    status.save()
            
            return True
            
        except Exception as e:
            print(f"Error injecting tracking codes: {e}")
            return False
    
    def get_user_integrations(self, user):
        """
        Get all analytics integrations for a user
        """
        integrations = AnalyticsIntegration.objects.filter(user=user).select_related('provider')
        
        result = {}
        for integration in integrations:
            result[integration.provider.name] = {
                'status': integration.status,
                'last_sync': integration.last_sync,
                'tracking_code': integration.tracking_code,
                'auto_inject': integration.auto_inject,
                'config': {
                    'google_email': integration.google_email,
                    'property_id': integration.property_id,
                    'facebook_email': integration.facebook_email,
                    'pixel_id': integration.pixel_id,
                    'bing_email': integration.bing_email,
                    'uet_tag_id': integration.uet_tag_id,
                }
            }
        
        return result
    
    def register_website(self, user, website_url, website_name):
        """
        Register a new website for analytics tracking
        """
        try:
            website, created = WebsiteTracking.objects.get_or_create(
                user=user,
                website_url=website_url,
                defaults={
                    'website_name': website_name,
                    'auto_inject_enabled': True
                }
            )
            
            # Auto-inject existing integrations
            user_integrations = AnalyticsIntegration.objects.filter(
                user=user, 
                status='connected',
                auto_inject=True
            )
            
            for integration in user_integrations:
                self._inject_tracking_codes(user, integration)
            
            return {
                'success': True,
                'website_id': website.id,
                'message': f'Website {website_name} registered successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to register website: {str(e)}'
            }
    
    def generate_combined_tracking_code(self, user, website_url=None):
        """
        Generate combined tracking code for all active integrations
        """
        integrations = AnalyticsIntegration.objects.filter(
            user=user,
            status='connected'
        ).select_related('provider')
        
        combined_code = "<!-- JustCodeWorks Analytics Integration -->\n"
        
        for integration in integrations:
            if integration.tracking_code:
                combined_code += f"\n{integration.tracking_code}\n"
        
        combined_code += "\n<!-- End JustCodeWorks Analytics Integration -->\n"
        
        return combined_code


# Service instance
analytics_service = AnalyticsIntegrationService()