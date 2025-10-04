from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import re
import random
from tenants.models import Tenant, Domain


def signup_step1(request):
    """Step 1: Collect business information"""
    return render(request, 'signup/step1.html')


def signup_step2(request):
    """Step 2: Domain selection with suggestions"""
    if request.method == 'POST':
        # Get business details from form
        business_name = request.POST.get('business_name', '').strip()
        business_type = request.POST.get('business_type', '').strip()
        
        if not business_name:
            messages.error(request, 'Business name is required')
            return redirect('signup_step1')
            
        # Generate domain suggestions
        suggestions = generate_domain_suggestions(business_name, business_type)
        
        # Store business details in session
        request.session['signup_data'] = {
            'business_name': business_name,
            'business_type': business_type,
            'contact_name': request.POST.get('contact_name', ''),
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', ''),
            'description': request.POST.get('description', ''),
        }
        
        context = {
            'business_name': business_name,
            'suggestions': suggestions,
        }
        return render(request, 'signup/step2.html', context)
    
    return redirect('signup_step1')


def signup_step3(request):
    """Step 3: Template selection"""
    if request.method == 'POST':
        selected_domain = request.POST.get('selected_domain')
        
        if not selected_domain:
            messages.error(request, 'Please select a domain name')
            return redirect('signup_step2')
            
        # Store selected domain
        signup_data = request.session.get('signup_data', {})
        signup_data['selected_domain'] = selected_domain
        request.session['signup_data'] = signup_data
        
        context = {
            'selected_domain': selected_domain,
            'business_name': signup_data.get('business_name', ''),
        }
        return render(request, 'signup/step3.html', context)
    
    return redirect('signup_step1')


def signup_complete(request):
    """Final step: Create tenant and redirect to new website"""
    if request.method == 'POST':
        selected_template = request.POST.get('selected_template')
        signup_data = request.session.get('signup_data')
        
        if not signup_data or not selected_template:
            messages.error(request, 'Invalid signup data')
            return redirect('signup_step1')
            
        try:
            # Create the tenant automatically
            tenant = create_tenant_from_signup(signup_data, selected_template)
            
            # Clear signup session
            del request.session['signup_data']
            
            # Success! Redirect to their new website
            subdomain_url = f"http://{signup_data['selected_domain']}"
            if request.get_host().split(':')[0] == 'localhost' or '127.0.0.1' in request.get_host():
                # For local development, add port
                subdomain_url = f"http://{signup_data['selected_domain']}:8000"
            
            context = {
                'tenant': tenant,
                'subdomain_url': subdomain_url,
                'admin_url': f"{subdomain_url}/admin/",
                'business_name': signup_data['business_name'],
            }
            return render(request, 'signup/success.html', context)
            
        except Exception as e:
            messages.error(request, f'Error creating website: {str(e)}')
            return redirect('signup_step1')
    
    return redirect('signup_step1')


def generate_domain_suggestions(business_name, business_type):
    """Generate domain name suggestions based on business info"""
    # Clean business name for domain use
    clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', business_name.lower())
    words = clean_name.split()
    
    suggestions = []
    base_domain = "justcodeworks.eu"
    
    # Strategy 1: Full name (if single word or short)
    if len(words) == 1 and len(words[0]) <= 15:
        suggestions.append(f"{words[0]}.{base_domain}")
    elif len(words) == 2 and len(''.join(words)) <= 15:
        suggestions.append(f"{''.join(words)}.{base_domain}")
    
    # Strategy 2: Abbreviated versions
    if len(words) >= 2:
        # First letters of each word
        abbreviation = ''.join([w[0] for w in words if w])
        if len(abbreviation) >= 2:
            suggestions.append(f"{abbreviation}.{base_domain}")
        
        # First word + first letter of others
        first_plus = words[0] + ''.join([w[0] for w in words[1:] if w])
        if len(first_plus) <= 15:
            suggestions.append(f"{first_plus}.{base_domain}")
    
    # Strategy 3: Business type combinations
    type_suffixes = {
        'construction': ['bouw', 'pro', 'werk'],
        'technology': ['tech', 'pro', 'solutions'],
        'consulting': ['consulting', 'adviseurs', 'experts'],
        'retail': ['shop', 'store', 'online'],
        'restaurant': ['restaurant', 'eten', 'food'],
        'healthcare': ['zorg', 'health', 'medical'],
        'education': ['education', 'learning', 'academy'],
    }
    
    if business_type.lower() in type_suffixes:
        for suffix in type_suffixes[business_type.lower()]:
            if words:
                combo = f"{words[0]}{suffix}"
                if len(combo) <= 15:
                    suggestions.append(f"{combo}.{base_domain}")
    
    # Strategy 4: Add common suffixes
    common_suffixes = ['pro', 'plus', 'online', 'digital', 'eu']
    if words:
        for suffix in common_suffixes:
            combo = f"{words[0]}{suffix}"
            if len(combo) <= 15:
                suggestions.append(f"{combo}.{base_domain}")
    
    # Remove duplicates and check availability
    suggestions = list(dict.fromkeys(suggestions))  # Remove duplicates
    available_suggestions = []
    
    for suggestion in suggestions[:8]:  # Limit to 8 suggestions
        if not Domain.objects.filter(domain=suggestion).exists():
            available_suggestions.append({
                'domain': suggestion,
                'available': True,
                'recommendation': get_recommendation_reason(suggestion, business_name, business_type)
            })
        else:
            available_suggestions.append({
                'domain': suggestion,
                'available': False,
                'recommendation': 'Already taken'
            })
    
    # If we don't have enough available suggestions, add numbered versions
    while len([s for s in available_suggestions if s['available']]) < 3:
        if words:
            for i in range(2, 10):
                numbered = f"{words[0]}{i}.{base_domain}"
                if not Domain.objects.filter(domain=numbered).exists() and numbered not in [s['domain'] for s in available_suggestions]:
                    available_suggestions.append({
                        'domain': numbered,
                        'available': True,
                        'recommendation': f'Alternative with number'
                    })
                    if len([s for s in available_suggestions if s['available']]) >= 3:
                        break
            break
    
    return available_suggestions


def get_recommendation_reason(domain, business_name, business_type):
    """Get a recommendation reason for a domain suggestion"""
    reasons = [
        "Short and memorable",
        "Matches your business name",
        "Professional sounding", 
        "Easy to remember",
        "Great for branding",
        "Industry-appropriate",
        "Clean and simple",
        "Perfect for your business"
    ]
    return random.choice(reasons)


def create_tenant_from_signup(signup_data, template_type):
    """Create a new tenant from signup data"""
    business_name = signup_data['business_name']
    selected_domain = signup_data['selected_domain']
    
    # Create schema name from domain (remove .justcodeworks.eu)
    schema_name = selected_domain.replace('.justcodeworks.eu', '').replace('-', '').replace('.', '')
    
    # Ensure unique schema name
    counter = 1
    base_schema = schema_name
    while Tenant.objects.filter(schema_name=schema_name).exists():
        schema_name = f"{base_schema}{counter}"
        counter += 1
    
    # Create tenant
    tenant = Tenant.objects.create(
        schema_name=schema_name,
        company_name=business_name,
        contact_email=signup_data.get('email', ''),
        phone=signup_data.get('phone', ''),
        description=signup_data.get('description', ''),
        template_type=template_type,
        is_active=True,
    )
    
    # Create domain mapping
    Domain.objects.create(
        domain=selected_domain,
        tenant=tenant,
        is_primary=True,
    )
    
    return tenant