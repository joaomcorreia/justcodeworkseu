from django.shortcuts import render, get_object_or_404
from django.http import Http404
from tenants.models import Tenant, Domain
from websites.views import get_sidebar_context


def get_tenant_from_request(request):
    """Get tenant from request domain"""
    host = request.get_host().split(':')[0]  # Remove port if present
    
    try:
        domain = Domain.objects.get(domain=host)
        return domain.tenant
    except Domain.DoesNotExist:
        return None


def get_customer_context(tenant):
    """Get context data for customer tenant"""
    return {
        'company_name': tenant.company_name,
        'contact_email': tenant.contact_email,
        'phone': tenant.phone,
        'tenant': tenant,
        'is_customer_site': True,
    }


# Customer Site Views (based on tenant subdomain)
def customer_home(request, tenant):
    """Customer home page - template depends on tenant settings"""
    context = get_customer_context(tenant)
    context.update(get_sidebar_context())
    
    # Determine template based on tenant (in real app, store template choice in DB)
    if 'vakwerk' in tenant.schema_name or 'bouw' in tenant.schema_name or 'schilder' in tenant.schema_name:
        # Construction companies use TP2
        context.update({
            'projects_completed': '200+',
            'years_experience': '15+',
            'satisfaction_rate': '98%',
        })
        return render(request, 'website/tp2/home.html', context)
    else:
        # Tech companies use TP1
        context.update({
            'projects_completed': '150+',
            'happy_clients': '120+',
            'years_experience': '8+',
        })
        return render(request, 'website/tp1/home.html', context)


def customer_about(request, tenant):
    """Customer about page"""
    context = get_customer_context(tenant)
    context.update(get_sidebar_context())
    
    if 'vakwerk' in tenant.schema_name or 'bouw' in tenant.schema_name or 'schilder' in tenant.schema_name:
        # Construction companies
        context.update({
            'founding_year': '2008',
            'years_experience': '15+',
            'team_member_1_name': 'Jan van der Berg',
            'team_member_1_role': 'Eigenaar & Projectleider',
            'team_member_2_name': 'Piet Bakker',
            'team_member_2_role': 'Hoofd Schilder',
        })
        return render(request, 'website/tp2/about.html', context)
    else:
        # Tech companies
        return render(request, 'website/tp1/about.html', context)


def customer_services(request, tenant):
    """Customer services page"""
    context = get_customer_context(tenant)
    context.update(get_sidebar_context())
    
    if 'vakwerk' in tenant.schema_name or 'bouw' in tenant.schema_name or 'schilder' in tenant.schema_name:
        return render(request, 'website/tp2/services.html', context)
    else:
        return render(request, 'website/tp1/services.html', context)


def customer_portfolio(request, tenant):
    """Customer portfolio page"""
    context = get_customer_context(tenant)
    context.update(get_sidebar_context())
    
    if 'vakwerk' in tenant.schema_name or 'bouw' in tenant.schema_name or 'schilder' in tenant.schema_name:
        return render(request, 'website/tp2/portfolio.html', context)
    else:
        return render(request, 'website/tp1/portfolio.html', context)


def customer_contact(request, tenant):
    """Customer contact page"""
    context = get_customer_context(tenant)
    context.update(get_sidebar_context())
    
    if 'vakwerk' in tenant.schema_name or 'bouw' in tenant.schema_name or 'schilder' in tenant.schema_name:
        return render(request, 'website/tp2/contact.html', context)
    else:
        return render(request, 'website/tp1/contact.html', context)


def customer_quote(request, tenant):
    """Customer quote page"""
    context = get_customer_context(tenant)
    context.update(get_sidebar_context())
    
    # Always use TP1 quote page for now (can be customized later)
    return render(request, 'website/tp1/quote.html', context)
