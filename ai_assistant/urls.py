"""
AI Assistant URL configuration
Frontend chat widget and API endpoints
"""
from django.urls import path
from . import chat_views

app_name = 'ai_assistant'

urlpatterns = [
    # Chat widget demo page
    path('demo/', chat_views.chat_widget_page, name='chat_demo'),
    
    # API endpoints
    path('chat/', chat_views.frontend_chat_api, name='chat_api'),
    path('visitor-info/', chat_views.collect_visitor_info, name='visitor_info'),
    path('config/', chat_views.chat_widget_config, name='chat_config'),
]