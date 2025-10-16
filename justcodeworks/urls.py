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
from django.conf.urls.i18n import i18n_patterns
from .public_views import homepage, static_page, websites_page, prints_page, submit_print_order, robots_txt

urlpatterns = [
    # Robots.txt - block search engines from development site
    path('robots.txt', robots_txt, name='robots_txt'),
    
    # Language switching
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Rosetta translation management (admin only)
    path('rosetta/', include('rosetta.urls')),
]

urlpatterns += i18n_patterns(
    # Root URL - public homepage
    path('', homepage, name='homepage'),
    
    # Websites page - dedicated website builder landing
    path('websites/', websites_page, name='websites_page'),
    
    # Print services page - where customers order prints
    path('prints/', prints_page, name='prints_page'),
    
    # Print order submission
    path('api/submit-print-order/', submit_print_order, name='submit_print_order'),
    
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
)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
