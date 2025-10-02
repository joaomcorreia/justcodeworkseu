from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def coming_soon_view(request):
    """
    Coming soon page for non-authenticated users
    """
    context = {
        'site_name': 'JustCodeWorks.EU',
        'tagline': 'AI-Powered Website Builder',
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
    
    context = {
        'site_name': 'JustCodeWorks.EU',
        'tagline': 'Build AI-Powered Websites in Minutes',
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
