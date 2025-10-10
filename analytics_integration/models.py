# Analytics Integration Models

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class AnalyticsProvider(models.Model):
    """Analytics provider configuration"""
    PROVIDER_CHOICES = [
        ('google_analytics', 'Google Analytics'),
        ('facebook_pixel', 'Facebook Pixel'),
        ('bing_ads', 'Bing Ads'),
        ('google_tag_manager', 'Google Tag Manager'),
    ]
    
    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    api_endpoint = models.URLField(blank=True, null=True)
    documentation_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.display_name


class AnalyticsIntegration(models.Model):
    """User's analytics integration settings"""
    STATUS_CHOICES = [
        ('not_connected', 'Not Connected'),
        ('pending', 'Pending'),
        ('connected', 'Connected'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(AnalyticsProvider, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_connected')
    
    # Google Analytics fields
    google_email = models.EmailField(blank=True, null=True)
    property_id = models.CharField(max_length=50, blank=True, null=True)
    measurement_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Facebook Pixel fields
    facebook_email = models.EmailField(blank=True, null=True)
    pixel_id = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        validators=[RegexValidator(regex=r'^\d{15,16}$', message='Enter a valid Facebook Pixel ID')]
    )
    
    # Bing Ads fields
    bing_email = models.EmailField(blank=True, null=True)
    uet_tag_id = models.CharField(max_length=20, blank=True, null=True)
    
    # Configuration settings
    auto_inject = models.BooleanField(default=True)
    track_conversions = models.BooleanField(default=True)
    track_events = models.BooleanField(default=True)
    track_ecommerce = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sync = models.DateTimeField(blank=True, null=True)
    sync_error = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['user', 'provider']
    
    def __str__(self):
        return f"{self.user.username} - {self.provider.display_name} ({self.status})"
    
    @property
    def tracking_code(self):
        """Generate tracking code based on provider"""
        if self.provider.name == 'google_analytics' and self.measurement_id:
            return f'''
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={self.measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{self.measurement_id}');
</script>'''
        
        elif self.provider.name == 'facebook_pixel' and self.pixel_id:
            return f'''
<!-- Facebook Pixel -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{self.pixel_id}');
fbq('track', 'PageView');
</script>
<noscript>
<img height="1" width="1" style="display:none"
     src="https://www.facebook.com/tr?id={self.pixel_id}&ev=PageView&noscript=1"/>
</noscript>'''
        
        elif self.provider.name == 'bing_ads' and self.uet_tag_id:
            return f'''
<!-- Bing Ads Universal Event Tracking -->
<script>
(function(w,d,t,r,u){{var f,n,i;w[u]=w[u]||[],f=function(){{var o={{ti:"{self.uet_tag_id}"}};o.q=w[u],w[u]=new UET(o),w[u].push("pageLoad");}},n=d.createElement(t),n.src=r,n.async=1,n.onload=n.onreadystatechange=function(){{var s=this.readyState;s&&s!=="loaded"&&s!=="complete"||(f(),n.onload=n.onreadystatechange=null);}},i=d.getElementsByTagName(t)[0],i.parentNode.insertBefore(n,i);}})(window,document,"script","//bat.bing.com/bat.js","uetq");
</script>'''
        
        return ''


class WebsiteTracking(models.Model):
    """Track which websites have analytics codes installed"""
    
    # This would link to your website/project models
    website_url = models.URLField()
    website_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Analytics integrations for this website
    integrations = models.ManyToManyField(AnalyticsIntegration, through='WebsiteIntegrationStatus')
    
    # Auto-injection settings
    auto_inject_enabled = models.BooleanField(default=True)
    inject_in_head = models.BooleanField(default=True)
    inject_in_body = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.website_name} - {self.website_url}"


class WebsiteIntegrationStatus(models.Model):
    """Status of analytics integration for specific websites"""
    
    website = models.ForeignKey(WebsiteTracking, on_delete=models.CASCADE)
    integration = models.ForeignKey(AnalyticsIntegration, on_delete=models.CASCADE)
    
    is_active = models.BooleanField(default=True)
    installed_at = models.DateTimeField(auto_now_add=True)
    last_verified = models.DateTimeField(blank=True, null=True)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    
    class Meta:
        unique_together = ['website', 'integration']
    
    def __str__(self):
        return f"{self.website.website_name} - {self.integration.provider.display_name}"


class AnalyticsEvent(models.Model):
    """Track analytics events and conversions"""
    
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('form_submit', 'Form Submit'),
        ('purchase', 'Purchase'),
        ('signup', 'Sign Up'),
        ('download', 'Download'),
        ('custom', 'Custom Event'),
    ]
    
    website = models.ForeignKey(WebsiteTracking, on_delete=models.CASCADE)
    integration = models.ForeignKey(AnalyticsIntegration, on_delete=models.CASCADE)
    
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=100)
    event_data = models.JSONField(default=dict, blank=True)
    
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.event_name} - {self.website.website_name}"