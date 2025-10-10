"""
Template-based website creation views
Integration for turning templates into real websites
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.template import Template, Context
from .models import WebsiteTemplate, WebsiteProject
import json
import uuid
import os
from django.conf import settings


@login_required
def create_from_template(request, template_id):
    """
    Create website from selected template
    Shows form for business information input
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
    Core function to convert template into website
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
        
        # Create CSS file content (combine template CSS with any custom styles)
        final_css = template_obj.css_template or ""
        
        # Create JS file content
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
            status='completed'
        )
        
        # Store the generated files (you could save these to files or database)
        # For now, we'll store in the project record
        project.generated_html = final_html
        project.generated_css = final_css  
        project.generated_js = final_js
        project.template_used = template_obj.template_id
        project.save()
        
        return {
            'success': True,
            'project': project,
            'html_content': final_html,
            'css_content': final_css,
            'js_content': final_js,
            'template_used': template_obj,
            'message': f'Website created successfully using {template_obj.name}'
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
        
        if not hasattr(project, 'generated_html') or not project.generated_html:
            messages.error(request, 'No generated website content found for this project.')
            return redirect('website_builder:project_detail', project_id=project_id)
        
        # Create ZIP file
        import zipfile
        from io import BytesIO
        
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add HTML file
            zip_file.writestr('index.html', project.generated_html)
            
            # Add CSS file if exists
            if hasattr(project, 'generated_css') and project.generated_css:
                zip_file.writestr('style.css', project.generated_css)
            
            # Add JS file if exists  
            if hasattr(project, 'generated_js') and project.generated_js:
                zip_file.writestr('script.js', project.generated_js)
            
            # Add README with instructions
            readme_content = f'''
# {project.business_name} Website

Generated using JustCodeWorks.EU Template System

## Files:
- index.html - Main website file
- style.css - Stylesheet (if applicable)
- script.js - JavaScript functionality (if applicable)

## To use:
1. Upload all files to your web hosting provider
2. Set index.html as your homepage
3. Customize content as needed

## Template Used: {getattr(project, 'template_used', 'Unknown')}
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
        
        if not hasattr(project, 'generated_html') or not project.generated_html:
            return HttpResponse("No generated website content found.", status=404)
        
        # Return the generated HTML directly
        return HttpResponse(project.generated_html, content_type='text/html')
        
    except Exception as e:
        return HttpResponse(f"Error loading website: {str(e)}", status=500)


# Add these to your existing views.py or create a new views file
# Don't forget to add the URL patterns!