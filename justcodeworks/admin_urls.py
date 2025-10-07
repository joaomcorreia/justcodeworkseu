from django.urls import path
from . import admin_views

app_name = 'customadmin'

urlpatterns = [
    path('', admin_views.admin_dashboard, name='dashboard'),
    path('pages/', admin_views.pages_management, name='pages'),
    path('blog/', admin_views.blog_management, name='blog'),
    path('forms/', admin_views.forms_management, name='forms'),
    path('ai-tools/', admin_views.ai_tools, name='ai_tools'),
    path('print-materials/', admin_views.print_materials, name='print_materials'),
    path('api/ai-chat/', admin_views.ai_chat_endpoint, name='ai_chat'),
]