from django.http import Http404
from tenants.models import Tenant, Domain
from tenants.views import get_tenant_from_request, customer_home, customer_about, customer_services, customer_portfolio, customer_contact, customer_quote


class CustomerSubdomainMiddleware:
    """Middleware to handle customer subdomain routing"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get tenant by subdomain (real subdomains like vakwerkpro.justcodeworks.eu)
        tenant = get_tenant_from_request(request)
        
        # Fallback: For localhost testing, check for customer parameter in URL
        if not tenant:
            customer_param = request.GET.get('customer')
            if customer_param:
                try:
                    tenant = Tenant.objects.get(schema_name=customer_param)
                except Tenant.DoesNotExist:
                    pass
        
        if tenant:
            # This is a customer subdomain or test
            path_info = request.path_info.strip('/')
            
            # Route to appropriate customer view
            if path_info == '':
                return customer_home(request, tenant)
            elif path_info == 'about':
                return customer_about(request, tenant)
            elif path_info == 'services':
                return customer_services(request, tenant)
            elif path_info == 'portfolio':
                return customer_portfolio(request, tenant)
            elif path_info == 'contact':
                return customer_contact(request, tenant)
            elif path_info == 'get-quote':
                return customer_quote(request, tenant)
            # Add customer admin routes
            elif path_info == 'admin' or path_info.startswith('admin/'):
                # Handle customer admin interface
                from websites.customer_admin_views import customer_admin_dashboard
                return customer_admin_dashboard(request)
        
        # Not a customer subdomain or unhandled path - continue normal processing
        response = self.get_response(request)
        return response