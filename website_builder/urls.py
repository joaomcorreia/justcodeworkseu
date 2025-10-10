"""
Website Builder URL Configuration
"""
from django.urls import path
from . import views

app_name = 'website_builder'

urlpatterns = [
    # Landing page (public)
    path('', views.landing_page, name='landing'),
    
    # Main dashboard (requires login)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Project management
    path('new/', views.start_new_project, name='new_project'),
    path('chat/<uuid:project_id>/', views.chat_interface, name='chat'),
    path('project/<uuid:project_id>/', views.project_detail, name='project_detail'),
    path('preview/<uuid:project_id>/', views.preview_website, name='preview'),
    path('export/<uuid:project_id>/', views.export_project, name='export'),
    
    # Templates
    path('templates/', views.templates_gallery, name='templates'),
    path('template-preview/<str:template_id>/', views.template_preview, name='template_preview'),
    path('create-from-template/<str:template_id>/', views.create_from_template, name='create_from_template'),
    path('download-website/<uuid:project_id>/', views.download_website, name='download_website'),
    path('preview-website/<uuid:project_id>/', views.preview_generated_website, name='preview_generated_website'),
    path('create-from-template/<str:template_id>/', views.create_from_template, name='create_from_template'),
    
    # Website management
    path('download/<uuid:project_id>/', views.download_website, name='download_website'),
    path('live-preview/<uuid:project_id>/', views.preview_generated_website, name='live_preview'),
    
    # API endpoints
    path('api/chat/<uuid:project_id>/', views.chat_api, name='chat_api'),
    path('api/quick-start/', views.quick_start_api, name='quick_start_api'),
    path('api/project/<uuid:project_id>/status/', views.project_status_api, name='project_status_api'),
    path('api/project/<uuid:project_id>/update/', views.update_project_api, name='update_project_api'),
    
    # Debug endpoint
    path('debug/', views.debug_assistant, name='debug_assistant'),
    path('test-chat/', views.test_chat, name='test_chat'),
    
    # New onboarding flow
    path('api/create-from-business-details/', views.create_from_business_details, name='create_from_business_details'),
    path('default-preview/', views.default_preview, name='default_preview'),
]