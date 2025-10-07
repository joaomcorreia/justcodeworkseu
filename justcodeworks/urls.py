"""
URL configuration for justcodeworks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .public_views import homepage, static_page

urlpatterns = [
    # Root URL - public homepage
    path('', homepage, name='homepage'),
    
    # Static pages (user-editable)
    path('static/<str:page_name>/', static_page, name='static_page'),
    
    # AI Assistant (frontend chat widget)
    path('ai/', include('ai_assistant.urls')),
    
    # Website Builder with Clippy 2.0
    path('website-builder/', include('website_builder.urls')),
    
    # Django admin (for development)
    path('django-admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Custom admin system
    path('admin/', include('justcodeworks.admin_urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
