from django.core.management.base import BaseCommand
from website_builder.models import WebsiteTemplate


class Command(BaseCommand):
    help = 'Create or update JCW templates with correct IDs (jcw-tpl01, jcw-tpl02, jcw-tpl03)'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Setting up JCW templates...')
        )
        
        # Template configurations
        templates_config = [
            {
                'template_id': 'jcw-tpl01',
                'name': 'JCW Professional Business Template 01',
                'description': 'Modern professional business template with clean design and corporate layout',
                'category': 'business',
                'preview_image': '/media/website_templates/previews/jcw-tpl01.png',
                'thumbnail_image': '/media/website_templates/thumbnails/jcw-tpl01.png',
            },
            {
                'template_id': 'jcw-tpl02',
                'name': 'JCW Creative Portfolio Template 02',
                'description': 'Creative and modern template perfect for portfolios and creative businesses',
                'category': 'creative',
                'preview_image': '/media/website_templates/previews/jcw-tpl02.png',
                'thumbnail_image': '/media/website_templates/thumbnails/jcw-tpl02.png',
            },
            {
                'template_id': 'jcw-tpl03',
                'name': 'JCW Service Business Template 03',
                'description': 'Service-oriented template ideal for consultants and service providers',
                'category': 'business',
                'preview_image': '/media/website_templates/previews/jcw-tpl03.png',
                'thumbnail_image': '/media/website_templates/thumbnails/jcw-tpl03.png',
            }
        ]
        
        for template_data in templates_config:
            template, created = WebsiteTemplate.objects.update_or_create(
                template_id=template_data['template_id'],
                defaults={
                    'name': template_data['name'],
                    'description': template_data['description'],
                    'category': template_data['category'],
                    'preview_image': template_data['preview_image'],
                    'thumbnail_image': template_data['thumbnail_image'],
                    'is_active': True,
                    'html_template': self.get_template_html(template_data['template_id']),
                    'css_template': self.get_template_css(template_data['template_id']),
                    'js_template': '',  # Empty JS template for now
                    'supports_one_page': True,
                    'supports_multi_page': True,
                    'color_schemes': ['default', 'blue', 'green', 'red'],
                    'font_options': ['Arial', 'Georgia', 'Helvetica'],
                    'usage_count': 0,
                    'rating': 5.0,
                    'is_ai_generated': False,
                }
            )
            
            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(f'{action} template: {template_data["template_id"]} - {template_data["name"]}')
            )
        
        # Clean up old template if exists
        try:
            old_template = WebsiteTemplate.objects.get(template_id='professional_universal_v1')
            old_template.delete()
            self.stdout.write(
                self.style.WARNING('Removed old template: professional_universal_v1')
            )
        except WebsiteTemplate.DoesNotExist:
            pass
        
        self.stdout.write(
            self.style.SUCCESS('JCW templates setup completed!')
        )

    def get_template_html(self, template_id):
        """Generate basic HTML content for each template"""
        base_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ business_name }}}} - {template_id.upper()}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">
                <h1>{{{{ business_name }}}}</h1>
            </div>
            <ul class="nav-menu">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section id="home" class="hero">
            <div class="hero-content">
                <h1>Welcome to {{{{ business_name }}}}</h1>
                <p>{{{{ business_description }}}}</p>
                <a href="#contact" class="cta-button">Get Started</a>
            </div>
        </section>

        <section id="about" class="about">
            <div class="container">
                <h2>About Us</h2>
                <p>{{{{ about_text }}}}</p>
            </div>
        </section>

        <section id="services" class="services">
            <div class="container">
                <h2>Our Services</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <h3>Service 1</h3>
                        <p>Description of service 1</p>
                    </div>
                    <div class="service-card">
                        <h3>Service 2</h3>
                        <p>Description of service 2</p>
                    </div>
                    <div class="service-card">
                        <h3>Service 3</h3>
                        <p>Description of service 3</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="contact" class="contact">
            <div class="container">
                <h2>Contact Us</h2>
                <div class="contact-info">
                    <p><strong>Phone:</strong> {{{{ phone }}}}</p>
                    <p><strong>Email:</strong> {{{{ email }}}}</p>
                    <p><strong>Address:</strong> {{{{ address }}}}</p>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2025 {{{{ business_name }}}}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''
        return base_html

    def get_template_css(self, template_id):
        """Generate basic CSS content for each template"""
        if template_id == 'jcw-tpl01':
            return self.get_tpl01_css()
        elif template_id == 'jcw-tpl02':
            return self.get_tpl02_css()
        elif template_id == 'jcw-tpl03':
            return self.get_tpl03_css()
        else:
            return self.get_default_css()

    def get_tpl01_css(self):
        """Professional Business Template CSS"""
        return '''/* JCW Template 01 - Professional Business */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
header {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-menu a:hover {
    color: #3498db;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 150px 0 100px;
    text-align: center;
}

.hero-content h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-content p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.cta-button {
    background: #3498db;
    color: white;
    padding: 12px 30px;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    transition: background 0.3s;
}

.cta-button:hover {
    background: #2980b9;
}

/* Sections */
section {
    padding: 80px 0;
}

.about {
    background: #f8f9fa;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.service-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

/* Footer */
footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .nav-menu {
        flex-direction: column;
        gap: 1rem;
    }
    
    .hero-content h1 {
        font-size: 2rem;
    }
}'''

    def get_tpl02_css(self):
        """Creative Portfolio Template CSS"""
        return '''/* JCW Template 02 - Creative Portfolio */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', serif;
    line-height: 1.6;
    color: #444;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
header {
    background: #fff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.logo h1 {
    color: #e74c3c;
    font-size: 1.8rem;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: #333;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-menu a:hover {
    color: #e74c3c;
}

/* Hero Section */
.hero {
    background: linear-gradient(45deg, #ff6b6b, #ffd93d);
    color: white;
    padding: 150px 0 100px;
    text-align: center;
}

.hero-content h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    font-weight: 300;
}

.hero-content p {
    font-size: 1.3rem;
    margin-bottom: 2rem;
}

.cta-button {
    background: #e74c3c;
    color: white;
    padding: 15px 35px;
    text-decoration: none;
    border-radius: 25px;
    font-weight: bold;
    transition: all 0.3s;
}

.cta-button:hover {
    background: #c0392b;
    transform: translateY(-2px);
}

/* Sections */
section {
    padding: 80px 0;
}

.about {
    background: #fafafa;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.service-card {
    background: white;
    padding: 2.5rem;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    text-align: center;
    border-left: 4px solid #e74c3c;
}

/* Footer */
footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-content h1 {
        font-size: 2.5rem;
    }
}'''

    def get_tpl03_css(self):
        """Service Business Template CSS"""
        return '''/* JCW Template 03 - Service Business */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Helvetica', sans-serif;
    line-height: 1.6;
    color: #555;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
header {
    background: #34495e;
    color: white;
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-menu a:hover {
    color: #1abc9c;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%);
    color: white;
    padding: 150px 0 100px;
    text-align: center;
}

.hero-content h1 {
    font-size: 3.2rem;
    margin-bottom: 1rem;
    font-weight: bold;
}

.hero-content p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.cta-button {
    background: #e67e22;
    color: white;
    padding: 14px 32px;
    text-decoration: none;
    border-radius: 6px;
    font-weight: bold;
    transition: background 0.3s;
}

.cta-button:hover {
    background: #d35400;
}

/* Sections */
section {
    padding: 80px 0;
}

.about {
    background: #ecf0f1;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.service-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
    text-align: center;
    border-top: 3px solid #1abc9c;
}

.service-card h3 {
    color: #1abc9c;
    margin-bottom: 1rem;
}

/* Footer */
footer {
    background: #34495e;
    color: white;
    text-align: center;
    padding: 2rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-content h1 {
        font-size: 2.2rem;
    }
}'''

    def get_default_css(self):
        """Default CSS template"""
        return '''/* Default Template CSS */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
header { background: #333; color: white; padding: 1rem 0; }
nav { display: flex; justify-content: space-between; align-items: center; }
.nav-menu { display: flex; list-style: none; gap: 2rem; }
.nav-menu a { color: white; text-decoration: none; }
.hero { background: #f4f4f4; padding: 100px 0; text-align: center; }
section { padding: 60px 0; }
.services-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
.service-card { background: white; padding: 2rem; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
footer { background: #333; color: white; text-align: center; padding: 2rem 0; }'''