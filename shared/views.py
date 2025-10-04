from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_tenants.utils import get_tenant_model
from websites.views import (
    home_page, about_page, services_page, portfolio_page, 
    contact_page, quote_page, service_detail_page,
    tp2_home, tp2_about, tp2_services, tp2_portfolio, tp2_contact,
    get_sidebar_context
)


# Template routing functions
def route_template_request(request, template_path):
    """Route template requests based on path"""
    
    # TP1 Routes (JustCodeWorks theme)
    if template_path == '' or template_path == 'tp1/':
        return home_page(request)
    elif template_path == 'about/':
        return about_page(request)
    elif template_path == 'services/':
        return services_page(request)
    elif template_path == 'portfolio/':
        return portfolio_page(request)
    elif template_path == 'contact/':
        return contact_page(request)
    elif template_path == 'get-quote/':
        return quote_page(request)
    elif template_path.startswith('services/'):
        service_slug = template_path.replace('services/', '').rstrip('/')
        return service_detail_page(request, service_slug)
    
    # TP2 Routes (Dutch Construction theme)  
    elif template_path == 'tp2/':
        return tp2_home(request)
    elif template_path == 'tp2/about/':
        return tp2_about(request)
    elif template_path == 'tp2/services/':
        return tp2_services(request)
    elif template_path == 'tp2/portfolio/':
        return tp2_portfolio(request)
    elif template_path == 'tp2/contact/':
        return tp2_contact(request)
    
    else:
        # Default to home if no match
        return home_page(request)


def coming_soon_view(request):
    """
    Coming soon page for non-authenticated users
    """
    # Get the current tenant to display their company name
    tenant = getattr(request, 'tenant', None)
    
    if tenant and hasattr(tenant, 'company_name') and tenant.company_name:
        site_name = tenant.company_name
        tagline = f'Powered by JustCodeWorks.EU'
    else:
        site_name = 'JustCodeWorks.EU'
        tagline = 'AI-Powered Website Builder'
    
    context = {
        'site_name': site_name,
        'tagline': tagline,
        'description': 'We\'re building something amazing. Join our waitlist to be the first to know when we launch!',
        'launch_date': '2025-12-01',  # Estimated launch date
    }
    return render(request, 'main_site/coming_soon.html', context)


def main_site_view(request):
    """
    Main website view for justcodeworks.eu
    Shows coming soon page for non-authenticated users
    """
    # Redirect non-authenticated users to coming soon page
    if not request.user.is_authenticated:
        return redirect('coming_soon')
    
    # Get the current tenant to display their company name
    tenant = getattr(request, 'tenant', None)
    
    if tenant and hasattr(tenant, 'company_name') and tenant.company_name:
        site_name = tenant.company_name
        tagline = f'Powered by JustCodeWorks.EU'
    else:
        site_name = 'JustCodeWorks.EU'
        tagline = 'Build AI-Powered Websites in Minutes'
    
    context = {
        'site_name': site_name,
        'tagline': tagline,
        'description': 'Create stunning websites with the power of AI. No coding required.',
        'features': [
            {
                'title': 'AI-Powered Design',
                'description': 'Let AI create beautiful designs tailored to your business',
                'icon': 'fas fa-magic'
            },
            {
                'title': 'Easy Management',
                'description': 'Intuitive admin interface to manage your entire website',
                'icon': 'fas fa-cog'
            },
            {
                'title': 'Multi-Tenant',
                'description': 'Each user gets their own dedicated website space',
                'icon': 'fas fa-users'
            },
            {
                'title': 'SEO Optimized',
                'description': 'Built-in SEO tools to help your website rank better',
                'icon': 'fas fa-chart-line'
            }
        ]
    }
    return render(request, 'main_site/index.html', context)
