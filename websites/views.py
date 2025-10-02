from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .models import Website, Page, HomeSlider, Settings
from .forms import WebsiteForm, PageForm, HomeSliderForm, SettingsForm


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
