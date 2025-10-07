"""
Static pages models for manual content management
"""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Page(models.Model):
    """
    Static page model for manual content editing
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    # Multi-language support
    title_en = models.CharField(max_length=200, blank=True)
    title_nl = models.CharField(max_length=200, blank=True) 
    title_de = models.CharField(max_length=200, blank=True)
    title_fr = models.CharField(max_length=200, blank=True)
    title_es = models.CharField(max_length=200, blank=True)
    title_pt = models.CharField(max_length=200, blank=True)
    
    # Content fields
    content = RichTextField(help_text="Main page content")
    content_en = RichTextField(blank=True)
    content_nl = RichTextField(blank=True)
    content_de = RichTextField(blank=True) 
    content_fr = RichTextField(blank=True)
    content_es = RichTextField(blank=True)
    content_pt = RichTextField(blank=True)
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Page settings
    is_published = models.BooleanField(default=True)
    is_homepage = models.BooleanField(default=False)
    show_in_menu = models.BooleanField(default=True)
    menu_order = models.IntegerField(default=0)
    
    # Tracking
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['menu_order', 'title']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        if self.is_homepage:
            return '/'
        return reverse('pages:detail', kwargs={'slug': self.slug})
    
    def get_localized_title(self, language='en'):
        """Get title in specific language"""
        field_name = f'title_{language}'
        title = getattr(self, field_name, '') or self.title
        return title
    
    def get_localized_content(self, language='en'):
        """Get content in specific language"""
        field_name = f'content_{language}'
        content = getattr(self, field_name, '') or self.content
        return content
    
    def __str__(self):
        return self.title


class PageSection(models.Model):
    """
    Reusable page sections/components
    """
    page = models.ForeignKey(Page, related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Section identifier")
    
    # Multi-language content
    content = RichTextField()
    content_en = RichTextField(blank=True)
    content_nl = RichTextField(blank=True)
    content_de = RichTextField(blank=True)
    content_fr = RichTextField(blank=True) 
    content_es = RichTextField(blank=True)
    content_pt = RichTextField(blank=True)
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ('page', 'name')
    
    def get_localized_content(self, language='en'):
        """Get content in specific language"""
        field_name = f'content_{language}'
        content = getattr(self, field_name, '') or self.content
        return content
    
    def __str__(self):
        return f"{self.page.title} - {self.name}"
