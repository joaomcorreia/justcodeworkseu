"""
Website Builder Views - Dashboard and API endpoints
"""
import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from .models import WebsiteProject, WebsiteBuilderConversation, WebsiteTemplate, IndustryTemplate
from .clippy_assistant import ClippyWebsiteBuilder
from django.template import Template, Context
import zipfile
from io import BytesIO


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
@login_required
def start_new_project(request):
    """
    Start a new website building project with Clippy
    """
    if request.method == 'POST':
        project_name = request.POST.get('project_name', 'My New Website')
        
        # Initialize Clippy assistant
        try:
            clippy = ClippyWebsiteBuilder()
            
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


# @login_required  # Temporarily disabled for testing
def chat_interface(request, project_id):
    """
    Chat interface for website building with Clippy
    """
    try:
        # For testing purposes, find project by ID regardless of user
        project = get_object_or_404(WebsiteProject, project_id=project_id)
        conversation = project.ai_conversation
        
        # Generate initial message if this is the first time visiting the chat
        initial_message = None
        if conversation.current_step == 'template_selection':
            initial_message = "Hello! 👋 I'm Clippy, your AI website builder assistant and I am going to help you build a great website."
        
        # Get conversation history (we'd need to add a Message model for this)
        # For now, just show the current state
        
        context = {
            'project': project,
            'conversation': conversation,
            'current_step': conversation.current_step,
            'progress': project.get_completion_percentage(),
            'initial_message': initial_message,
            'conversation_data': conversation.conversation_data,  # Pass conversation data to template
        }
        
        return render(request, 'website_builder/chat.html', context)
        
    except WebsiteProject.DoesNotExist:
        messages.error(request, 'Project not found.')
        return redirect('website_builder:dashboard')


@csrf_exempt
@require_http_methods(["POST"])
# @login_required  # Temporarily disabled for testing
def chat_api(request, project_id):
    """
    API endpoint for chat interactions with Clippy
    """
    import traceback
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
        
        # Process conversation (get user or create test user for debugging)
        from django.contrib.auth.models import User
        user = request.user if request.user.is_authenticated else User.objects.get_or_create(username='testuser')[0]
        response = clippy.process_conversation(project_id, user_message, user)
        
        return JsonResponse(response)
        
    except json.JSONDecodeError as e:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.',
            'error_type': 'json_decode',
            'error_detail': str(e)
        })
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Chat API Error: {e}")
        print(traceback.format_exc())
        
        return JsonResponse({
            'success': False,
            'message': f'Sorry, I encountered an error. Please try again. ({str(e)})',
            'error_type': 'general',
            'error_detail': str(e)
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
    
    # Get available categories with display names
    categories_raw = set(WebsiteTemplate.objects.filter(is_active=True).values_list('category', flat=True))
    
    # Category display name mapping (matches database categories)
    category_names = {
        'bars': '🍺 Bars & Nightlife',
        'business': '💼 Business & Professional',
        'construction': '🏗️ Construction & Building',
        'creative': '🎨 Creative & Design',
        'ecommerce': '🛒 E-commerce & Shop',
        'portfolio': '📁 Portfolio & Showcase',
        'restaurant': '🍽️ Restaurant & Food',
    }
    
    # Create categories list with display names
    categories = []
    for cat in categories_raw:
        display_name = category_names.get(cat, cat.title())
        categories.append({
            'key': cat,
            'name': display_name
        })
    
    # Debug: Check for missing category mappings (only in development)
    from django.conf import settings
    if settings.DEBUG:
        missing_categories = [cat for cat in categories_raw if cat not in category_names]
        if missing_categories:
            print(f"⚠️  Warning: Categories in database but not in category_names: {missing_categories}")
        
        unused_categories = [cat for cat in category_names.keys() if cat not in categories_raw]
        if unused_categories:
            print(f"ℹ️  Info: Categories in category_names but not in database: {unused_categories}")
    
    context = {
        'templates': templates,
        'categories': categories,
        'selected_category': category,
        'category_names': category_names,
    }
    
    return render(request, 'website_builder/templates.html', context)


def template_preview(request, template_id):
    """
    Returns template HTML content for preview
    """
    try:
        template_obj = WebsiteTemplate.objects.get(template_id=template_id, is_active=True)
        
        # Sample data for template preview - matching template variables
        sample_data = {
            'business_name': 'Your Business Name',
            'business_description': 'Your business description goes here. We provide excellent services to help your business grow and succeed.',
            'business_phone': '+1 (555) 123-4567',
            'business_email': 'info@yourbusiness.com',
            'business_address': '123 Main Street<br>Suite 100<br>Your City, ST 12345',
            'business_hours': 'Mon-Fri: 9:00 AM - 6:00 PM<br>Sat: 10:00 AM - 4:00 PM<br>Sun: Closed',
            'contact_phone': '+1 (555) 123-4567',
            'contact_email': 'info@yourbusiness.com',
            'address': '123 Main St, Your City, State 12345',
            'services': [
                'Professional Service 1',
                'Quality Service 2', 
                'Expert Service 3'
            ],
            'features': [
                'Feature 1',
                'Feature 2',
                'Feature 3'
            ],
            # Social media links for footer
            'social_facebook': '#',
            'social_twitter': '#',
            'social_linkedin': '#',
            'social_instagram': '#'
        }
        
        # Render template with sample data
        from django.template import Template, Context
        django_template = Template(template_obj.html_template)
        context = Context(sample_data)
        html_content = django_template.render(context)
        
        return HttpResponse(html_content, content_type='text/html')
        
    except WebsiteTemplate.DoesNotExist:
        return HttpResponse("Template not found", status=404)


@login_required
def create_from_template(request, template_id):
    """
    Create website from selected template - shows form for business information input
    """
    try:
        template_obj = get_object_or_404(WebsiteTemplate, template_id=template_id, is_active=True)
        
        if request.method == 'POST':
            # Process form data
            business_data = {
                'business_name': request.POST.get('business_name', '').strip(),
                'business_description': request.POST.get('business_description', '').strip(),
                'phone': request.POST.get('phone', '').strip(),
                'email': request.POST.get('email', '').strip(),
                'location': request.POST.get('location', '').strip(),
                'target_audience': request.POST.get('target_audience', '').strip(),
            }
            
            # Validate required fields
            if not business_data['business_name']:
                messages.error(request, 'Business name is required.')
                return render(request, 'website_builder/create_from_template.html', {
                    'template': template_obj,
                    'form_data': business_data
                })
            
            # Create website from template
            result = create_website_from_template_data(
                user=request.user,
                template_id=template_id,
                business_data=business_data
            )
            
            if result['success']:
                messages.success(request, result['message'])
                return redirect('website_builder:project_detail', project_id=result['project'].project_id)
            else:
                messages.error(request, result['error'])
                return render(request, 'website_builder/create_from_template.html', {
                    'template': template_obj,
                    'form_data': business_data
                })
        
        # GET request - show form
        context = {
            'template': template_obj,
            'form_data': {}  # Empty form
        }
        
        return render(request, 'website_builder/create_from_template.html', context)
        
    except WebsiteTemplate.DoesNotExist:
        messages.error(request, 'Template not found.')
        return redirect('website_builder:templates')


def create_website_from_template_data(user, template_id, business_data):
    """
    Core function to convert template into website with user's business data
    """
    try:
        # Get the template
        template_obj = WebsiteTemplate.objects.get(template_id=template_id, is_active=True)
        
        # Create Django template from HTML
        django_template = Template(template_obj.html_template)
        
        # Create context with user's business data
        context = Context(business_data)
        
        # Generate final HTML
        final_html = django_template.render(context)
        
        # Create CSS and JS content
        final_css = template_obj.css_template or ""
        final_js = template_obj.js_template or ""
        
        # Create a website project record
        project = WebsiteProject.objects.create(
            user=user,
            project_name=business_data.get('business_name', 'My Website'),
            business_name=business_data.get('business_name', ''),
            industry=template_obj.category,
            business_description=business_data.get('business_description', ''),
            target_audience=business_data.get('target_audience', ''),
            location=business_data.get('location', ''),
            phone=business_data.get('phone', ''),
            email=business_data.get('email', ''),
            template_id=template_obj.template_id,
            template_used=template_obj.template_id,
            final_html=final_html,
            final_css=final_css,
            final_js=final_js,
            status='completed'
        )
        
        return {
            'success': True,
            'project': project,
            'html_content': final_html,
            'css_content': final_css,
            'js_content': final_js,
            'template_used': template_obj,
            'message': f'Website created successfully using {template_obj.name}!'
        }
        
    except WebsiteTemplate.DoesNotExist:
        return {
            'success': False,
            'error': f'Template {template_id} not found or not active'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error creating website: {str(e)}'
        }


@login_required  
def download_website(request, project_id):
    """
    Download website as ZIP file with HTML, CSS, JS files
    """
    try:
        project = get_object_or_404(WebsiteProject, project_id=project_id, user=request.user)
        
        if not project.final_html:
            messages.error(request, 'No generated website content found for this project.')
            return redirect('website_builder:project_detail', project_id=project_id)
        
        # Create ZIP file
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add HTML file
            zip_file.writestr('index.html', project.final_html)
            
            # Add CSS file if exists
            if project.final_css:
                zip_file.writestr('style.css', project.final_css)
            
            # Add JS file if exists  
            if project.final_js:
                zip_file.writestr('script.js', project.final_js)
            
            # Add README with instructions
            readme_content = f'''# {project.business_name} Website

Generated using JustCodeWorks.EU Template System

## Files:
- index.html - Main website file
- style.css - Stylesheet (if applicable)
- script.js - JavaScript functionality (if applicable)

## To use:
1. Upload all files to your web hosting provider
2. Set index.html as your homepage
3. Customize content as needed

## Template Used: {project.template_used or 'Custom'}
## Generated: {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Visit JustCodeWorks.EU for more templates and website services!
'''
            zip_file.writestr('README.txt', readme_content)
        
        # Prepare response
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        filename = f"{project.business_name.replace(' ', '_')}_website.zip"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error creating download: {str(e)}')
        return redirect('website_builder:project_detail', project_id=project_id)


@login_required
def preview_generated_website(request, project_id):
    """
    Preview the generated website in full screen
    """
    try:
        project = get_object_or_404(WebsiteProject, project_id=project_id, user=request.user)
        
        if not project.final_html:
            return HttpResponse("No generated website content found for this project.", status=404)
        
        # Return the generated HTML directly
        return HttpResponse(project.final_html, content_type='text/html')
        
    except Exception as e:
        return HttpResponse(f"Error loading website: {str(e)}", status=500)


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
        allowed_fields = [
            'project_name', 'business_name', 'business_description', 'business_address', 
            'location', 'phone', 'email', 'business_email', 'whatsapp_number', 'opening_times',
            'industry', 'website_type'
        ]
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


def debug_assistant(request):
    """
    Debug page to test assistant functionality
    """
    try:
        from .clippy_assistant import ClippyWebsiteBuilder
        clippy = ClippyWebsiteBuilder()
        
        debug_info = {
            'clippy_initialized': True,
            'magic_ai_available': hasattr(clippy, 'generate_website_content'),
            'conversation_steps': list(clippy.conversation_steps.keys()),
        }
        
        return JsonResponse({
            'success': True,
            'message': 'Assistant debugging information',
            'debug_info': debug_info
        })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'message': f'Debug error: {str(e)}',
            'traceback': traceback.format_exc()
        })


def test_chat(request):
    """
    Create a test chat session
    """
    try:
        from django.contrib.auth.models import User
        from .clippy_assistant import ClippyWebsiteBuilder
        
        # Get or create test user
        user, created = User.objects.get_or_create(username='testuser')
        
        # Initialize assistant
        clippy = ClippyWebsiteBuilder()
        
        # Create test project
        project, welcome_msg = clippy.start_conversation(user, 'Test Project')
        
        # Redirect to chat interface
        return redirect('website_builder:chat', project_id=project.project_id)
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'message': f'Error creating test chat: {str(e)}',
            'traceback': traceback.format_exc()
        })


@require_http_methods(["POST"])
def create_from_business_details(request):
    """
    Create a new website project from business details form
    """
    try:
        data = json.loads(request.body)
        
        # Get or create user (for now, create anonymous user)
        from django.contrib.auth.models import User
        import uuid
        
        # Create anonymous user or get existing test user
        username = f"business_{uuid.uuid4().hex[:8]}"
        user = User.objects.create_user(username=username, email=f"{username}@temp.com")
        
        # Create website project with business details
        project = WebsiteProject.objects.create(
            user=user,
            project_name=data.get('business_name', 'My Website'),
            business_name=data.get('business_name', ''),
            business_address=data.get('business_address', ''),
            phone=data.get('phone_number', ''),
            business_email=data.get('business_email', ''),  # New field
            whatsapp_number=data.get('whatsapp_number', ''),  # New field  
            opening_times=data.get('opening_times', ''),  # New field
            industry=data.get('business_type', ''),  # Map business_type to industry field
            website_type=data.get('website_type', 'one_page'),
            # Store payment info securely (in production, this would be encrypted/tokenized)
            payment_verified=True  # For demo purposes
        )
        
        # Create conversation tracker starting at template selection since we have basic info
        from .models import WebsiteBuilderConversation
        conversation = WebsiteBuilderConversation.objects.create(
            project=project,
            current_step='template_selection',  # Skip basic info since we have it
            conversation_data={
                'business_name': data.get('business_name', ''),
                'business_address': data.get('business_address', ''),
                'phone_number': data.get('phone_number', ''),
                'business_email': data.get('business_email', ''),
                'whatsapp_number': data.get('whatsapp_number', ''),
                'opening_times': data.get('opening_times', ''),
                'business_type': data.get('business_type', ''),
                'website_type': data.get('website_type', 'one_page'),
                'onboarding_completed': True
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Project created successfully',
            'project_id': str(project.project_id),
            'user_id': user.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid form data'
        })
    except Exception as e:
        import traceback
        print(f"Error creating project from business details: {e}")
        print(traceback.format_exc())
        
        return JsonResponse({
            'success': False,
            'message': f'Error creating project: {str(e)}'
        })


def default_preview(request):
    """
    Renders the default preview template for new projects
    """
    context = {
        'business_name': 'Your Business Name',
        'business_address': 'Your Business Address',
        'phone_number': 'Your Phone Number',
        'website_type': 'one-page',
        'is_preview': True
    }
    return render(request, 'website_builder/default_preview.html', context)