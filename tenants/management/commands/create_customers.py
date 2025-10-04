from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Create realistic customer tenant examples'

    def handle(self, *args, **options):
        # Create realistic customer companies
        customers = [
            {
                'name': 'VakWerk Pro BV',
                'schema_name': 'vakwerkpro', 
                'domain': 'vakwerkpro.justcodeworks.eu',
                'company_name': 'VakWerk Pro',
                'contact_email': 'info@vakwerkpro.nl',
                'phone': '+31 20 123 4567',
                'plan': 'premium',
                'template': 'tp2',
                'description': 'Professional construction and renovation services in Amsterdam'
            },
            {
                'name': 'Bouwbedrijf Amsterdam',
                'schema_name': 'bouwbedrijf_amsterdam',
                'domain': 'bouwbedrijf-amsterdam.justcodeworks.eu', 
                'company_name': 'Bouwbedrijf Amsterdam',
                'contact_email': 'contact@bouwbedrijf-amsterdam.nl',
                'phone': '+31 20 987 6543',
                'plan': 'basic',
                'template': 'tp2',
                'description': 'Traditional construction company serving Amsterdam and surroundings'
            },
            {
                'name': 'TechSolutions Europe',
                'schema_name': 'techsolutions',
                'domain': 'techsolutions.justcodeworks.eu',
                'company_name': 'TechSolutions Europe',
                'contact_email': 'hello@techsolutions.eu',
                'phone': '+31 85 401 2345',
                'plan': 'premium', 
                'template': 'tp1',
                'description': 'Innovative technology solutions for European businesses'
            },
            {
                'name': 'WebStudio Delft',
                'schema_name': 'webstudio_delft',
                'domain': 'webstudio-delft.justcodeworks.eu',
                'company_name': 'WebStudio Delft',
                'contact_email': 'info@webstudio-delft.nl',
                'phone': '+31 15 234 5678',
                'plan': 'basic',
                'template': 'tp1', 
                'description': 'Creative web design and development studio in Delft'
            },
            {
                'name': 'Schilder & Partners',
                'schema_name': 'schilder_partners',
                'domain': 'schilder-partners.justcodeworks.eu',
                'company_name': 'Schilder & Partners',
                'contact_email': 'offerte@schilder-partners.nl',
                'phone': '+31 30 345 6789',
                'plan': 'basic',
                'template': 'tp2',
                'description': 'Professional painting services for residential and commercial projects'
            }
        ]

        for customer_data in customers:
            # Create or update tenant
            tenant, created = Tenant.objects.get_or_create(
                schema_name=customer_data['schema_name'],
                defaults={
                    'name': customer_data['name'],
                    'company_name': customer_data['company_name'],
                    'contact_email': customer_data['contact_email'],
                    'phone': customer_data['phone'],
                    'plan': customer_data['plan'],
                    'description': customer_data['description'],
                }
            )
            
            # Create or update domain
            domain, created = Domain.objects.get_or_create(
                domain=customer_data['domain'],
                defaults={
                    'tenant': tenant,
                    'is_primary': True
                }
            )
            
            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(
                    f'{action} tenant: {tenant.name} -> {domain.domain} (Template: {customer_data["template"]})'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully processed {len(customers)} customer tenants!'
            )
        )