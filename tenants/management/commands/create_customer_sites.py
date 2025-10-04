from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Create customer tenant websites for demo'

    def handle(self, *args, **options):
        customers = [
            {
                'name': 'Customer Site 1',
                'schema_name': 'customer1',
                'domain': 'customer1.justcodeworks.eu',
                'company_name': 'ABC Corporation',
                'contact_email': 'info@abccorp.com',
                'description': 'Professional business website for ABC Corporation'
            },
            {
                'name': 'Customer Site 2', 
                'schema_name': 'customer2',
                'domain': 'customer2.justcodeworks.eu',
                'company_name': 'XYZ Services Ltd',
                'contact_email': 'contact@xyzservices.com',
                'description': 'Service provider website for XYZ Services'
            },
            {
                'name': 'Customer Site 3',
                'schema_name': 'customer3', 
                'domain': 'customer3.justcodeworks.eu',
                'company_name': 'Digital Solutions Inc',
                'contact_email': 'hello@digitalsolutions.com',
                'description': 'Tech company website for Digital Solutions'
            }
        ]

        for customer_data in customers:
            # Create tenant
            tenant, created = Tenant.objects.get_or_create(
                schema_name=customer_data['schema_name'],
                defaults={
                    'name': customer_data['name'],
                    'description': customer_data['description'],
                    'company_name': customer_data['company_name'],
                    'contact_email': customer_data['contact_email'],
                    'plan': 'premium',
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created tenant: {tenant.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Tenant already exists: {tenant.name}')
                )
            
            # Create domain
            domain, created = Domain.objects.get_or_create(
                domain=customer_data['domain'],
                defaults={
                    'tenant': tenant,
                    'is_primary': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created domain: {domain.domain}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Domain already exists: {domain.domain}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✅ Customer sites setup complete!')
        )
        self.stdout.write('Test URLs:')
        self.stdout.write('- http://customer1.justcodeworks.eu/')
        self.stdout.write('- http://customer2.justcodeworks.eu/') 
        self.stdout.write('- http://customer3.justcodeworks.eu/')
        self.stdout.write('\nNote: You need to configure DNS A records pointing these subdomains to 46.202.152.237')