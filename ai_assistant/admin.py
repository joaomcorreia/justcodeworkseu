from django.contrib import admin
from .models import AIKnowledgeBase, Conversation, Message, AITrainingData


@admin.register(AIKnowledgeBase)
class AIKnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'priority', 'usage_count', 'is_active', 'created_at']
    list_filter = ['content_type', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'keywords']
    readonly_fields = ['usage_count', 'last_used', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content_type', 'priority', 'is_active')
        }),
        ('Content', {
            'fields': ('content', 'keywords'),
            'description': 'Main content and keywords that trigger this knowledge entry'
        }),
        ('Multi-language Content (Optional)', {
            'fields': ('content_en', 'content_nl', 'content_de', 'content_fr', 'content_es', 'content_pt'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('usage_count', 'last_used'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'visitor_name', 'visitor_email', 'session_type', 'started_at', 'message_count']
    list_filter = ['session_type', 'started_at']
    search_fields = ['visitor_name', 'visitor_email', 'visitor_company']
    readonly_fields = ['session_id', 'started_at', 'last_activity']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'message_type', 'message_preview', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['timestamp', 'response_time', 'metadata']
    
    def message_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    message_preview.short_description = 'Message Preview'
