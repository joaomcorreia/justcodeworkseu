from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from tenants.models import Tenant
from tenants.views import get_tenant_from_request, get_customer_context


@login_required
def customer_admin_dashboard(request):
    """Customer admin dashboard"""
    tenant = get_tenant_from_request(request) or get_test_tenant(request)
    
    if not tenant:
        messages.error(request, "Customer site not found")
        return redirect('/')
    
    context = get_customer_context(tenant)
    context.update({
        'user': request.user,
        'page_title': f'{tenant.company_name} - Admin Dashboard',
        'stats': {
            'views_today': 127,
            'total_views': 1234,
            'inquiries_today': 5,
            'total_inquiries': 89,
            'quote_requests': 23,
            'conversion_rate': '15%'
        }
    })
    
    return render(request, 'customer-admin/dashboard.html', context)


@login_required
def customer_edit_homepage(request):
    """Edit customer homepage content"""
    tenant = get_tenant_from_request(request) or get_test_tenant(request)
    
    if not tenant:
        messages.error(request, "Customer site not found")
        return redirect('/')
    
    if request.method == 'POST':
        # Handle homepage updates
        tenant.company_name = request.POST.get('company_name', tenant.company_name)
        tenant.contact_email = request.POST.get('contact_email', tenant.contact_email)
        tenant.phone = request.POST.get('phone', tenant.phone)
        tenant.description = request.POST.get('description', tenant.description)
        tenant.save()
        
        messages.success(request, 'Homepage updated successfully!')
        return redirect('customer_edit_homepage')
    
    context = get_customer_context(tenant)
    context.update({
        'page_title': f'Edit Homepage - {tenant.company_name}',
        'edit_mode': True,
    })
    
    return render(request, 'customer-admin/edit-homepage.html', context)


@login_required 
def customer_edit_services(request):
    """Edit customer services"""
    tenant = get_tenant_from_request(request) or get_test_tenant(request)
    
    if not tenant:
        messages.error(request, "Customer site not found")
        return redirect('/')
    
    # Sample services data (in real app, this would be in database)
    if 'vakwerk' in tenant.schema_name or 'bouw' in tenant.schema_name or 'schilder' in tenant.schema_name:
        services = [
            {
                'id': 1,
                'name': 'Schilderwerk',
                'description': 'Professioneel binnen- en buitenschilderwerk',
                'price_range': '€25-50 per m²',
                'active': True
            },
            {
                'id': 2,
                'name': 'Elektrotechniek',
                'description': 'Elektrotechnische installaties en reparaties',
                'price_range': '€45-80 per uur',
                'active': True
            },
            {
                'id': 3,
                'name': 'Tegelwerk',
                'description': 'Badkamer en keuken tegelwerk',
                'price_range': '€30-60 per m²',
                'active': True
            }
        ]
    else:
        services = [
            {
                'id': 1,
                'name': 'Web Design',
                'description': 'Custom website design and development',
                'price_range': '€1500-5000',
                'active': True
            },
            {
                'id': 2,
                'name': 'SEO Optimization',
                'description': 'Search engine optimization services',
                'price_range': '€300-800/month',
                'active': True
            },
            {
                'id': 3,
                'name': 'Digital Marketing',
                'description': 'Online marketing and advertising',
                'price_range': '€500-2000/month',
                'active': True
            }
        ]
    
    context = get_customer_context(tenant)
    context.update({
        'page_title': f'Edit Services - {tenant.company_name}',
        'services': services,
    })
    
    return render(request, 'customer-admin/edit-services.html', context)


@login_required
def customer_edit_portfolio(request):
    """Edit customer portfolio"""
    tenant = get_tenant_from_request(request) or get_test_tenant(request)
    
    if not tenant:
        messages.error(request, "Customer site not found")
        return redirect('/')
    
    # Sample portfolio data
    if 'vakwerk' in tenant.schema_name or 'bouw' in tenant.schema_name or 'schilder' in tenant.schema_name:
        portfolio = [
            {
                'id': 1,
                'title': 'Woning Renovatie Amsterdam',
                'category': 'schilderwerk',
                'description': 'Complete buitenschilderwerk monumentaal pand',
                'date': '2024-03-01',
                'featured': True
            },
            {
                'id': 2,
                'title': 'Badkamer Renovatie Haarlem', 
                'category': 'tegelwerk',
                'description': 'Luxe badkamer met natuursteen',
                'date': '2024-01-15',
                'featured': False
            }
        ]
    else:
        portfolio = [
            {
                'id': 1,
                'title': 'E-commerce Website',
                'category': 'web-design',
                'description': 'Modern online store with payment integration',
                'date': '2024-02-15',
                'featured': True
            },
            {
                'id': 2,
                'title': 'Corporate Identity',
                'category': 'branding', 
                'description': 'Complete brand redesign and guidelines',
                'date': '2024-01-20',
                'featured': False
            }
        ]
    
    context = get_customer_context(tenant)
    context.update({
        'page_title': f'Edit Portfolio - {tenant.company_name}',
        'portfolio': portfolio,
    })
    
    return render(request, 'customer-admin/edit-portfolio.html', context)


@login_required
def customer_settings(request):
    """Customer website settings"""
    tenant = get_tenant_from_request(request) or get_test_tenant(request)
    
    if not tenant:
        messages.error(request, "Customer site not found")
        return redirect('/')
    
    context = get_customer_context(tenant)
    context.update({
        'page_title': f'Settings - {tenant.company_name}',
    })
    
    return render(request, 'customer-admin/settings.html', context)


def get_test_tenant(request):
    """Get tenant for testing via URL parameter"""
    customer_param = request.GET.get('customer')
    if customer_param:
        try:
            return Tenant.objects.get(schema_name=customer_param)
        except Tenant.DoesNotExist:
            pass
    return None