"""
Admin views for JustCodeWorks dashboard
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from pages.models import Page
from blog.models import Post, Category
from ai_assistant.models import Conversation, Message


@login_required
def admin_dashboard(request):
    """
    Main admin dashboard view with Website Builder integration
    """
    # Import Website Builder models
    try:
        from website_builder.models import WebsiteProject, WebsiteTemplate
        website_projects = WebsiteProject.objects.count()
        website_templates = WebsiteTemplate.objects.filter(is_active=True).count()
        recent_projects = WebsiteProject.objects.order_by('-created_at')[:5]
    except ImportError:
        website_projects = 0
        website_templates = 0
        recent_projects = []
    
    # Get basic stats
    context = {
        'total_pages': Page.objects.count() if hasattr(Page.objects, 'count') else 0,
        'total_posts': Post.objects.count() if hasattr(Post.objects, 'count') else 0,
        'total_conversations': Conversation.objects.count() if hasattr(Conversation.objects, 'count') else 0,
        'website_projects': website_projects,
        'website_templates': website_templates,
        'recent_projects': recent_projects,
        'page_title': 'Dashboard Overview',
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required
def pages_management(request):
    """
    Pages management view with real page data
    """
    # Get page statistics (mock data for now, replace with real queries later)
    context = {
        'page_title': 'Pages Management',
        'section': 'pages',
        'total_pages': 12,
        'published_pages': 8,
        'draft_pages': 3,
        'total_views': 1234,
    }
    return render(request, 'admin/pages.html', context)


@login_required
def blog_management(request):
    """
    Blog management view with real blog data
    """
    # Get blog statistics (mock data for now, replace with real queries later)
    context = {
        'page_title': 'Blog Management',
        'section': 'blog',
        'total_posts': 24,
        'published_posts': 18,
        'total_categories': 8,
        'total_comments': 156,
    }
    return render(request, 'admin/blog.html', context)


@login_required
def website_builder_management(request):
    """
    Website Builder management view - integrated with main admin
    """
    from website_builder.models import WebsiteProject, WebsiteTemplate
    
    # Get all website builder projects
    all_projects = WebsiteProject.objects.all().order_by('-created_at')
    user_projects = WebsiteProject.objects.filter(user=request.user).order_by('-created_at')
    
    # Get project statistics
    stats = {
        'total_projects': all_projects.count(),
        'user_projects': user_projects.count(),
        'completed_projects': all_projects.filter(status='completed').count(),
        'in_progress_projects': all_projects.filter(status__in=['draft', 'in_progress']).count(),
        'published_projects': all_projects.filter(status='published').count(),
        'templates_count': WebsiteTemplate.objects.filter(is_active=True).count(),
    }
    
    # Recent projects for quick access
    recent_projects = all_projects[:10]
    
    context = {
        'page_title': 'Website Builder Management',
        'section': 'website_builder',
        'stats': stats,
        'recent_projects': recent_projects,
        'user_projects': user_projects[:5],  # Show user's recent projects
    }
    
    return render(request, 'admin/website_builder.html', context)


@login_required
def website_builder_iframe(request):
    """Website Builder embedded iframe view"""
    return render(request, 'admin/website_builder_iframe_v2.html')


@login_required
def forms_management(request):
    """
    Forms management view with real form data
    """
    # Get form statistics (mock data for now, replace with real queries later)
    context = {
        'page_title': 'Forms Management',
        'section': 'forms',
        'active_forms': 6,
        'total_submissions': 142,
        'completion_rate': 89,
        'avg_time': '2m 15s',
    }
    return render(request, 'admin/forms.html', context)


@login_required
def ai_tools(request):
    """
    AI tools view
    """
    context = {
        'page_title': 'AI Content Generator',
        'section': 'ai-tools'
    }
    return render(request, 'admin/ai_tools.html', context)


@login_required
def print_materials(request):
    """
    Print materials view
    """
    context = {
        'page_title': 'Print Materials',
        'section': 'print-materials'
    }
    return render(request, 'admin/print_materials.html', context)


@login_required
def print_cards(request):
    """Print materials - Business cards management"""
    context = {
        'page_title': 'Business Cards',
        'section': 'print-materials'
    }
    return render(request, 'admin/print_cards.html', context)


@login_required
def print_trifolds(request):
    """Print materials - Trifold brochures management"""
    context = {
        'page_title': 'Trifold Brochures',
        'section': 'print-materials'
    }
    return render(request, 'admin/print_trifolds.html', context)


@login_required
def print_clothing(request):
    """Print materials - Custom clothing management"""
    context = {
        'page_title': 'Custom Clothing',
        'section': 'print-materials'
    }
    return render(request, 'admin/print_clothing.html', context)


@login_required
def print_gifts(request):
    """Print materials - Corporate gifts management"""
    context = {
        'page_title': 'Corporate Gifts',
        'section': 'print-materials'
    }
    return render(request, 'admin/print_gifts.html', context)


@login_required
def ai_chat_endpoint(request):
    """
    AI chat API endpoint
    """
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            message = data.get('message', '')
            
            # Mock AI response for now
            response_data = {
                'response': f'I received your message: "{message}". This is a mock response. The actual AI integration will be connected soon!',
                'suggestions': [
                    'Tell me more',
                    'Create a new page',
                    'Help with forms',
                    'Show examples'
                ]
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def subscription_management(request):
    """
    Subscription management view with domain, hosting, and website details
    """
    context = {
        'page_title': 'Subscription Management',
        'domain_info': {
            'domain_name': 'example.com',
            'status': 'Active',
            'expiry_date': '2025-12-08',
            'registrar': 'JustCodeWorks Registry',
            'auto_renewal': True,
            'dns_status': 'Configured'
        },
        'hosting_plan': {
            'plan_name': 'Professional',
            'plan_type': 'Shared Hosting',
            'storage': '50 GB SSD',
            'bandwidth': 'Unlimited',
            'email_accounts': '25',
            'databases': '10',
            'ssl_certificate': 'Free SSL',
            'backup_frequency': 'Daily',
            'uptime_guarantee': '99.9%',
            'monthly_cost': '€29.99'
        },
        'website_details': {
            'website_name': 'My Business Website',
            'template': 'Professional Business',
            'pages_count': 8,
            'last_update': '2025-10-07',
            'visitors_month': '2,547',
            'storage_used': '12.5 GB',
            'seo_score': '85/100',
            'mobile_friendly': True,
            'ssl_enabled': True,
            'cdn_enabled': True
        }
    }
    
    return render(request, 'admin/subscription.html', context)


@login_required
def settings_management(request):
    """
    Settings management view with contact, language, and profile configuration
    """
    context = {
        'page_title': 'Settings Management',
        'contact_info': {
            'company_name': 'JustCodeWorks.EU',
            'email': 'info@justcodeworks.eu',
            'phone': '+351 123 456 789',
            'address': 'Rua da Tecnologia, 123',
            'city': 'Lisboa',
            'postal_code': '1000-001',
            'country': 'Portugal',
            'website': 'https://justcodeworks.eu',
            'social_facebook': 'https://facebook.com/justcodeworks',
            'social_linkedin': 'https://linkedin.com/company/justcodeworks',
            'social_twitter': 'https://twitter.com/justcodeworks'
        },
        'language_settings': {
            'default_language': 'English',
            'available_languages': [
                {'code': 'en', 'name': 'English', 'flag': '🇺🇸', 'active': True},
                {'code': 'pt', 'name': 'Portuguese', 'flag': '🇵🇹', 'active': True},
                {'code': 'es', 'name': 'Spanish', 'flag': '🇪🇸', 'active': False},
                {'code': 'fr', 'name': 'French', 'flag': '🇫🇷', 'active': False},
                {'code': 'de', 'name': 'German', 'flag': '🇩🇪', 'active': False},
                {'code': 'it', 'name': 'Italian', 'flag': '🇮🇹', 'active': False}
            ],
            'auto_detect': True,
            'rtl_support': False
        },
        'profile_settings': {
            'user_name': 'Administrator',
            'email': 'admin@justcodeworks.eu',
            'role': 'Super Admin',
            'timezone': 'Europe/Lisbon',
            'date_format': 'DD/MM/YYYY',
            'time_format': '24h',
            'notifications_email': True,
            'notifications_sms': False,
            'notifications_desktop': True,
            'two_factor_auth': True,
            'last_login': '2025-10-08 14:30:25',
            'account_created': '2024-01-15',
            'login_attempts': 0
        },
        'analytics_integration': {
            'google_email': 'analytics@justcodeworks.eu',
            'google_property_id': 'G-XXXXXXXXXX',
            'facebook_pixel_id': '123456789012345',
            'bing_uet_tag': '12345678',
            'auto_tracking': True,
            'track_conversions': True,
            'track_events': True,
            'data_retention': '26 months'
        }
    }
    
    return render(request, 'admin/settings.html', context)


@login_required
def analytics_facebook(request):
    """
    Facebook Analytics dashboard
    """
    context = {
        'page_title': 'Facebook Analytics',
        'facebook_stats': {
            'page_likes': '12,547',
            'page_reach': '45,623',
            'post_engagement': '8.4%',
            'top_post_likes': '2,341',
            'followers_growth': '+245',
            'impressions': '89,432',
            'clicks': '1,876',
            'shares': '324'
        },
        'recent_posts': [
            {
                'content': 'Check out our latest website templates!',
                'date': '2025-10-07',
                'likes': 156,
                'comments': 23,
                'shares': 12
            },
            {
                'content': 'New AI Website Builder features released',
                'date': '2025-10-06',
                'likes': 203,
                'comments': 45,
                'shares': 18
            },
            {
                'content': 'Customer success story: HMD Klusbedrijf',
                'date': '2025-10-05',
                'likes': 89,
                'comments': 8,
                'shares': 5
            }
        ]
    }
    
    return render(request, 'admin/analytics_facebook.html', context)


@login_required
def analytics_google(request):
    """
    Google Analytics dashboard
    """
    context = {
        'page_title': 'Google Analytics',
        'google_stats': {
            'total_users': '28,945',
            'sessions': '45,672',
            'pageviews': '127,834',
            'bounce_rate': '42.3%',
            'avg_session_duration': '3m 42s',
            'new_users': '18,234',
            'returning_users': '10,711',
            'conversion_rate': '3.8%'
        },
        'traffic_sources': [
            {'source': 'Organic Search', 'users': '15,234', 'percentage': '52.6%'},
            {'source': 'Direct', 'users': '8,945', 'percentage': '30.9%'},
            {'source': 'Social Media', 'users': '3,456', 'percentage': '11.9%'},
            {'source': 'Referrals', 'users': '1,310', 'percentage': '4.5%'}
        ],
        'top_pages': [
            {'page': '/', 'pageviews': '23,456', 'unique_pageviews': '18,234'},
            {'page': '/website-builder/', 'pageviews': '12,345', 'unique_pageviews': '9,876'},
            {'page': '/templates/', 'pageviews': '8,765', 'unique_pageviews': '7,234'},
            {'page': '/pricing/', 'pageviews': '6,543', 'unique_pageviews': '5,432'}
        ]
    }
    
    return render(request, 'admin/analytics_google.html', context)


@login_required
def analytics_bing(request):
    """
    Bing Analytics dashboard
    """
    context = {
        'page_title': 'Bing Analytics',
        'bing_stats': {
            'total_clicks': '5,847',
            'total_impressions': '89,234',
            'avg_ctr': '6.5%',
            'avg_position': '4.2',
            'total_keywords': '1,234',
            'top_keyword_clicks': '456',
            'indexed_pages': '89',
            'crawl_errors': '2'
        },
        'top_keywords': [
            {'keyword': 'website builder', 'clicks': 456, 'impressions': 8234, 'ctr': '5.5%', 'position': 3.2},
            {'keyword': 'custom website design', 'clicks': 234, 'impressions': 5678, 'ctr': '4.1%', 'position': 4.8},
            {'keyword': 'AI website creator', 'clicks': 189, 'impressions': 4321, 'ctr': '4.4%', 'position': 2.9},
            {'keyword': 'business website templates', 'clicks': 156, 'impressions': 3456, 'ctr': '4.5%', 'position': 5.1}
        ],
        'search_performance': [
            {'date': '2025-10-07', 'clicks': 234, 'impressions': 4567, 'ctr': '5.1%'},
            {'date': '2025-10-06', 'clicks': 189, 'impressions': 3890, 'ctr': '4.9%'},
            {'date': '2025-10-05', 'clicks': 267, 'impressions': 5234, 'ctr': '5.1%'},
            {'date': '2025-10-04', 'clicks': 198, 'impressions': 4123, 'ctr': '4.8%'}
        ]
    }
    
    return render(request, 'admin/analytics_bing.html', context)


@login_required
def analytics_integration(request):
    """
    Analytics Integration setup and management
    """
    if request.method == 'POST':
        # Handle form submission for analytics setup
        google_email = request.POST.get('google_email')
        property_id = request.POST.get('property_id')
        
        if google_email and property_id:
            # Here you would normally:
            # 1. Validate the Google Analytics credentials
            # 2. Connect to Google Analytics API
            # 3. Verify property access
            # 4. Store credentials securely
            # 5. Auto-inject tracking codes
            
            # For demo purposes, we'll simulate success
            context = {
                'page_title': 'Analytics Integration',
                'success_message': f'Successfully connected {google_email} to property {property_id}',
                'integration_status': {
                    'google_analytics': 'Connected',
                    'facebook_pixel': 'Pending',
                    'bing_ads': 'Not Connected',
                    'last_sync': '2025-10-08 15:30:00'
                }
            }
        else:
            context = {
                'page_title': 'Analytics Integration',
                'error_message': 'Please provide both Gmail address and Property ID'
            }
    else:
        context = {
            'page_title': 'Analytics Integration',
            'integration_status': {
                'google_analytics': 'Not Connected',
                'facebook_pixel': 'Not Connected', 
                'bing_ads': 'Not Connected',
                'last_sync': 'Never'
            },
            'tracking_codes': {
                'google_analytics_code': '''
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
                ''',
                'facebook_pixel_code': '''
<!-- Facebook Pixel -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '123456789012345');
fbq('track', 'PageView');
</script>
                '''
            }
        }
    
    return render(request, 'admin/analytics_integration.html', context)


@login_required
def translations_management(request):
    """
    Translation management view for multilingual support with real database data
    """
    from translations.models import TranslationKey, Translation, get_translation_statistics, LanguageSettings
    
    # Available languages from settings
    available_languages = [
        {'code': 'en', 'name': 'English', 'flag': '🇺🇸'},
        {'code': 'nl', 'name': 'Nederlands', 'flag': '🇳🇱'},
        {'code': 'de', 'name': 'Deutsch', 'flag': '🇩🇪'},
        {'code': 'fr', 'name': 'Français', 'flag': '🇫🇷'},
        {'code': 'es', 'name': 'Español', 'flag': '🇪🇸'},
        {'code': 'pt', 'name': 'Português', 'flag': '🇵🇹'},
    ]
    
    # Get real translation statistics from database
    translation_stats = get_translation_statistics()
    
    # Get translation keys with their translations
    translation_keys = []
    for key in TranslationKey.objects.all():
        key_data = {'key': key.key}
        
        # Get translations for each language
        for lang_code, lang_name in Translation.LANGUAGE_CHOICES:
            try:
                translation = Translation.objects.get(key=key, language=lang_code)
                key_data[lang_code] = translation.value
            except Translation.DoesNotExist:
                key_data[lang_code] = None
        
        translation_keys.append(key_data)
    
    context = {
        'page_title': 'Translation Management',
        'available_languages': available_languages,
        'translation_stats': translation_stats,
        'translation_keys': translation_keys,
        'current_language': getattr(request, 'LANGUAGE_CODE', 'en'),
    }
    
    return render(request, 'admin/translations.html', context)