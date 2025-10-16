"""
Public views for JustCodeWorks.EU homepage and public pages
"""
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os
import json

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


def websites_page(request):
    """
    Dedicated websites page view
    """
    context = {
        'page_title': 'Professional Website Builder - JustCodeWorks.EU',
        'company_name': 'JustCodeWorks.EU',
    }
    return render(request, 'public/static/websites.html', context)


def prints_page(request):
    """
    Print services page - where customers order prints
    """
    context = {
        'page_title': 'Print Services - JustCodeWorks.EU',
        'company_name': 'JustCodeWorks.EU',
    }
    return render(request, 'public/static/prints.html', context)


@csrf_exempt
def submit_print_order(request):
    """
    Handle print order form submissions
    """
    if request.method == 'POST':
        try:
            from django.core.mail import send_mail
            
            # Get form data
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['customer_name', 'customer_email', 'print_service']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'success': False, 
                        'message': f'{field.replace("_", " ").title()} is required'
                    })
            
            # Prepare email content
            email_subject = f"Print Order Request - {data.get('print_service', 'Unknown')}"
            email_body = f"""
New Print Order Request

Customer Information:
- Name: {data.get('customer_name')}
- Email: {data.get('customer_email')}
- Phone: {data.get('customer_phone', 'Not provided')}

Order Details:
- Service: {data.get('print_service')}
- Quantity: {data.get('quantity', 'Not specified')}
- Size/Format: {data.get('print_size', 'Not specified')}

Project Details:
{data.get('project_details', 'No additional details provided')}

Delivery Address:
{data.get('delivery_address', 'Not provided')}

Please respond to the customer within 24 hours with pricing and timeline.
            """
            
            # Send email notification (you can configure this later)
            try:
                # For now, just log the order (replace with actual email sending)
                print(f"Print order received from {data.get('customer_email')}")
                print(email_body)
                
                # In production, uncomment this:
                # send_mail(
                #     email_subject,
                #     email_body,
                #     'noreply@justcodeworks.eu',
                #     ['prints@justcodeworks.eu'],
                #     fail_silently=False,
                # )
                
            except Exception as e:
                print(f"Email send error: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you! Your print order request has been received. We will contact you within 24 hours with a quote.'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid form data'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


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


@require_http_methods(["GET"])
def robots_txt(request):
    """
    Serve robots.txt file to block search engines from development site
    """
    robots_path = os.path.join(settings.BASE_DIR, 'robots.txt')
    try:
        with open(robots_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        # Fallback content if file is missing
        content = "User-agent: *\nDisallow: /"
        return HttpResponse(content, content_type='text/plain')