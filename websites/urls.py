from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.tenant_dashboard, name='tenant_dashboard'),
    
    # Website editing
    path('edit-homepage/', views.edit_homepage, name='edit_homepage'),
    
    # Subscriptions
    path('subscription/', views.subscription_overview, name='subscription_overview'),
    path('domain/', views.domain_settings, name='domain_settings'),
    path('hosting/', views.hosting_settings, name='hosting_settings'),
    path('website-settings/', views.website_settings, name='website_settings'),
    path('seo/', views.seo_settings, name='seo_settings'),
    path('social-networks/', views.social_networks, name='social_networks'),
    
    # AI Features
    path('ai/', views.ai_overview, name='ai_overview'),
    path('ai/content-generator/', views.ai_content_generator, name='ai_content_generator'),
    path('ai/design-assistant/', views.ai_design_assistant, name='ai_design_assistant'),
    
    # Analytics
    path('analytics/google/', views.google_analytics, name='google_analytics'),
    path('analytics/facebook/', views.facebook_insights, name='facebook_insights'),
    path('analytics/visitors/', views.visitor_stats, name='visitor_stats'),
    
    # Settings & Users
    path('profile/', views.profile_settings, name='profile_settings'),
    path('users/', views.user_management, name='user_management'),
    
    # Tools
    path('tools/qr-maker/', views.qr_maker, name='qr_maker'),
    path('tools/image-resizer/', views.image_resizer, name='image_resizer'),
    path('tools/backup-restore/', views.backup_restore, name='backup_restore'),
    
    # Preview
    path('preview/', views.website_preview, name='website_preview'),
]