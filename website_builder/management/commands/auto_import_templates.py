from django.core.management.base import BaseCommand
from website_builder.models import WebsiteTemplate
import os
from django.conf import settings
import re


class Command(BaseCommand):
    help = 'Automatically scan and import new templates from the media directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--scan-only',
            action='store_true',
            help='Only scan and show what would be imported, without actually importing',
        )
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Update existing templates even if they already exist',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔍 Scanning for new templates in organized folders...')
        )
        
        preview_dir = os.path.join(settings.MEDIA_ROOT, 'website_templates', 'previews')
        
        if not os.path.exists(preview_dir):
            self.stdout.write(
                self.style.ERROR(f'Preview directory not found: {preview_dir}')
            )
            return
        
        # Scan for category folders and preview images
        found_templates = []
        
        # First check for files in root directory (legacy support - PNG for backwards compatibility)
        root_files = [f for f in os.listdir(preview_dir) if f.endswith(('.png', '.jpg', '.jpeg')) and os.path.isfile(os.path.join(preview_dir, f))]
        
        # Then check category folders (prioritize JPG files)
        category_folders = [d for d in os.listdir(preview_dir) if os.path.isdir(os.path.join(preview_dir, d))]
        
        self.stdout.write(f'📁 Found category folders: {category_folders}')
        if root_files:
            self.stdout.write(f'📄 Found {len(root_files)} files in root directory (legacy)')
        
        # Process category folders (JPG preferred)
        for folder in category_folders:
            category_path = os.path.join(preview_dir, folder)
            # Prioritize JPG files, but still support PNG during transition
            jpg_files = [f for f in os.listdir(category_path) if f.endswith('.jpg')]
            png_files = [f for f in os.listdir(category_path) if f.endswith(('.png', '.jpeg'))]
            category_files = jpg_files + png_files  # JPG first priority
            
            self.stdout.write(f'🏷️  Category "{folder}": {len(category_files)} files')
            
            for filename in category_files:
                template_info = self.parse_template_from_folder(folder, filename)
                if template_info:
                    found_templates.append(template_info)
        
        # Process legacy root files (if any) using the same patterns
        if root_files:
            legacy_templates = self.process_legacy_files(root_files)
            found_templates.extend(legacy_templates)
        
        # Sort all templates by ID for consistent output  
        found_templates.sort(key=lambda x: x['template_id'])
        
        # Display findings
        self.stdout.write(f'\n📋 Found {len(found_templates)} total templates:')
        
        new_count = 0
        existing_count = 0
        
        for template in found_templates:
            status_icon = "✅" if template['exists'] else "🆕"
            status_text = "EXISTS" if template['exists'] else "NEW"
            
            if template['exists']:
                existing_count += 1
            else:
                new_count += 1
            
            self.stdout.write(
                f"  {status_icon} {template['template_id']} - {template['name']} [{status_text}]"
            )
            self.stdout.write(
                f"      Category: {template['category']} | Type: {template['type']}"
            )
        
        self.stdout.write(f'\n📊 Summary: {new_count} new templates, {existing_count} existing')
        
        # If scan-only mode, stop here
        if options['scan_only']:
            self.stdout.write(
                self.style.WARNING('\n👀 Scan-only mode: No changes made to database')
            )
            return
        
        # Import new templates
        if new_count == 0 and not options['force_update']:
            self.stdout.write(
                self.style.SUCCESS('\n✨ No new templates to import!')
            )
            return
        
        imported_count = 0
        updated_count = 0
        
        for template in found_templates:
            if template['exists'] and not options['force_update']:
                continue
            
            # Create organized thumbnail directory if needed
            thumbnail_dir = os.path.join(
                settings.MEDIA_ROOT,
                'website_templates', 
                'thumbnails',
                template['category']
            )
            os.makedirs(thumbnail_dir, exist_ok=True)
            
            # Check if thumbnail exists, create if needed
            thumbnail_full_path = os.path.join(settings.MEDIA_ROOT, template['thumbnail_path'])
            preview_full_path = os.path.join(settings.MEDIA_ROOT, template['preview_path'])
            
            if not os.path.exists(thumbnail_full_path) and os.path.exists(preview_full_path):
                import shutil
                shutil.copy2(preview_full_path, thumbnail_full_path)
                self.stdout.write(f"  📋 Created thumbnail for {template['template_id']} in {template['category']}/")
            
            # Create or update template
            template_obj, created = WebsiteTemplate.objects.update_or_create(
                template_id=template['template_id'],
                defaults={
                    'name': template['name'],
                    'category': template['category'],
                    'description': template['description'],
                    'preview_image': template['preview_path'],
                    'thumbnail_image': template['thumbnail_path'],
                    'html_template': self.get_template_html(template),
                    'css_template': self.get_template_css(template),
                    'js_template': '',
                    'supports_one_page': template['type'] in ['one_page', 'business', 'portfolio'],
                    'supports_multi_page': template['type'] in ['multi_page', 'business', 'ecommerce'],
                    'color_schemes': ['default', 'blue', 'green', 'red', 'purple'],
                    'font_options': ['Arial', 'Georgia', 'Helvetica', 'Open Sans'],
                    'is_active': True,
                    'is_ai_generated': False,
                    'usage_count': 0,
                    'rating': 5.0,
                }
            )
            
            if created:
                imported_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✨ Imported: {template["template_id"]}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'  🔄 Updated: {template["template_id"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Import complete! {imported_count} imported, {updated_count} updated')
        )

    def parse_template_from_folder(self, category, filename):
        """Parse template information from organized category folders"""
        
        # Template naming patterns for organized folders (JPG preferred)
        patterns = {
            r'^jcw-(\w+)(\d+)\.(jpg|png|jpeg)$': {
                'name_template': 'JCW {category_title} Template {number}',
                'description_template': '{category_title} template #{number} - Professional and modern design'
            },
            r'^(\w+)-template-(\d+)\.(jpg|png|jpeg)$': {
                'name_template': '{category_title} Template {number}',
                'description_template': 'Professional {category} template #{number}'
            },
            r'^template-(\d+)\.(jpg|png|jpeg)$': {
                'name_template': '{category_title} Template {number}',
                'description_template': 'Template #{number} for {category} websites'
            }
        }
        
        for pattern, config in patterns.items():
            match = re.match(pattern, filename)
            if match:
                if 'jcw-' in pattern:
                    # jcw-restaurant01.png -> restaurant01
                    type_part = match.group(1)  # restaurant
                    number = match.group(2)     # 01
                    extension = match.group(3)  # png
                    template_id = f"jcw-{type_part}{number}"
                else:
                    number = match.group(1)
                    template_id = f"{category}-template-{number}"
                
                # Check if template already exists
                try:
                    from website_builder.models import WebsiteTemplate
                    exists = WebsiteTemplate.objects.filter(template_id=template_id).exists()
                except:
                    exists = False
                
                # Build paths
                preview_path = f'website_templates/previews/{category}/{filename}'
                thumbnail_path = f'website_templates/thumbnails/{category}/{filename}'
                
                template_info = {
                    'template_id': template_id,
                    'filename': filename,
                    'category': category,
                    'name': config['name_template'].format(
                        category_title=category.title(),
                        category=category,
                        number=number.lstrip('0') or number
                    ),
                    'description': config['description_template'].format(
                        category_title=category.title(),
                        category=category,
                        number=number.lstrip('0') or number
                    ),
                    'preview_path': preview_path,
                    'thumbnail_path': thumbnail_path,
                    'type': self.get_template_type(category),
                    'exists': exists
                }
                
                return template_info
        
        # If no pattern matches, create a generic template
        base_name = os.path.splitext(filename)[0]
        template_id = f"{category}-{base_name}"
        
        try:
            from website_builder.models import WebsiteTemplate
            exists = WebsiteTemplate.objects.filter(template_id=template_id).exists()
        except:
            exists = False
        
        return {
            'template_id': template_id,
            'filename': filename,
            'category': category,
            'name': f"{category.title()} - {base_name.title()}",
            'description': f"Professional {category} template - {base_name}",
            'preview_path': f'website_templates/previews/{category}/{filename}',
            'thumbnail_path': f'website_templates/thumbnails/{category}/{filename}',
            'type': self.get_template_type(category),
            'exists': exists
        }

    def get_template_type(self, category):
        """Determine template type based on category"""
        type_mapping = {
            'business': 'one_page',
            'restaurant': 'one_page', 
            'bars': 'one_page',
            'construction': 'business',
            'shop': 'ecommerce',
            'ecommerce': 'ecommerce',
            'portfolio': 'portfolio',
            'creative': 'portfolio',
            'multi': 'multi_page'
        }
        return type_mapping.get(category, 'one_page')

    def process_legacy_files(self, root_files):
        """Process templates in root directory (legacy support)"""
        
        # Template naming patterns for legacy root files (maintain PNG support for existing files)
        template_patterns = {
            r'^jcw-tpl(\d+)\.(jpg|png|jpeg)$': {
                'category': 'business',
                'type': 'one_page',
                'name_template': 'JCW Business Template {number}',
                'description_template': 'Professional one-page business template #{number} - Clean and modern design'
            },
            r'^jcw-multi(\d+)\.(jpg|png|jpeg)$': {
                'category': 'business', 
                'type': 'multi_page',
                'name_template': 'JCW Multi-Page Template {number}',
                'description_template': 'Multi-page business template #{number} - Complete website solution'
            },
            r'^jcw-shop(\d+)\.(jpg|png|jpeg)$': {
                'category': 'ecommerce',
                'type': 'ecommerce', 
                'name_template': 'JCW E-commerce Template {number}',
                'description_template': 'E-commerce template #{number} - Online store ready'
            }
        }
        
        legacy_templates = []
        existing_templates = set(WebsiteTemplate.objects.values_list('template_id', flat=True))
        
        for preview_file in root_files:
            for pattern, config in template_patterns.items():
                match = re.match(pattern, preview_file)
                if match:
                    number = match.group(1)
                    file_extension = match.group(2)
                    template_id = preview_file.replace(f'.{file_extension}', '')
                    
                    template_info = {
                        'template_id': template_id,
                        'filename': preview_file,
                        'category': config['category'],
                        'type': config['type'],
                        'name': config['name_template'].format(number=number),
                        'description': config['description_template'].format(number=number),
                        'preview_path': f'website_templates/previews/{preview_file}',
                        'thumbnail_path': f'website_templates/thumbnails/{preview_file}',
                        'exists': template_id in existing_templates
                    }
                    legacy_templates.append(template_info)
                    break
        
        return legacy_templates

    def get_template_html(self, template_info):
        """Generate HTML template based on category and type"""
        category = template_info['category']
        template_type = template_info['type']
        
        # Base HTML structure
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ business_name }}}} - {template_info['name']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="{category}-template {template_type}-type">
    <header class="main-header">
        <nav class="navbar">
            <div class="nav-brand">
                <h1>{{{{ business_name }}}}</h1>
            </div>
            <ul class="nav-menu">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>'''
        
        # Add category-specific navigation
        if category == 'restaurant':
            html += '''
                <li><a href="#menu">Menu</a></li>
                <li><a href="#reservations">Reservations</a></li>'''
        elif category == 'portfolio':
            html += '''
                <li><a href="#portfolio">Portfolio</a></li>
                <li><a href="#skills">Skills</a></li>'''
        elif category == 'ecommerce':
            html += '''
                <li><a href="#products">Products</a></li>
                <li><a href="#cart">Cart</a></li>'''
        elif category == 'health':
            html += '''
                <li><a href="#services">Services</a></li>
                <li><a href="#appointments">Appointments</a></li>'''
        else:
            html += '''
                <li><a href="#services">Services</a></li>
                <li><a href="#portfolio">Work</a></li>'''
        
        html += '''
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section id="home" class="hero-section">
            <div class="hero-content">
                <h1>{{{{ business_name }}}}</h1>
                <p class="hero-subtitle">{{{{ business_description }}}}</p>
                <a href="#contact" class="cta-button">Get Started</a>
            </div>
        </section>

        <section id="about" class="about-section">
            <div class="container">
                <h2>About Us</h2>
                <p>{{{{ about_text }}}}</p>
            </div>
        </section>

        <section id="services" class="services-section">
            <div class="container">
                <h2>Our Services</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <h3>Service 1</h3>
                        <p>Professional service description</p>
                    </div>
                    <div class="service-card">
                        <h3>Service 2</h3>
                        <p>Quality service offering</p>
                    </div>
                    <div class="service-card">
                        <h3>Service 3</h3>
                        <p>Expert service solution</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="contact" class="contact-section">
            <div class="container">
                <h2>Contact Us</h2>
                <div class="contact-info">
                    <div class="contact-item">
                        <strong>Phone:</strong> {{{{ phone }}}}
                    </div>
                    <div class="contact-item">
                        <strong>Email:</strong> {{{{ email }}}}
                    </div>
                    <div class="contact-item">
                        <strong>Address:</strong> {{{{ address }}}}
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="main-footer">
        <div class="container">
            <p>&copy; 2025 {{{{ business_name }}}}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''
        
        return html

    def get_template_css(self, template_info):
        """Generate CSS based on category"""
        category = template_info['category']
        
        # Base CSS
        base_css = '''/* Base Template Styles */
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
.main-header {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
    padding: 1rem 0;
}

.navbar {
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
    text-decoration: none;
    transition: color 0.3s;
}

/* Hero Section */
.hero-section {
    padding: 150px 0 100px;
    text-align: center;
}

.hero-content h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.cta-button {
    display: inline-block;
    padding: 12px 30px;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    transition: all 0.3s;
}

/* Sections */
section {
    padding: 80px 0;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.service-card {
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
}

.contact-info {
    display: grid;
    gap: 1rem;
    margin-top: 2rem;
}

.contact-item {
    padding: 1rem;
}

/* Footer */
.main-footer {
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
}

'''
        
        # Category-specific styles
        category_styles = {
            'business': '''
/* Business Template */
.main-header {
    background: #2c3e50;
    color: white;
}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.cta-button {
    background: #3498db;
    color: white;
}

.service-card {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.main-footer {
    background: #2c3e50;
    color: white;
}
''',
            'creative': '''
/* Creative Template */
.main-header {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-menu a {
    color: #333;
}

.hero-section {
    background: linear-gradient(45deg, #ff6b6b, #ffd93d);
    color: white;
}

.cta-button {
    background: #e74c3c;
    color: white;
    border-radius: 25px;
}

.service-card {
    background: white;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    border-left: 4px solid #e74c3c;
}
''',
            'restaurant': '''
/* Restaurant Template */
.main-header {
    background: #8b4513;
    color: white;
}

.hero-section {
    background: linear-gradient(135deg, #d2691e 0%, #8b4513 100%);
    color: white;
}

.cta-button {
    background: #ff6b35;
    color: white;
}

.service-card {
    background: #fff8dc;
    border: 2px solid #ddd;
}
''',
            'health': '''
/* Healthcare Template */
.main-header {
    background: #2c5aa0;
    color: white;
}

.hero-section {
    background: linear-gradient(135deg, #4a90e2 0%, #2c5aa0 100%);
    color: white;
}

.cta-button {
    background: #28a745;
    color: white;
}

.service-card {
    background: #f8f9fa;
    border-top: 3px solid #28a745;
}
''',
            'technology': '''
/* Technology Template */
.main-header {
    background: #1a1a1a;
    color: white;
}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.cta-button {
    background: #007bff;
    color: white;
}

.service-card {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
}
''',
            'construction': '''
/* Construction Template */
.main-header {
    background: #ff6b35;
    color: white;
}

.hero-section {
    background: linear-gradient(135deg, #ff8c42 0%, #ff6b35 100%);
    color: white;
}

.cta-button {
    background: #ffa500;
    color: white;
}

.service-card {
    background: white;
    border-left: 4px solid #ff6b35;
}
''',
            'ecommerce': '''
/* E-commerce Template */
.main-header {
    background: #6c757d;
    color: white;
}

.hero-section {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: white;
}

.cta-button {
    background: #ffc107;
    color: #212529;
}

.service-card {
    background: white;
    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
}
''',
            'portfolio': '''
/* Portfolio Template */
.main-header {
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(10px);
}

.nav-menu a {
    color: #333;
}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.cta-button {
    background: transparent;
    border: 2px solid white;
    color: white;
}

.service-card {
    background: white;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
'''
        }
        
        return base_css + category_styles.get(category, category_styles['business'])