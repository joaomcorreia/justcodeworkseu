from django.urls import path
from . import admin_views

app_name = 'customadmin'

urlpatterns = [
    path('', admin_views.admin_dashboard, name='dashboard'),
    path('pages/', admin_views.pages_management, name='pages'),
    path('blog/', admin_views.blog_management, name='blog'),
    path('website-builder/', admin_views.website_builder_management, name='website_builder'),
    path('website-builder-app/', admin_views.website_builder_iframe, name='website_builder_iframe'),
    path('forms/', admin_views.forms_management, name='forms'),
    path('ai-tools/', admin_views.ai_tools, name='ai_tools'),
    path('print-materials/', admin_views.print_materials, name='print_materials'),
    path('print-materials/cards/', admin_views.print_cards, name='print_cards'),
    path('print-materials/trifolds/', admin_views.print_trifolds, name='print_trifolds'),
    path('print-materials/clothing/', admin_views.print_clothing, name='print_clothing'),
    path('print-materials/gifts/', admin_views.print_gifts, name='print_gifts'),
    path('subscription/', admin_views.subscription_management, name='subscription'),
    path('settings/', admin_views.settings_management, name='settings'),
    path('analytics/facebook/', admin_views.analytics_facebook, name='analytics_facebook'),
    path('analytics/google/', admin_views.analytics_google, name='analytics_google'),
    path('analytics/bing/', admin_views.analytics_bing, name='analytics_bing'),
    path('analytics/integration/', admin_views.analytics_integration, name='analytics_integration'),
    path('translations/', admin_views.translations_management, name='translations'),
    path('api/ai-chat/', admin_views.ai_chat_endpoint, name='ai_chat'),
]