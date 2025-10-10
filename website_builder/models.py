"""
Website Builder models for interactive website creation
"""
from django.db import models
from django.contrib.auth.models import User
from tenants.models import Tenant
from django.utils import timezone
import json
import uuid


class WebsiteProject(models.Model):
    """
    Main website project created through the AI assistant
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('content_review', 'Content Review'),
        ('design_review', 'Design Review'),
        ('completed', 'Completed'),
        ('published', 'Published'),
        ('paused', 'Paused'),
    ]
    
    PAGE_TYPE_CHOICES = [
        ('one_page', 'One Page Website'),
        ('multi_page', 'Multi-Page Website'),
        ('landing_page', 'Landing Page'),
        ('portfolio', 'Portfolio'),
        ('ecommerce', 'E-commerce'),
    ]
    
    # Core identification
    project_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='website_projects')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name='websites')
    
    # Project details
    project_name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    page_type = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES, default='one_page')
    
    # Business information collected by AI
    business_description = models.TextField(blank=True)
    target_audience = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=200, blank=True)
    business_address = models.TextField(blank=True)  # Full business address
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website_type = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES, default='one_page')  # From onboarding
    payment_verified = models.BooleanField(default=False)  # Payment verification status
    website_url = models.URLField(blank=True)
    social_media = models.JSONField(default=dict, blank=True)  # Store social media links
    
    # Selected template and style
    template_id = models.CharField(max_length=50, blank=True)
    color_scheme = models.CharField(max_length=50, default='professional')
    font_style = models.CharField(max_length=50, default='modern')
    
    # Content preferences
    content_tone = models.CharField(max_length=50, default='professional')  # professional, friendly, creative
    language = models.CharField(max_length=10, default='en')
    
    # Status and progress
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    completion_percentage = models.IntegerField(default=0)
    assistant_conversation_id = models.CharField(max_length=100, blank=True)
    
    # Generated content
    generated_content = models.JSONField(default=dict, blank=True)
    final_html = models.TextField(blank=True)
    final_css = models.TextField(blank=True)
    final_js = models.TextField(blank=True)
    template_used = models.CharField(max_length=50, blank=True)  # Track which template was used
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Website Project"
        verbose_name_plural = "Website Projects"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.business_name} - {self.project_name}"
    
    def get_completion_percentage(self):
        """Calculate project completion based on filled fields"""
        required_fields = [
            self.business_name,
            self.industry,
            self.business_description,
            self.target_audience,
            self.template_id,
        ]
        completed = sum(1 for field in required_fields if field)
        return int((completed / len(required_fields)) * 100)


class BusinessService(models.Model):
    """
    Services offered by the business, selected during AI conversation
    """
    project = models.ForeignKey(WebsiteProject, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=200)
    service_description = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    # AI-generated content for this service
    short_description = models.CharField(max_length=300, blank=True)
    detailed_description = models.TextField(blank=True)
    features = models.JSONField(default=list, blank=True)  # List of service features
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Business Service"
        verbose_name_plural = "Business Services"
        ordering = ['display_order', 'service_name']
    
    def __str__(self):
        return f"{self.project.business_name} - {self.service_name}"


class WebsiteTemplate(models.Model):
    """
    Available website templates that can be generated or pre-made
    """
    TEMPLATE_CATEGORIES = [
        ('business', 'General Business'),
        ('construction', 'Construction & Building'),
        ('technology', 'Technology & IT'),
        ('restaurant', 'Restaurant & Food'),
        ('health', 'Healthcare & Wellness'),
        ('creative', 'Creative & Design'),
        ('ecommerce', 'E-commerce'),
        ('portfolio', 'Portfolio & Personal'),
    ]
    
    template_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=TEMPLATE_CATEGORIES)
    description = models.TextField()
    
    # Template files
    html_template = models.TextField()
    css_template = models.TextField()
    js_template = models.TextField(blank=True)
    
    # Template configuration
    supports_one_page = models.BooleanField(default=True)
    supports_multi_page = models.BooleanField(default=True)
    color_schemes = models.JSONField(default=list, blank=True)  # Available color schemes
    font_options = models.JSONField(default=list, blank=True)   # Available fonts
    
    # Preview and images
    preview_image = models.URLField(blank=True)
    thumbnail_image = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    rating = models.FloatField(default=5.0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Website Template"
        verbose_name_plural = "Website Templates"
        ordering = ['-usage_count', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class WebsiteBuilderConversation(models.Model):
    """
    Track the AI conversation during website building process
    """
    CONVERSATION_STEPS = [
        ('welcome', 'Welcome & Introduction'),
        ('business_name', 'Business Name Collection'),
        ('industry_selection', 'Industry Selection'),
        ('services_selection', 'Services Selection'),
        ('business_details', 'Business Details Collection'),
        ('template_selection', 'Template Selection'),
        ('content_generation', 'Content Generation'),
        ('content_review', 'Content Review & Editing'),
        ('final_review', 'Final Review'),
        ('completion', 'Project Completion'),
    ]
    
    project = models.OneToOneField(WebsiteProject, on_delete=models.CASCADE, related_name='ai_conversation')
    current_step = models.CharField(max_length=30, choices=CONVERSATION_STEPS, default='welcome')
    conversation_data = models.JSONField(default=dict, blank=True)  # Store all collected data
    
    # Progress tracking
    step_progress = models.JSONField(default=dict, blank=True)  # Track completion of each step
    total_messages = models.IntegerField(default=0)
    
    # AI behavior settings
    assistant_personality = models.CharField(max_length=50, default='helpful')  # helpful, friendly, professional
    user_expertise_level = models.CharField(max_length=30, default='beginner')  # beginner, intermediate, expert
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Website Builder Conversation"
        verbose_name_plural = "Website Builder Conversations"
    
    def __str__(self):
        return f"Conversation for {self.project.business_name}"
    
    def get_next_step(self):
        """Get the next step in the conversation flow"""
        steps = [step[0] for step in self.CONVERSATION_STEPS]
        try:
            current_index = steps.index(self.current_step)
            if current_index < len(steps) - 1:
                return steps[current_index + 1]
        except ValueError:
            pass
        return None
    
    def advance_step(self):
        """Advance to the next conversation step"""
        next_step = self.get_next_step()
        if next_step:
            self.current_step = next_step
            self.save()
        return next_step


class IndustryTemplate(models.Model):
    """
    Pre-defined industry templates with common services and content patterns
    """
    industry_name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Common services for this industry
    common_services = models.JSONField(default=list, blank=True)
    
    # Content templates
    business_description_template = models.TextField(blank=True)
    services_intro_template = models.TextField(blank=True)
    about_us_template = models.TextField(blank=True)
    
    # SEO and marketing
    common_keywords = models.JSONField(default=list, blank=True)
    target_audience_suggestions = models.JSONField(default=list, blank=True)
    
    # Design preferences
    recommended_colors = models.JSONField(default=list, blank=True)
    recommended_templates = models.ManyToManyField(WebsiteTemplate, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Industry Template"
        verbose_name_plural = "Industry Templates"
        ordering = ['display_name']
    
    def __str__(self):
        return self.display_name