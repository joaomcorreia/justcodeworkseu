"""
Blog models for dynamic content and tutorials
"""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    """
    Blog categories for organizing content
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    # Multi-language support
    name_en = models.CharField(max_length=100, blank=True)
    name_nl = models.CharField(max_length=100, blank=True)
    name_de = models.CharField(max_length=100, blank=True)
    name_fr = models.CharField(max_length=100, blank=True)
    name_es = models.CharField(max_length=100, blank=True)
    name_pt = models.CharField(max_length=100, blank=True)
    
    description_en = models.TextField(blank=True)
    description_nl = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    description_es = models.TextField(blank=True)
    description_pt = models.TextField(blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_localized_name(self, language='en'):
        field_name = f'name_{language}'
        return getattr(self, field_name, '') or self.name
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Blog post model for tutorials and business tips
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('tutorial', 'Tutorial'),
        ('tip', 'Business Tip'),
        ('guide', 'How-to Guide'),
        ('news', 'News & Updates'),
        ('case_study', 'Case Study'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    # Multi-language content
    title_en = models.CharField(max_length=200, blank=True)
    title_nl = models.CharField(max_length=200, blank=True)
    title_de = models.CharField(max_length=200, blank=True)
    title_fr = models.CharField(max_length=200, blank=True)
    title_es = models.CharField(max_length=200, blank=True)
    title_pt = models.CharField(max_length=200, blank=True)
    
    excerpt = models.TextField(max_length=300, help_text="Brief summary")
    excerpt_en = models.TextField(max_length=300, blank=True)
    excerpt_nl = models.TextField(max_length=300, blank=True)
    excerpt_de = models.TextField(max_length=300, blank=True)
    excerpt_fr = models.TextField(max_length=300, blank=True)
    excerpt_es = models.TextField(max_length=300, blank=True)
    excerpt_pt = models.TextField(max_length=300, blank=True)
    
    content = RichTextField()
    content_en = RichTextField(blank=True)
    content_nl = RichTextField(blank=True)
    content_de = RichTextField(blank=True)
    content_fr = RichTextField(blank=True)
    content_es = RichTextField(blank=True)
    content_pt = RichTextField(blank=True)
    
    # Organization
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='tutorial')
    tags = TaggableManager()
    
    # Featured image
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=200, blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False, help_text="Show in featured section")
    
    # Scheduling
    publish_date = models.DateTimeField(default=timezone.now)
    
    # Tracking
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-publish_date', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_published(self):
        return self.status == 'published' and self.publish_date <= timezone.now()
    
    def get_localized_title(self, language='en'):
        field_name = f'title_{language}'
        return getattr(self, field_name, '') or self.title
    
    def get_localized_content(self, language='en'):
        field_name = f'content_{language}'
        return getattr(self, field_name, '') or self.content
    
    def get_localized_excerpt(self, language='en'):
        field_name = f'excerpt_{language}'
        return getattr(self, field_name, '') or self.excerpt
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
    
    def get_reading_time(self):
        """Estimate reading time in minutes"""
        word_count = len(self.content.split())
        return max(1, word_count // 200)  # Average 200 words per minute
    
    def __str__(self):
        return self.title
