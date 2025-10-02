from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from websites.models import Website, Page, HomeSlider, Settings
from tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Create example website data for demonstration'

    def handle(self, *args, **options):
        # Create demo user
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
            }
        )
        
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user: demo/demo123'))
        else:
            self.stdout.write(self.style.WARNING('Demo user already exists'))

        # Create tenant
        tenant, created = Tenant.objects.get_or_create(
            schema_name='demo',
            defaults={
                'name': 'Demo Company Website',
                'company_name': 'Demo Company Ltd.',
                'contact_email': 'contact@democompany.com',
                'phone': '+1-555-0123',
                'plan': 'basic'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created tenant: {tenant.name}'))
        
        # Create domain
        domain, created = Domain.objects.get_or_create(
            domain='demo.localhost:8000',
            defaults={
                'tenant': tenant,
                'is_primary': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created domain: {domain.domain}'))

        # Create example website
        website, created = Website.objects.get_or_create(
            owner=demo_user,
            defaults={
                'name': 'Demo Company Website',
                'description': 'A beautiful example website created with JustCodeWorks.EU',
                'domain': 'demo.localhost:8000',
                'meta_title': 'Demo Company - Leading Solutions Provider',
                'meta_description': 'Demo Company provides innovative solutions for businesses worldwide. Discover our services and expertise.',
                'theme': 'modern',
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created website: {website.name}'))
        
        # Create homepage
        homepage, created = Page.objects.get_or_create(
            website=website,
            is_homepage=True,
            defaults={
                'title': 'Welcome to Demo Company',
                'slug': 'home',
                'content': '''
                <div class="row">
                    <div class="col-lg-6">
                        <h2>Welcome to Our Company</h2>
                        <p class="lead">We are a leading provider of innovative solutions that help businesses grow and succeed in today's competitive market.</p>
                        <p>Our team of experts has over 20 years of combined experience in delivering high-quality services to clients across various industries.</p>
                        <ul>
                            <li>Professional consulting services</li>
                            <li>Custom software development</li>
                            <li>24/7 customer support</li>
                            <li>Proven track record of success</li>
                        </ul>
                    </div>
                    <div class="col-lg-6">
                        <h3>Why Choose Us?</h3>
                        <p>We believe in building lasting partnerships with our clients by delivering exceptional value and outstanding results.</p>
                        <div class="alert alert-info">
                            <strong>Get Started Today!</strong> Contact us to learn how we can help your business achieve its goals.
                        </div>
                    </div>
                </div>
                ''',
                'meta_title': 'Welcome to Demo Company - Home',
                'meta_description': 'Welcome to Demo Company. Learn about our services and how we can help your business succeed.',
                'is_published': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created homepage: {homepage.title}'))
        
        # Create slider items
        slider_items = [
            {
                'title': 'Professional Solutions',
                'subtitle': 'Excellence in Every Project',
                'description': 'We deliver high-quality solutions that exceed expectations and drive business growth.',
                'button_text': 'Learn More',
                'button_url': '#about',
                'order': 1
            },
            {
                'title': 'Expert Team',
                'subtitle': '20+ Years of Experience', 
                'description': 'Our experienced professionals are dedicated to helping your business succeed.',
                'button_text': 'Meet Our Team',
                'button_url': '#team',
                'order': 2
            },
            {
                'title': 'Customer Focused',
                'subtitle': '24/7 Support Available',
                'description': 'We provide round-the-clock support to ensure your success at every step.',
                'button_text': 'Contact Us',
                'button_url': '#contact',
                'order': 3
            }
        ]
        
        for item_data in slider_items:
            slider_item, created = HomeSlider.objects.get_or_create(
                website=website,
                title=item_data['title'],
                defaults=item_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created slider item: {slider_item.title}'))
        
        # Create settings
        settings, created = Settings.objects.get_or_create(
            website=website,
            defaults={
                'contact_email': 'contact@democompany.com',
                'contact_phone': '+1-555-0123',
                'address': '123 Business Street\nSuite 100\nBusiness City, BC 12345',
                'facebook_url': 'https://facebook.com/democompany',
                'twitter_url': 'https://twitter.com/democompany',
                'linkedin_url': 'https://linkedin.com/company/democompany',
                'google_analytics_id': 'GA-123456789-1'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created website settings'))
        
        # Create additional pages
        about_page, created = Page.objects.get_or_create(
            website=website,
            slug='about',
            defaults={
                'title': 'About Us',
                'content': '''
                <h2>About Demo Company</h2>
                <p class="lead">Founded in 2004, Demo Company has been at the forefront of innovation, helping businesses transform and grow through cutting-edge solutions.</p>
                
                <div class="row mt-4">
                    <div class="col-md-6">
                        <h4>Our Mission</h4>
                        <p>To empower businesses with innovative solutions that drive growth, efficiency, and success in an ever-evolving marketplace.</p>
                        
                        <h4>Our Vision</h4>
                        <p>To be the leading partner for businesses seeking transformation and growth through technology and strategic innovation.</p>
                    </div>
                    <div class="col-md-6">
                        <h4>Our Values</h4>
                        <ul>
                            <li><strong>Innovation:</strong> We continuously push boundaries to deliver cutting-edge solutions.</li>
                            <li><strong>Excellence:</strong> We strive for excellence in everything we do.</li>
                            <li><strong>Partnership:</strong> We build lasting relationships with our clients.</li>
                            <li><strong>Integrity:</strong> We conduct business with honesty and transparency.</li>
                        </ul>
                    </div>
                </div>
                ''',
                'meta_title': 'About Us - Demo Company',
                'meta_description': 'Learn about Demo Company\'s mission, vision, and values. Discover our history and commitment to excellence.',
                'is_published': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created page: {about_page.title}'))
            
        self.stdout.write(self.style.SUCCESS('Example data creation completed successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now:'))
        self.stdout.write(self.style.SUCCESS('1. Login to Django admin with admin/admin123 at /admin5689/'))
        self.stdout.write(self.style.SUCCESS('2. Login to tenant admin with demo/demo123 at /tenant-admin/'))
        self.stdout.write(self.style.SUCCESS('3. Preview the website at /tenant-admin/preview/'))
        self.stdout.write(self.style.SUCCESS('4. Coming soon page at / (for non-authenticated users)'))