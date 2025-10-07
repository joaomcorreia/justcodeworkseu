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
    
    # API endpoints
    path('api/chat/<uuid:project_id>/', views.chat_api, name='chat_api'),
    path('api/quick-start/', views.quick_start_api, name='quick_start_api'),
    path('api/project/<uuid:project_id>/status/', views.project_status_api, name='project_status_api'),
    path('api/project/<uuid:project_id>/update/', views.update_project_api, name='update_project_api'),
]