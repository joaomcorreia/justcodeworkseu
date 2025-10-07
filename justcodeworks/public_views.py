"""
Public views for JustCodeWorks.EU homepage and public pages
"""
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
import os

def homepage(request):
    """
    Public homepage view - no login required
    """
    context = {
        'page_title': 'JustCodeWorks.EU - AI-Powered Website Solutions',
        'company_name': 'JustCodeWorks.EU',
        'tagline': 'Build Professional Websites with AI',
        'features': [
            {
                'icon': 'fas fa-magic',
                'title': 'AI-Powered Content',
                'description': 'Generate professional content instantly with our advanced AI assistant.'
            },
            {
                'icon': 'fas fa-rocket',
                'title': 'Quick Setup',
                'description': 'Get your website live in minutes with our automated platform.'
            },
            {
                'icon': 'fas fa-cog',
                'title': 'Easy Management',
                'description': 'Manage your content with our intuitive admin dashboard.'
            },
            {
                'icon': 'fas fa-chart-line',
                'title': 'Business Growth',
                'description': 'Built-in tools for forms, analytics, and business materials.'
            }
        ]
    }
    
    return render(request, 'public/homepage.html', context)


def static_page(request, page_name):
    """
    Serve static HTML pages from static/pages/ directory
    These pages can be edited directly by the user
    """
    # Security: Only allow specific page names
    allowed_pages = ['index', 'contact', 'about', 'privacy', 'terms']
    
    if page_name not in allowed_pages:
        raise Http404("Page not found")
    
    # Build path to static HTML file
    static_path = os.path.join(settings.BASE_DIR, 'static', 'pages', f'{page_name}.html')
    
    # Check if file exists
    if not os.path.exists(static_path):
        raise Http404("Page not found")
    
    # Read and return the static HTML file
    try:
        with open(static_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/html')
    except Exception as e:
        raise Http404("Error loading page")