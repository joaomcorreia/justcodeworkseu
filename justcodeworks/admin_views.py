"""
Admin views for JustCodeWorks dashboard
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from pages.models import Page
from blog.models import Post, Category
from ai_assistant.models import Conversation, Message


@login_required
def admin_dashboard(request):
    """
    Main admin dashboard view
    """
    # Get basic stats
    context = {
        'total_pages': Page.objects.count() if hasattr(Page.objects, 'count') else 0,
        'total_posts': Post.objects.count() if hasattr(Post.objects, 'count') else 0,
        'total_conversations': Conversation.objects.count() if hasattr(Conversation.objects, 'count') else 0,
        'page_title': 'Dashboard Overview',
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required
def pages_management(request):
    """
    Pages management view
    """
    context = {
        'page_title': 'Pages Management',
        'section': 'pages'
    }
    return render(request, 'admin/pages.html', context)


@login_required
def blog_management(request):
    """
    Blog management view
    """
    context = {
        'page_title': 'Blog Posts',
        'section': 'blog'
    }
    return render(request, 'admin/blog.html', context)


@login_required
def forms_management(request):
    """
    Forms management view
    """
    context = {
        'page_title': 'Forms Management',
        'section': 'forms'
    }
    return render(request, 'admin/forms.html', context)


@login_required
def ai_tools(request):
    """
    AI tools view
    """
    context = {
        'page_title': 'AI Content Generator',
        'section': 'ai-tools'
    }
    return render(request, 'admin/ai_tools.html', context)


@login_required
def print_materials(request):
    """
    Print materials view
    """
    context = {
        'page_title': 'Print Materials',
        'section': 'print-materials'
    }
    return render(request, 'admin/print_materials.html', context)


@login_required
def ai_chat_endpoint(request):
    """
    AI chat API endpoint
    """
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            message = data.get('message', '')
            
            # Mock AI response for now
            response_data = {
                'response': f'I received your message: "{message}". This is a mock response. The actual AI integration will be connected soon!',
                'suggestions': [
                    'Tell me more',
                    'Create a new page',
                    'Help with forms',
                    'Show examples'
                ]
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)