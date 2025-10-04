from django.db import models
from django.contrib.auth.models import User


class Website(models.Model):
    """
    Website model for tenant websites
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Design settings
    theme = models.CharField(max_length=50, default='default')
    primary_color = models.CharField(max_length=7, default='#007bff')
    secondary_color = models.CharField(max_length=7, default='#6c757d')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Page(models.Model):
    """
    Page model for website pages
    """
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    is_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['website', 'slug']
    
    def __str__(self):
        return f"{self.website.name} - {self.title}"


class HomeSlider(models.Model):
    """
    Home slider items for homepage
    """
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='slider_items')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='slider/', blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.website.name} - {self.title}"


class HomeCarouselItem(models.Model):
    """
    Home carousel items
    """
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='carousel_items')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='carousel/', blank=True)
    link = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.website.name} - {self.title}"


class HomeAboutPanel(models.Model):
    """
    Homepage about panel
    """
    website = models.OneToOneField(Website, on_delete=models.CASCADE, related_name='about_panel')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.website.name} - About Panel"


class HomeValueBlock(models.Model):
    """
    Homepage value blocks
    """
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='value_blocks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.website.name} - {self.title}"


class AboutPage(models.Model):
    """
    About page content
    """
    website = models.OneToOneField(Website, on_delete=models.CASCADE, related_name='about_page')
    title = models.CharField(max_length=200, default="About Us")
    content = models.TextField()
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.website.name} - About Page"


class AboutBenefit(models.Model):
    """
    About page benefits
    """
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='benefits')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.about_page.website.name} - {self.title}"


class Settings(models.Model):
    """
    Website settings
    """
    website = models.OneToOneField(Website, on_delete=models.CASCADE, related_name='settings')
    
    # Contact information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Social media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.website.name} - Settings"


class SiteSettings(models.Model):
    """
    Site-wide settings for each tenant - editable business information
    """
    # Company Information
    company_name = models.CharField(max_length=200, help_text="Your company name")
    company_email = models.EmailField(help_text="Main business email")
    company_phone = models.CharField(max_length=20, blank=True, help_text="Main phone number")
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text="WhatsApp business number")
    company_address = models.TextField(blank=True, help_text="Full business address")
    
    # Business Hours
    opening_hours = models.TextField(blank=True, help_text="Business opening hours (e.g., Mon-Fri: 9:00-17:00)")
    
    # Pricing & Services
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Hourly service rate")
    currency = models.CharField(max_length=10, default='EUR', help_text="Currency for pricing")
    
    # Social Media Links
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn company page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X profile URL")
    youtube_url = models.URLField(blank=True, help_text="YouTube channel URL")
    
    # Automation Settings
    domain_auto_registration = models.BooleanField(default=False, help_text="Enable automatic domain registration")
    hosting_auto_provision = models.BooleanField(default=False, help_text="Enable automatic hosting setup")
    search_engine_submission = models.BooleanField(default=True, help_text="Automatically submit to search engines")
    
    # SEO Settings
    seo_plan = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic SEO (Free)'),
            ('premium', 'Premium SEO'),
        ],
        default='basic'
    )
    
    # Multi-language Settings
    enabled_languages = models.JSONField(default=list, help_text="List of enabled languages for this site")
    default_language = models.CharField(max_length=10, default='en', help_text="Default site language")
    
    # Watermark Settings
    watermark_enabled = models.BooleanField(default=False, help_text="Add watermark to uploaded images")
    watermark_text = models.CharField(max_length=100, blank=True, help_text="Watermark text (company name)")
    watermark_opacity = models.IntegerField(default=50, help_text="Watermark opacity (0-100)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return f"Settings for {self.company_name}"
