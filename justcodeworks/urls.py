"""
URL configuration for justcodeworks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shared import views as shared_views
from websites import views as website_views
from websites import signup_views_fixed as signup_views
from tenants import views as tenant_views


def customer_site_router(request):
    """Route customer subdomain requests to appropriate views"""
    tenant = tenant_views.get_tenant_from_request(request)
    
    if tenant:
        # This is a customer subdomain - route to customer views
        path_info = request.path_info.strip('/')
        
        if path_info == '' or path_info == '/':
            return tenant_views.customer_home(request, tenant)
        elif path_info == 'about':
            return tenant_views.customer_about(request, tenant)
        elif path_info == 'services':
            return tenant_views.customer_services(request, tenant)
        elif path_info == 'portfolio':
            return tenant_views.customer_portfolio(request, tenant)
        elif path_info == 'contact':
            return tenant_views.customer_contact(request, tenant)
        elif path_info == 'get-quote':
            return tenant_views.customer_quote(request, tenant)
    
    # Not a customer subdomain - continue with normal routing
    return None


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tenant-admin/', include('websites.urls')),
    path('coming-soon/', shared_views.coming_soon_view, name='coming_soon'),
    
    # Signup Flow
    path('signup/', signup_views.signup_step1, name='signup_step1'),
    path('signup/step2/', signup_views.signup_step2, name='signup_step2'),
    path('signup/step3/', signup_views.signup_step3, name='signup_step3'),
    path('signup/complete/', signup_views.signup_complete, name='signup_complete'),
    
    # TP1 Template Routes (JustCodeWorks main site)
    path('', website_views.home_page, name='home'),
    path('about/', website_views.about_page, name='about'),
    path('services/', website_views.services_page, name='services'),
    path('services/<slug:service_slug>/', website_views.service_detail_page, name='service_detail'),
    path('portfolio/', website_views.portfolio_page, name='portfolio'),
    path('contact/', website_views.contact_page, name='contact'),
    path('get-quote/', website_views.quote_page, name='quote'),
    
    # TP2 Template Routes (Demo purposes)
    path('tp2/', website_views.tp2_home, name='tp2_home'),
    path('tp2/about/', website_views.tp2_about, name='tp2_about'),
    path('tp2/services/', website_views.tp2_services, name='tp2_services'),
    path('tp2/portfolio/', website_views.tp2_portfolio, name='tp2_portfolio'),
    path('tp2/contact/', website_views.tp2_contact, name='tp2_contact'),
    
    # Customer Admin Routes
    path('customer-admin/', website_views.customer_admin_home, name='customer_admin'),
    path('customer-admin/templates/', website_views.customer_template_selection, name='template_selection'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
