from django.core.management.base import BaseCommand
from website_builder.models import WebsiteTemplate


class Command(BaseCommand):
    help = 'Make existing templates visually unique by adding distinctive elements'

    def handle(self, *args, **options):
        templates = WebsiteTemplate.objects.all()
        
        template_variations = {
            'jcw-tpl01': {
                'color_scheme': 'blue',
                'accent_color': '#007bff',
                'hero_bg': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'unique_element': '<div class="template-identifier">Template 1 - Professional Blue</div>'
            },
            'jcw-tpl02': {
                'color_scheme': 'green', 
                'accent_color': '#28a745',
                'hero_bg': 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
                'unique_element': '<div class="template-identifier">Template 2 - Fresh Green</div>'
            },
            'jcw-tpl03': {
                'color_scheme': 'orange',
                'accent_color': '#fd7e14',
                'hero_bg': 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%)',
                'unique_element': '<div class="template-identifier">Template 3 - Vibrant Orange</div>'
            },
            'jcw-tpl04': {
                'color_scheme': 'purple',
                'accent_color': '#6f42c1',
                'hero_bg': 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
                'unique_element': '<div class="template-identifier">Template 4 - Royal Purple</div>'
            },
            'jcw-tpl05': {
                'color_scheme': 'red',
                'accent_color': '#dc3545',
                'hero_bg': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                'unique_element': '<div class="template-identifier">Template 5 - Dynamic Red</div>'
            }
        }
        
        for template in templates:
            if template.template_id in template_variations:
                variation = template_variations[template.template_id]
                
                # Update HTML with unique identifier
                updated_html = self.create_unique_html(template, variation)
                updated_css = self.create_unique_css(template, variation)
                
                template.html_template = updated_html
                template.css_template = updated_css
                template.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✨ Updated {template.template_id} with {variation["color_scheme"]} theme')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Made {templates.count()} templates unique!')
        )

    def create_unique_html(self, template, variation):
        """Create unique HTML with template-specific elements"""
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ business_name }}}} - {template.name}</title>
    <style>
        {self.create_unique_css(template, variation)}
    </style>
</head>
<body class="template-{template.template_id}">
    {variation['unique_element']}
    
    <header class="main-header" style="background: {variation['hero_bg']};">
        <nav class="navbar">
            <div class="nav-brand">
                <h1 style="color: white;">{{{{ business_name }}}}</h1>
                <small style="color: rgba(255,255,255,0.8);">Powered by {template.template_id.upper()}</small>
            </div>
            <ul class="nav-menu">
                <li><a href="#home" style="color: white;">Home</a></li>
                <li><a href="#about" style="color: white;">About</a></li>
                <li><a href="#services" style="color: white;">Services</a></li>
                <li><a href="#contact" style="color: white;">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main style="margin-top: 80px;">
        <section id="home" class="hero-section" style="background: {variation['hero_bg']}; padding: 100px 0; text-align: center;">
            <div class="hero-content">
                <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem;">{{{{ business_name }}}}</h1>
                <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-bottom: 2rem;">{{{{ business_description }}}}</p>
                <div class="template-badge" style="background: rgba(255,255,255,0.2); color: white; padding: 10px 20px; border-radius: 25px; display: inline-block; margin-bottom: 2rem;">
                    🎨 {template.name}
                </div><br>
                <a href="#contact" style="background: {variation['accent_color']}; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">Get Started Today</a>
            </div>
        </section>

        <section id="about" class="about-section" style="padding: 80px 0; background: #f8f9fa;">
            <div class="container" style="max-width: 1200px; margin: 0 auto; text-align: center;">
                <h2 style="color: {variation['accent_color']}; margin-bottom: 2rem;">About {{{{ business_name }}}}</h2>
                <p style="font-size: 1.1rem; color: #666; max-width: 800px; margin: 0 auto;">{{{{ about_text }}}}</p>
                
                <div style="margin-top: 3rem; padding: 20px; background: white; border-left: 4px solid {variation['accent_color']}; border-radius: 8px;">
                    <h3 style="color: {variation['accent_color']};">Template Features for {template.template_id.upper()}</h3>
                    <p style="color: #666;">This template showcases the {variation['color_scheme']} color scheme with modern design elements.</p>
                </div>
            </div>
        </section>

        <section id="services" class="services-section" style="padding: 80px 0;">
            <div class="container" style="max-width: 1200px; margin: 0 auto; text-align: center;">
                <h2 style="color: {variation['accent_color']}; margin-bottom: 3rem;">Our Services</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                    <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-top: 4px solid {variation['accent_color']};">
                        <h3 style="color: {variation['accent_color']}; margin-bottom: 1rem;">Premium Service</h3>
                        <p style="color: #666;">Professional service with {template.template_id} styling</p>
                    </div>
                    <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-top: 4px solid {variation['accent_color']};">
                        <h3 style="color: {variation['accent_color']}; margin-bottom: 1rem;">Quality Solutions</h3>
                        <p style="color: #666;">Expert solutions tailored for your business needs</p>
                    </div>
                    <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-top: 4px solid {variation['accent_color']};">
                        <h3 style="color: {variation['accent_color']}; margin-bottom: 1rem;">Custom Design</h3>
                        <p style="color: #666;">Beautiful {variation['color_scheme']} themed designs</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="contact" class="contact-section" style="padding: 80px 0; background: {variation['hero_bg']};">
            <div class="container" style="max-width: 1200px; margin: 0 auto; text-align: center;">
                <h2 style="color: white; margin-bottom: 2rem;">Contact {{{{ business_name }}}}</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 3rem;">
                    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 10px; color: white;">
                        <strong>📞 Phone:</strong><br>{{{{ phone }}}}
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 10px; color: white;">
                        <strong>📧 Email:</strong><br>{{{{ email }}}}
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 10px; color: white;">
                        <strong>📍 Address:</strong><br>{{{{ address }}}}
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer style="background: #333; color: white; text-align: center; padding: 2rem 0;">
        <div class="container">
            <p>&copy; 2025 {{{{ business_name }}}}. All rights reserved.</p>
            <p style="opacity: 0.7; margin-top: 0.5rem;">Template: {template.name} ({template.template_id})</p>
        </div>
    </footer>

    <script>
        // Auto-scroll functionality for template preview
        let isScrolling = false;
        let scrollDirection = 1;
        let scrollSpeed = 1;
        
        function autoScroll() {{
            if (!isScrolling) return;
            
            const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
            const currentScroll = window.pageYOffset;
            
            if (currentScroll >= maxScroll) {{
                scrollDirection = -1;
            }} else if (currentScroll <= 0) {{
                scrollDirection = 1;
            }}
            
            window.scrollBy(0, scrollDirection * scrollSpeed);
            requestAnimationFrame(autoScroll);
        }}
        
        // Listen for messages from parent window
        window.addEventListener('message', function(event) {{
            if (event.data === 'startScroll') {{
                isScrolling = true;
                autoScroll();
            }} else if (event.data === 'stopScroll') {{
                isScrolling = false;
            }}
        }});
        
        // Template identifier for debugging
        console.log('Template loaded: {template.template_id}');
    </script>
</body>
</html>'''
        return html

    def create_unique_css(self, template, variation):
        """Create unique CSS for each template"""
        return f'''/* {template.name} - {variation['color_scheme'].title()} Theme */
        .template-identifier {{
            position: fixed;
            top: 10px;
            right: 10px;
            background: {variation['accent_color']};
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            z-index: 9999;
            font-weight: bold;
        }}
        
        .template-{template.template_id} {{
            --accent-color: {variation['accent_color']};
            --hero-bg: {variation['hero_bg']};
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Smooth scrolling */
        html {{
            scroll-behavior: smooth;
        }}
        '''