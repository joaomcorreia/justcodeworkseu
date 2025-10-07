"""
Website Builder Views - Dashboard and API endpoints
"""
import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from .models import WebsiteProject, WebsiteBuilderConversation, WebsiteTemplate, IndustryTemplate
from .clippy_assistant import ClippyWebsiteBuilder


def landing_page(request):
    """
    Public landing page for website builder
    """
    if request.user.is_authenticated:
        return redirect('website_builder:dashboard')
    
    # Get available templates for preview
    templates = WebsiteTemplate.objects.filter(is_active=True).order_by('-rating')[:6]
    
    context = {
        'templates': templates,
    }
    
    return render(request, 'website_builder/landing.html', context)


@login_required
def dashboard(request):
    """
    Main website builder dashboard
    """
    # Get user's projects
    projects = WebsiteProject.objects.filter(user=request.user).order_by('-created_at')
    
    # Get project statistics
    stats = {
        'total_projects': projects.count(),
        'completed_projects': projects.filter(status='completed').count(),
        'in_progress_projects': projects.filter(status__in=['draft', 'in_progress', 'content_review']).count(),
        'published_projects': projects.filter(status='published').count(),
    }
    
    # Get available templates
    templates = WebsiteTemplate.objects.filter(is_active=True).order_by('-rating')[:6]
    
    context = {
        'projects': projects[:5],  # Show last 5 projects
        'stats': stats,
        'templates': templates,
        'user': request.user,
    }
    
    return render(request, 'website_builder/dashboard.html', context)


@login_required  
def start_new_project(request):
    """
    Start a new website building project with Clippy
    """
    if request.method == 'POST':
        project_name = request.POST.get('project_name', 'My New Website')
        
        # Initialize Clippy assistant
        clippy = ClippyWebsiteBuilder()
        
        try:
            # Start conversation
            project, welcome_message = clippy.start_conversation(request.user, project_name)
            
            if project:
                return redirect('website_builder:chat', project_id=project.project_id)
            else:
                messages.error(request, 'Failed to start new project. Please try again.')
                return redirect('website_builder:dashboard')
                
        except Exception as e:
            messages.error(request, f'Error starting project: {str(e)}')
            return redirect('website_builder:dashboard')
    
    # GET request - show new project form
    return render(request, 'website_builder/new_project.html')


@login_required
def chat_interface(request, project_id):
    """
    Chat interface for website building with Clippy
    """
    try:
        project = get_object_or_404(WebsiteProject, project_id=project_id, user=request.user)
        conversation = project.ai_conversation
        
        # Get conversation history (we'd need to add a Message model for this)
        # For now, just show the current state
        
        context = {
            'project': project,
            'conversation': conversation,
            'current_step': conversation.current_step,
            'progress': project.get_completion_percentage(),
        }
        
        return render(request, 'website_builder/chat.html', context)
        
    except WebsiteProject.DoesNotExist:
        messages.error(request, 'Project not found.')
        return redirect('website_builder:dashboard')


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def chat_api(request, project_id):
    """
    API endpoint for chat interactions with Clippy
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a message.'
            })
        
        # Initialize Clippy
        clippy = ClippyWebsiteBuilder()
        
        # Process conversation
        response = clippy.process_conversation(project_id, user_message, request.user)
        
        return JsonResponse(response)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })


@login_required
def project_detail(request, project_id):
    """
    Detailed view of a website project
    """
    project = get_object_or_404(WebsiteProject, project_id=project_id, user=request.user)
    
    # Get project services
    services = project.services.all().order_by('display_order')
    
    context = {
        'project': project,
        'services': services,
        'can_preview': project.status == 'completed' and project.final_html,
    }
    
    return render(request, 'website_builder/project_detail.html', context)


@login_required
def preview_website(request, project_id):
    """
    Preview the generated website
    """
    project = get_object_or_404(WebsiteProject, project_id=project_id, user=request.user)
    
    if not project.final_html:
        messages.error(request, 'Website not yet generated.')
        return redirect('website_builder:project_detail', project_id=project_id)
    
    # Return the HTML directly
    from django.http import HttpResponse
    return HttpResponse(project.final_html)


@login_required
def export_project(request, project_id):
    """
    Export project as ZIP file
    """
    project = get_object_or_404(WebsiteProject, project_id=project_id, user=request.user)
    
    if not project.final_html:
        messages.error(request, 'Website not yet generated.')
        return redirect('website_builder:project_detail', project_id=project_id)
    
    # Create ZIP export
    import zipfile
    import io
    from django.http import HttpResponse
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add HTML file
        zip_file.writestr('index.html', project.final_html)
        
        # Add CSS file
        if project.final_css:
            zip_file.writestr('style.css', project.final_css)
        
        # Add README with instructions
        readme_content = f"""
{project.business_name} Website
Created with JustCodeWorks Website Builder

Files included:
- index.html: Main website file
- style.css: Website styling
- project_info.txt: Project details

To use:
1. Upload files to your web hosting
2. Set index.html as your main page
3. Your website is ready!

Created: {project.created_at.strftime('%Y-%m-%d')}
Project ID: {project.project_id}
        """.strip()
        
        zip_file.writestr('README.txt', readme_content)
        
        # Add project info
        project_info = f"""
Business Name: {project.business_name}
Industry: {project.industry}
Project Type: {project.page_type}
Services: {', '.join([s.service_name for s in project.services.all()])}
Location: {project.location}
Contact: {project.email} | {project.phone}
Status: {project.status}
        """.strip()
        
        zip_file.writestr('project_info.txt', project_info)
    
    zip_buffer.seek(0)
    
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    filename = f"{project.business_name.replace(' ', '_')}_website.zip"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required
def templates_gallery(request):
    """
    Browse available website templates
    """
    category = request.GET.get('category', 'all')
    
    templates = WebsiteTemplate.objects.filter(is_active=True)
    
    if category != 'all':
        templates = templates.filter(category=category)
    
    templates = templates.order_by('-rating', '-usage_count')
    
    # Get available categories
    categories = WebsiteTemplate.objects.filter(is_active=True).values_list('category', flat=True).distinct()
    
    context = {
        'templates': templates,
        'categories': categories,
        'selected_category': category,
    }
    
    return render(request, 'website_builder/templates.html', context)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def quick_start_api(request):
    """
    Quick start API for simple project creation
    """
    try:
        data = json.loads(request.body)
        
        business_name = data.get('business_name', '').strip()
        industry = data.get('industry', '').strip()
        
        if not business_name:
            return JsonResponse({
                'success': False,
                'message': 'Business name is required.'
            })
        
        # Create quick project
        project = WebsiteProject.objects.create(
            user=request.user,
            project_name=f"{business_name} Website",
            business_name=business_name,
            industry=industry or 'professional_services',
            status='draft'
        )
        
        # Create conversation
        conversation = WebsiteBuilderConversation.objects.create(
            project=project,
            current_step='welcome'
        )
        
        return JsonResponse({
            'success': True,
            'project_id': str(project.project_id),
            'redirect_url': f'/website-builder/chat/{project.project_id}/',
            'message': f'Project created for {business_name}!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating project: {str(e)}'
        })


# API Views for AJAX requests

@csrf_exempt
@require_http_methods(["GET"])
@login_required
def project_status_api(request, project_id):
    """
    Get project status and progress
    """
    try:
        project = get_object_or_404(WebsiteProject, project_id=project_id, user=request.user)
        
        return JsonResponse({
            'success': True,
            'project': {
                'id': str(project.project_id),
                'business_name': project.business_name,
                'status': project.status,
                'progress': project.get_completion_percentage(),
                'current_step': project.ai_conversation.current_step if hasattr(project, 'ai_conversation') else 'welcome',
                'services_count': project.services.count(),
                'created_at': project.created_at.isoformat(),
            }
        })
        
    except WebsiteProject.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Project not found.'
        })


@csrf_exempt  
@require_http_methods(["POST"])
@login_required
def update_project_api(request, project_id):
    """
    Update project details via API
    """
    try:
        project = get_object_or_404(WebsiteProject, project_id=project_id, user=request.user)
        data = json.loads(request.body)
        
        # Update allowed fields
        allowed_fields = ['project_name', 'business_description', 'location', 'phone', 'email']
        updated_fields = []
        
        for field in allowed_fields:
            if field in data:
                setattr(project, field, data[field])
                updated_fields.append(field)
        
        if updated_fields:
            project.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Updated: {", ".join(updated_fields)}',
                'updated_fields': updated_fields
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No valid fields to update.'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating project: {str(e)}'
        })