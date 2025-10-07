"""
AI Assistant models for MagicAI integration and chat functionality
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class Conversation(models.Model):
    """
    AI Assistant conversation tracking
    """
    SESSION_TYPES = [
        ('anonymous', 'Anonymous Visitor'),
        ('lead', 'Potential Customer'),
        ('customer', 'Existing Customer'),
        ('support', 'Support Request'),
    ]
    
    # Session identification
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Visitor information (collected during chat)
    visitor_name = models.CharField(max_length=100, blank=True)
    visitor_email = models.EmailField(blank=True)
    visitor_company = models.CharField(max_length=100, blank=True)
    visitor_phone = models.CharField(max_length=20, blank=True)
    
    # Context
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='anonymous')
    language = models.CharField(max_length=10, default='en')
    referrer_url = models.URLField(blank=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Conversation analytics
    message_count = models.IntegerField(default=0)
    avg_response_time = models.FloatField(default=0.0)  # seconds
    satisfaction_score = models.IntegerField(null=True, blank=True)  # 1-5 rating
    
    # Business intelligence
    detected_intent = models.CharField(max_length=50, blank=True)
    detected_industry = models.CharField(max_length=50, blank=True)
    budget_signals = models.JSONField(default=dict, blank=True)
    lead_score = models.IntegerField(default=0)  # 0-100
    
    # Status
    is_active = models.BooleanField(default=True)
    requires_followup = models.BooleanField(default=False)
    followup_notes = models.TextField(blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    @property
    def duration(self):
        """Calculate conversation duration"""
        end_time = self.ended_at or timezone.now()
        return end_time - self.started_at
    
    @property
    def is_qualified_lead(self):
        """Determine if this is a qualified sales lead"""
        return (
            self.visitor_email and 
            self.lead_score >= 50 and
            self.message_count >= 3
        )
    
    def __str__(self):
        name = self.visitor_name or f"Session {self.session_id[:8]}"
        return f"{name} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"


class Message(models.Model):
    """
    Individual messages in AI conversations
    """
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('assistant', 'AI Assistant'),
        ('system', 'System Message'),
    ]
    
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    
    # Message content
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    
    # AI context (for assistant messages)
    ai_model = models.CharField(max_length=50, blank=True)  # e.g., 'gpt-4'
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    response_time = models.FloatField(default=0.0)  # seconds
    
    # User context (for user messages)
    intent_detected = models.CharField(max_length=50, blank=True)
    sentiment = models.CharField(max_length=20, blank=True)  # positive, neutral, negative
    entities_extracted = models.JSONField(default=dict, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.get_message_type_display()}: {self.content[:50]}..."


class AIKnowledgeBase(models.Model):
    """
    Knowledge base for AI assistant training
    """
    CONTENT_TYPES = [
        ('faq', 'FAQ'),
        ('service', 'Service Information'),
        ('pricing', 'Pricing Details'),
        ('process', 'Process Explanation'),
        ('feature', 'Feature Description'),
        ('policy', 'Policy Information'),
    ]
    
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    
    # Multi-language content
    content = models.TextField(help_text="Knowledge content for AI training")
    content_en = models.TextField(blank=True)
    content_nl = models.TextField(blank=True)
    content_de = models.TextField(blank=True)
    content_fr = models.TextField(blank=True)
    content_es = models.TextField(blank=True)
    content_pt = models.TextField(blank=True)
    
    # Keywords and matching
    keywords = models.JSONField(default=list, help_text="Keywords that trigger this content")
    priority = models.IntegerField(default=1, help_text="Higher numbers = higher priority")
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'title']
    
    def get_localized_content(self, language='en'):
        """Get content in specific language"""
        field_name = f'content_{language}'
        content = getattr(self, field_name, '') or self.content
        return content
    
    def increment_usage(self):
        """Track usage for analytics"""
        self.usage_count += 1
        self.last_used = timezone.now()
        self.save()
    
    def __str__(self):
        return f"{self.get_content_type_display()}: {self.title}"


class AITrainingData(models.Model):
    """
    Training data for improving AI responses
    """
    # Input
    user_input = models.TextField()
    context = models.JSONField(default=dict, blank=True)
    
    # AI Response
    ai_response = models.TextField()
    confidence_score = models.FloatField(default=0.0)
    
    # Human feedback
    is_helpful = models.BooleanField(null=True, blank=True)
    feedback_notes = models.TextField(blank=True)
    corrected_response = models.TextField(blank=True)
    
    # Metadata
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Training: {self.user_input[:50]}..."
