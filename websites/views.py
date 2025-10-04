from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .models import Website, Page, HomeSlider, Settings
from .forms import WebsiteForm, PageForm, HomeSliderForm, SettingsForm


def get_sidebar_context():
    """Helper function to get sidebar widget data"""
    return {
        'sidebar_services': [
            {
                'name': 'Web Design',
                'slug': 'web-design',
                'icon': 'bi-palette',
                'description': 'Custom website design and development'
            },
            {
                'name': 'Digital Marketing',
                'slug': 'digital-marketing',
                'icon': 'bi-graph-up',
                'description': 'SEO, social media, and online advertising'
            },
            {
                'name': 'Branding',
                'slug': 'branding',
                'icon': 'bi-award',
                'description': 'Logo design and brand identity'
            },
            {
                'name': 'E-commerce',
                'slug': 'e-commerce',
                'icon': 'bi-cart',
                'description': 'Online store development'
            }
        ],
        'sidebar_contact': {
            'phone': '+420 123 456 789',
            'email': 'info@justcodeworks.eu',
            'address': 'Prague, Czech Republic',
            'hours': 'Mon-Fri: 9:00-17:00',
            'whatsapp_number': '+420123456789'
        },
        'sidebar_portfolio': [
            {'image': 'portfolio/web1.jpg', 'title': 'Corporate Website'},
            {'image': 'portfolio/web2.jpg', 'title': 'E-commerce Store'},
            {'image': 'portfolio/web3.jpg', 'title': 'Portfolio Site'},
            {'image': 'portfolio/web4.jpg', 'title': 'Restaurant Website'},
            {'image': 'portfolio/web5.jpg', 'title': 'Tech Startup'},
            {'image': 'portfolio/web6.jpg', 'title': 'Creative Agency'}
        ],
        'sidebar_announcements': [
            {
                'title': 'New AI Website Builder Launched',
                'date': '2024-01-15',
                'excerpt': 'Create professional websites using our AI-powered platform...',
                'link': '#'
            },
            {
                'title': 'EU Grant Program Available',
                'date': '2024-01-10',
                'excerpt': 'Apply for digital transformation grants for SMEs...',
                'link': '#'
            },
            {
                'title': 'Free SEO Audit Offer',
                'date': '2024-01-05',
                'excerpt': 'Get a comprehensive SEO analysis for your website...',
                'link': '#'
            }
        ]
    }


@login_required
def tenant_dashboard(request):
    """Dashboard overview for tenant"""
    website = Website.objects.filter(owner=request.user).first()
    if not website:
        # Create default website for user
        website = Website.objects.create(
            name=f"{request.user.username}'s Website",
            owner=request.user,
            domain=f"{request.user.username}.example.com"
        )
    
    pages_count = Page.objects.filter(website=website).count()
    published_pages = Page.objects.filter(website=website, is_published=True).count()
    
    context = {
        'website': website,
        'pages_count': pages_count,
        'published_pages': published_pages,
        'recent_pages': Page.objects.filter(website=website).order_by('-updated_at')[:5],
    }
    return render(request, 'admin/tenant_dashboard.html', context)


@login_required
def edit_homepage(request):
    """Edit homepage content"""
    website = get_object_or_404(Website, owner=request.user)
    homepage, created = Page.objects.get_or_create(
        website=website,
        is_homepage=True,
        defaults={'title': 'Home', 'slug': 'home'}
    )
    
    if request.method == 'POST':
        form = PageForm(request.POST, instance=homepage)
        if form.is_valid():
            form.save()
            messages.success(request, 'Homepage updated successfully!')
            return redirect('edit_homepage')
    else:
        form = PageForm(instance=homepage)
    
    context = {
        'form': form,
        'page': homepage,
        'website': website,
    }
    return render(request, 'admin/edit_homepage.html', context)


@login_required
def subscription_overview(request):
    """Subscription overview"""
    website = get_object_or_404(Website, owner=request.user)
    
    context = {
        'website': website,
        'plan_features': {
            'free': ['1 Website', 'Basic Templates', 'Community Support'],
            'basic': ['5 Websites', 'Premium Templates', 'Email Support', 'Custom Domain'],
            'premium': ['Unlimited Websites', 'All Templates', 'Priority Support', 'AI Features'],
            'enterprise': ['Everything in Premium', 'White Label', 'API Access', 'Dedicated Support']
        }
    }
    return render(request, 'admin/subscription_overview.html', context)


@login_required
def domain_settings(request):
    """Domain settings"""
    website = get_object_or_404(Website, owner=request.user)
    
    if request.method == 'POST':
        domain = request.POST.get('domain')
        if domain:
            website.domain = domain
            website.save()
            messages.success(request, 'Domain updated successfully!')
            return redirect('domain_settings')
    
    context = {'website': website}
    return render(request, 'admin/domain_settings.html', context)


@login_required
def hosting_settings(request):
    """Hosting settings"""
    website = get_object_or_404(Website, owner=request.user)
    context = {'website': website}
    return render(request, 'admin/hosting_settings.html', context)


@login_required
def website_settings(request):
    """Website settings"""
    website = get_object_or_404(Website, owner=request.user)
    settings, created = Settings.objects.get_or_create(website=website)
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('website_settings')
    else:
        form = SettingsForm(instance=settings)
    
    context = {
        'website': website,
        'form': form,
    }
    return render(request, 'admin/website_settings.html', context)


@login_required
def seo_settings(request):
    """SEO settings"""
    website = get_object_or_404(Website, owner=request.user)
    
    if request.method == 'POST':
        website.meta_title = request.POST.get('meta_title', '')
        website.meta_description = request.POST.get('meta_description', '')
        website.meta_keywords = request.POST.get('meta_keywords', '')
        website.save()
        messages.success(request, 'SEO settings updated successfully!')
        return redirect('seo_settings')
    
    context = {'website': website}
    return render(request, 'admin/seo_settings.html', context)


@login_required
def social_networks(request):
    """Social networks settings"""
    website = get_object_or_404(Website, owner=request.user)
    settings, created = Settings.objects.get_or_create(website=website)
    
    if request.method == 'POST':
        settings.facebook_url = request.POST.get('facebook_url', '')
        settings.twitter_url = request.POST.get('twitter_url', '')
        settings.linkedin_url = request.POST.get('linkedin_url', '')
        settings.instagram_url = request.POST.get('instagram_url', '')
        settings.save()
        messages.success(request, 'Social network settings updated successfully!')
        return redirect('social_networks')
    
    context = {
        'website': website,
        'settings': settings,
    }
    return render(request, 'admin/social_networks.html', context)


@login_required
def ai_overview(request):
    """AI features overview"""
    website = get_object_or_404(Website, owner=request.user)
    context = {'website': website}
    return render(request, 'admin/ai_overview.html', context)


@login_required
def ai_content_generator(request):
    """AI content generator"""
    website = get_object_or_404(Website, owner=request.user)
    context = {'website': website}
    return render(request, 'admin/ai_content_generator.html', context)


@login_required
def ai_design_assistant(request):
    """AI design assistant"""
    website = get_object_or_404(Website, owner=request.user)
    context = {'website': website}
    return render(request, 'admin/ai_design_assistant.html', context)


@login_required
def google_analytics(request):
    """Google Analytics settings"""
    website = get_object_or_404(Website, owner=request.user)
    settings, created = Settings.objects.get_or_create(website=website)
    
    if request.method == 'POST':
        settings.google_analytics_id = request.POST.get('google_analytics_id', '')
        settings.save()
        messages.success(request, 'Google Analytics settings updated successfully!')
        return redirect('google_analytics')
    
    context = {
        'website': website,
        'settings': settings,
    }
    return render(request, 'admin/google_analytics.html', context)


@login_required
def facebook_insights(request):
    """Facebook Insights settings"""
    website = get_object_or_404(Website, owner=request.user)
    settings, created = Settings.objects.get_or_create(website=website)
    
    if request.method == 'POST':
        settings.facebook_pixel_id = request.POST.get('facebook_pixel_id', '')
        settings.save()
        messages.success(request, 'Facebook Pixel settings updated successfully!')
        return redirect('facebook_insights')
    
    context = {
        'website': website,
        'settings': settings,
    }
    return render(request, 'admin/facebook_insights.html', context)


@login_required
def visitor_stats(request):
    """Visitor statistics"""
    website = get_object_or_404(Website, owner=request.user)
    context = {'website': website}
    return render(request, 'admin/visitor_stats.html', context)


@login_required
def profile_settings(request):
    """User profile settings"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_settings')
    
    context = {'user': request.user}
    return render(request, 'admin/profile_settings.html', context)


@login_required
def user_management(request):
    """User management"""
    website = get_object_or_404(Website, owner=request.user)
    context = {'website': website}
    return render(request, 'admin/user_management.html', context)


@login_required
def qr_maker(request):
    """QR Code maker tool"""
    context = {}
    return render(request, 'admin/qr_maker.html', context)


@login_required
def image_resizer(request):
    """Image resizer tool"""
    context = {}
    return render(request, 'admin/image_resizer.html', context)


@login_required
def backup_restore(request):
    """Backup and restore"""
    website = get_object_or_404(Website, owner=request.user)
    context = {'website': website}
    return render(request, 'admin/backup_restore.html', context)


@login_required
def website_preview(request):
    """Preview the live website"""
    website = get_object_or_404(Website, owner=request.user)
    homepage = Page.objects.filter(website=website, is_homepage=True).first()
    
    context = {
        'website': website,
        'homepage': homepage,
        'slider_items': HomeSlider.objects.filter(website=website, is_active=True),
    }
    return render(request, 'website/preview.html', context)


def home_page(request):
    """Home page for customer websites"""
    context = {
        'company_name': 'JustCodeWorks.EU',
        'projects_completed': '150+',
        'happy_clients': '120+',
        'years_experience': '8+',
        'page_title': 'Professional Web Solutions',
        'page_description': 'Create stunning websites and digital experiences that help your business grow.',
    }
    # Add sidebar data
    context.update(get_sidebar_context())
    return render(request, 'website/tp1/home.html', context)


def about_page(request):
    """About page for customer websites"""
    # Get tenant-specific settings (in future, this will come from Settings model)
    # For simple setup without tenants, use default values
    context = {
        'company_name': 'JustCodeWorks.EU',
        'about_title': 'About Our Company',
        'about_description': 'We are a professional company dedicated to providing excellent services to our clients.',
        'years_experience': '10+',
        'projects_completed': '500+',
        'mission_text': 'To provide exceptional services that exceed our clients\' expectations while maintaining the highest standards of quality.',
        'vision_text': 'To be the leading company in our industry, recognized for innovation, quality, and customer satisfaction.',
    }
    # Add sidebar data
    context.update(get_sidebar_context())
    return render(request, 'website/tp1/about.html', context)


def portfolio_page(request):
    """Portfolio page showcasing projects and image editing capabilities"""
    context = {
        'company_name': 'JustCodeWorks.EU',
        'projects_completed': '150+',
        'happy_clients': '120+',
        'years_experience': '8+',
        'awards_won': '12',
        'page_title': 'Our Portfolio',
        'page_description': 'Browse our collection of web design, branding, and digital projects.',
    }
    # Add sidebar data
    context.update(get_sidebar_context())
    return render(request, 'website/tp1/portfolio.html', context)


def contact_page(request):
    """Contact page with form and business information"""
    context = {
        'company_name': 'JustCodeWorks.EU',
        'company_phone': '+31 6 1234 5678',
        'company_email': 'info@justcodeworks.eu',
        'company_address': '1234 Innovation District<br>Amsterdam, Netherlands',
        'company_website': 'www.justcodeworks.eu',
        'page_title': 'Contact Us',
        'page_description': 'Get in touch with our team for your next web project.',
    }
    # Add sidebar data
    context.update(get_sidebar_context())
    return render(request, 'website/tp1/contact.html', context)


def quote_page(request):
    """Advanced quote form with multi-step wizard"""
    if request.method == 'POST':
        # Handle form submission (for now, just redirect back with success)
        # In a real implementation, this would save to database and send emails
        return render(request, 'website/tp1/quote.html', {
            'company_name': 'JustCodeWorks.EU',
            'success': True,
            **get_sidebar_context()
        })
    
    context = {
        'company_name': 'JustCodeWorks.EU',
        'page_title': 'Get Quote',
        'page_description': 'Get a detailed quote for your project with our advanced quote wizard.',
    }
    # Add sidebar data
    context.update(get_sidebar_context())
    return render(request, 'website/tp1/quote.html', context)


def services_page(request):
    """Services page showcasing all offerings"""
    context = {
        'company_name': 'JustCodeWorks.EU',
        'services_offered': '6',
        'projects_delivered': '150+',
        'satisfaction_rate': '98%',
        'page_title': 'Our Services',
        'page_description': 'Comprehensive digital solutions for your business growth.',
    }
    # Add sidebar data
    context.update(get_sidebar_context())
    return render(request, 'website/tp1/services.html', context)


def service_detail_page(request, service_slug):
    """Service detail page with pricing and features"""
    # Service data (in real app, this would come from database)
    services_data = {
        'web-design': {
            'title': 'Web Design',
            'slug': 'web-design',
            'icon': 'bi bi-palette-fill',
            'description': 'Beautiful, responsive websites that convert visitors into customers. Custom designs tailored to your brand and business goals.',
            'features': []  # Using default features in template
        },
        'web-development': {
            'title': 'Web Development',
            'slug': 'web-development', 
            'icon': 'bi bi-code-slash',
            'description': 'Robust, scalable web applications built with modern technologies. From simple sites to complex platforms.',
            'features': []
        },
        'ecommerce': {
            'title': 'E-commerce Solutions',
            'slug': 'ecommerce',
            'icon': 'bi bi-cart-fill',
            'description': 'Complete online stores with payment processing, inventory management, and marketing tools to boost your sales.',
            'features': []
        },
        'seo': {
            'title': 'SEO & Marketing',
            'slug': 'seo',
            'icon': 'bi bi-search',
            'description': 'Improve your search rankings and drive organic traffic with our comprehensive SEO and digital marketing services.',
            'features': []
        },
        'branding': {
            'title': 'Branding & Logo Design',
            'slug': 'branding',
            'icon': 'bi bi-award-fill',
            'description': 'Create a memorable brand identity that resonates with your audience. From logos to complete brand guidelines.',
            'features': []
        },
        'maintenance': {
            'title': 'Website Maintenance',
            'slug': 'maintenance',
            'icon': 'bi bi-tools',
            'description': 'Keep your website secure, updated, and performing at its best with our comprehensive maintenance services.',
            'features': []
        }
    }
    
    service = services_data.get(service_slug)
    if not service:
        # Return 404 or redirect to services page
        from django.shortcuts import redirect
        return redirect('services')
    
    context = {
        'company_name': 'JustCodeWorks.EU',
        'service': service,
        'page_title': service['title'],
        'page_description': service['description'],
    }
    # Add sidebar data
    context.update(get_sidebar_context())
    return render(request, 'website/tp1/service-detail.html', context)


# TP2 Template Views (Dutch Construction Theme)
def tp2_home(request):
    """TP2 Home page - Dutch construction services theme"""
    context = {
        'company_name': 'VakWerk Pro',
        'projects_completed': '200+',
        'years_experience': '15+',
        'satisfaction_rate': '98%',
    }
    context.update(get_sidebar_context())
    return render(request, 'website/tp2/home.html', context)

def tp2_about(request):
    """TP2 About page"""
    context = {
        'company_name': 'VakWerk Pro',
        'founding_year': '2008',
        'years_experience': '15+',
        'team_member_1_name': 'Jan van der Berg',
        'team_member_1_role': 'Eigenaar & Projectleider',
        'team_member_2_name': 'Piet Bakker',
        'team_member_2_role': 'Hoofd Schilder',
    }
    context.update(get_sidebar_context())
    return render(request, 'website/tp2/about.html', context)

def tp2_services(request):
    """TP2 Services page"""
    context = {
        'company_name': 'VakWerk Pro',
    }
    context.update(get_sidebar_context())
    return render(request, 'website/tp2/services.html', context)

def tp2_portfolio(request):
    """TP2 Portfolio page"""
    context = {
        'company_name': 'VakWerk Pro',
    }
    context.update(get_sidebar_context())
    return render(request, 'website/tp2/portfolio.html', context)

def tp2_contact(request):
    """TP2 Contact page"""
    context = {
        'company_name': 'VakWerk Pro',
    }
    context.update(get_sidebar_context())
    return render(request, 'website/tp2/contact.html', context)


# Customer Admin Interface
@login_required
def customer_admin_home(request):
    """Customer admin dashboard"""
    context = {
        'company_name': 'Customer Portal',
        'user': request.user,
    }
    return render(request, 'website/customer-admin/dashboard.html', context)

@login_required 
def customer_template_selection(request):
    """Template selection for customer"""
    templates = [
        {
            'id': 'tp1',
            'name': 'Professional Tech',
            'description': 'Modern template for tech companies and agencies',
            'preview_url': '/tp1/',
            'thumbnail': 'templates/tp1-thumb.jpg',
            'features': ['Multi-page layout', 'Quote system', 'Portfolio showcase', 'Contact forms']
        },
        {
            'id': 'tp2', 
            'name': 'Construction Pro',
            'description': 'Perfect template for construction and service companies',
            'preview_url': '/tp2/',
            'thumbnail': 'templates/tp2-thumb.jpg',
            'features': ['Dutch language', 'Service showcase', 'Project portfolio', 'Quote modal']
        }
    ]
    
    context = {
        'templates': templates,
        'company_name': 'Template Selection',
    }
    return render(request, 'website/customer-admin/template-selection.html', context)
