"""
Sample data for Website Builder
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justcodeworks.settings')
django.setup()

from website_builder.models import WebsiteTemplate, IndustryTemplate
import json

def create_sample_templates():
    """Create sample website templates"""
    
    # Template 1: Professional Business
    template1, created = WebsiteTemplate.objects.get_or_create(
        template_id='professional_template_1',
        defaults={
            'name': 'Professional Business',
            'category': 'business',
            'description': 'Clean, modern design perfect for any business. Features service showcase, about section, and contact form.',
            'html_template': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{business_name}}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{{business_name}}</h1>
        <nav>
            <a href="#services">Services</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
        </nav>
    </header>
    
    <section class="hero">
        <h2>{{hero_headline}}</h2>
        <p>{{hero_description}}</p>
        <a href="#contact" class="cta-button">Get Started</a>
    </section>
    
    <section id="services">
        <h2>Our Services</h2>
        <div class="services-grid">
            {{services_content}}
        </div>
    </section>
    
    <section id="about">
        <h2>About Us</h2>
        <p>{{about_content}}</p>
    </section>
    
    <section id="contact">
        <h2>Contact Us</h2>
        <div class="contact-info">
            <p>📍 {{location}}</p>
            <p>📞 {{phone}}</p>
            <p>✉️ {{email}}</p>
        </div>
    </section>
</body>
</html>''',
            'css_template': '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
}

header {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

header h1 {
    display: inline-block;
    margin-left: 2rem;
}

nav {
    float: right;
    margin-right: 2rem;
    margin-top: 0.5rem;
}

nav a {
    color: white;
    text-decoration: none;
    margin-left: 2rem;
    transition: color 0.3s;
}

nav a:hover {
    color: #3498db;
}

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 8rem 2rem 4rem;
    margin-top: 60px;
}

.hero h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.cta-button {
    background: #e74c3c;
    color: white;
    padding: 1rem 2rem;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    transition: background 0.3s;
}

.cta-button:hover {
    background: #c0392b;
}

section {
    padding: 4rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.service-card {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.service-card:hover {
    transform: translateY(-5px);
}

.contact-info {
    background: #ecf0f1;
    padding: 2rem;
    border-radius: 10px;
    margin-top: 1rem;
}

@media (max-width: 768px) {
    .hero h2 {
        font-size: 2rem;
    }
    
    nav {
        display: block;
        text-align: center;
        margin: 1rem 0;
    }
    
    header h1 {
        display: block;
        text-align: center;
        margin: 0;
    }
}''',
            'supports_one_page': True,
            'supports_multi_page': True,
            'color_schemes': ['blue', 'green', 'purple', 'red'],
            'font_options': ['Arial', 'Helvetica', 'Georgia', 'Roboto'],
            'rating': 4.8,
            'usage_count': 156
        }
    )
    
    # Template 2: Industry Expert
    template2, created = WebsiteTemplate.objects.get_or_create(
        template_id='industry_template_2',
        defaults={
            'name': 'Industry Expert',
            'category': 'business',
            'description': 'Professional layout highlighting expertise and experience. Great for service-based businesses.',
            'html_template': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{business_name}} - Industry Expert</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="expert-header">
        <div class="container">
            <h1>{{business_name}}</h1>
            <p class="tagline">{{business_description}}</p>
        </div>
    </header>
    
    <main>
        <section class="expertise">
            <div class="container">
                <h2>Our Expertise</h2>
                <div class="expertise-grid">
                    {{services_content}}
                </div>
            </div>
        </section>
        
        <section class="about">
            <div class="container">
                <h2>Why Choose Us</h2>
                <p>{{about_content}}</p>
            </div>
        </section>
        
        <section class="contact">
            <div class="container">
                <h2>Get In Touch</h2>
                <div class="contact-grid">
                    <div class="contact-item">
                        <h3>Location</h3>
                        <p>{{location}}</p>
                    </div>
                    <div class="contact-item">
                        <h3>Phone</h3>
                        <p>{{phone}}</p>
                    </div>
                    <div class="contact-item">
                        <h3>Email</h3>
                        <p>{{email}}</p>
                    </div>
                </div>
            </div>
        </section>
    </main>
</body>
</html>''',
            'css_template': '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', serif;
    line-height: 1.6;
    color: #2c3e50;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.expert-header {
    background: #34495e;
    color: white;
    padding: 4rem 0;
    text-align: center;
}

.expert-header h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: bold;
}

.tagline {
    font-size: 1.3rem;
    opacity: 0.9;
}

section {
    padding: 4rem 0;
}

.expertise {
    background: #ecf0f1;
}

.expertise h2, .about h2, .contact h2 {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    color: #2c3e50;
}

.expertise-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.expertise-card {
    background: white;
    padding: 2rem;
    border-left: 4px solid #3498db;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.expertise-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 25px rgba(0,0,0,0.15);
}

.about {
    background: white;
}

.about p {
    font-size: 1.2rem;
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
}

.contact {
    background: #2c3e50;
    color: white;
}

.contact h2 {
    color: white;
}

.contact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.contact-item {
    text-align: center;
    padding: 1rem;
}

.contact-item h3 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: #3498db;
}

@media (max-width: 768px) {
    .expert-header h1 {
        font-size: 2rem;
    }
    
    .tagline {
        font-size: 1.1rem;
    }
}''',
            'supports_one_page': True,
            'supports_multi_page': True,
            'color_schemes': ['dark', 'blue', 'red', 'green'],
            'font_options': ['Georgia', 'Arial', 'Roboto', 'Open Sans'],
            'rating': 4.6,
            'usage_count': 89
        }
    )
    
    # Template 3: Modern Corporate
    template3, created = WebsiteTemplate.objects.get_or_create(
        template_id='modern_template_3',
        defaults={
            'name': 'Modern Corporate',
            'category': 'business',
            'description': 'Contemporary design with focus on trust and professionalism. Ideal for established businesses.',
            'html_template': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{business_name}} - Modern Corporate</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="modern-nav">
        <div class="nav-container">
            <div class="logo">{{business_name}}</div>
            <div class="nav-links">
                <a href="#services">Services</a>
                <a href="#about">About</a>
                <a href="#contact">Contact</a>
            </div>
        </div>
    </nav>
    
    <section class="hero-modern">
        <div class="hero-content">
            <h1>{{hero_headline}}</h1>
            <p>{{hero_description}}</p>
            <button class="modern-cta">Learn More</button>
        </div>
    </section>
    
    <section id="services" class="services-modern">
        <div class="container">
            <h2>What We Do</h2>
            <div class="services-flex">
                {{services_content}}
            </div>
        </div>
    </section>
    
    <section id="about" class="about-modern">
        <div class="container">
            <h2>Our Story</h2>
            <p>{{about_content}}</p>
        </div>
    </section>
    
    <section id="contact" class="contact-modern">
        <div class="container">
            <h2>Connect With Us</h2>
            <div class="contact-modern-grid">
                <div class="contact-card">
                    <div class="contact-icon">📍</div>
                    <h3>Visit Us</h3>
                    <p>{{location}}</p>
                </div>
                <div class="contact-card">
                    <div class="contact-icon">📞</div>
                    <h3>Call Us</h3>
                    <p>{{phone}}</p>
                </div>
                <div class="contact-card">
                    <div class="contact-icon">✉️</div>
                    <h3>Email Us</h3>
                    <p>{{email}}</p>
                </div>
            </div>
        </div>
    </section>
</body>
</html>''',
            'css_template': '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Montserrat', sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.modern-nav {
    background: white;
    box-shadow: 0 2px 20px rgba(0,0,0,0.1);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.nav-links a {
    text-decoration: none;
    color: #333;
    margin-left: 2rem;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #667eea;
}

.hero-modern {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-top: 80px;
}

.hero-content h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
}

.hero-content p {
    font-size: 1.3rem;
    margin-bottom: 2rem;
    max-width: 600px;
}

.modern-cta {
    background: white;
    color: #667eea;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.modern-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.services-modern {
    padding: 6rem 0;
    background: #f8f9fa;
}

.services-modern h2 {
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 3rem;
    color: #2c3e50;
}

.services-flex {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    justify-content: center;
}

.service-modern-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
    max-width: 350px;
    text-align: center;
    transition: transform 0.3s ease;
}

.service-modern-card:hover {
    transform: translateY(-5px);
}

.about-modern {
    padding: 6rem 0;
    background: white;
}

.about-modern h2 {
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    color: #2c3e50;
}

.about-modern p {
    font-size: 1.2rem;
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
    color: #666;
}

.contact-modern {
    padding: 6rem 0;
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    color: white;
}

.contact-modern h2 {
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 3rem;
    color: white;
}

.contact-modern-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.contact-card {
    background: rgba(255,255,255,0.1);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.contact-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.contact-card h3 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: #3498db;
}

@media (max-width: 768px) {
    .hero-content h1 {
        font-size: 2.5rem;
    }
    
    .nav-links {
        display: none;
    }
    
    .services-flex {
        flex-direction: column;
        align-items: center;
    }
}''',
            'supports_one_page': True,
            'supports_multi_page': True,
            'color_schemes': ['gradient', 'minimal', 'corporate', 'dark'],
            'font_options': ['Montserrat', 'Lato', 'Source Sans Pro', 'Roboto'],
            'rating': 4.9,
            'usage_count': 203
        }
    )
    
    return [template1, template2, template3]

def create_industry_templates():
    """Create industry-specific templates"""
    
    # Construction Industry
    construction, created = IndustryTemplate.objects.get_or_create(
        industry_name='construction',
        defaults={
            'display_name': 'Construction & Building',
            'description': 'Templates and content for construction, renovation, and building services',
            'common_services': [
                'Home Renovation', 'Kitchen Remodeling', 'Bathroom Renovation',
                'Flooring Installation', 'Painting Services', 'Roofing',
                'Plumbing', 'Electrical Work', 'General Contracting'
            ],
            'business_description_template': 'We are a trusted construction company with years of experience in delivering quality building services. Our skilled team specializes in residential and commercial projects.',
            'services_intro_template': 'Our comprehensive construction services cover everything from small repairs to major renovations.',
            'about_us_template': 'Founded with a commitment to quality and customer satisfaction, we have built our reputation on delivering exceptional construction services.',
            'common_keywords': ['construction', 'renovation', 'building', 'contractor', 'remodeling'],
            'target_audience_suggestions': ['Homeowners', 'Property developers', 'Business owners', 'Real estate investors'],
            'recommended_colors': ['#2c3e50', '#e74c3c', '#f39c12', '#27ae60']
        }
    )
    
    # Technology Industry
    technology, created = IndustryTemplate.objects.get_or_create(
        industry_name='technology',
        defaults={
            'display_name': 'Technology & IT',
            'description': 'Templates for tech companies, software developers, and IT service providers',
            'common_services': [
                'Web Development', 'Mobile App Development', 'Software Consulting',
                'IT Support', 'Cloud Services', 'Cybersecurity',
                'Database Management', 'UI/UX Design', 'Digital Marketing'
            ],
            'business_description_template': 'We are a cutting-edge technology company providing innovative software solutions and IT services to help businesses thrive in the digital age.',
            'services_intro_template': 'Our technology services span from custom software development to comprehensive IT support.',
            'about_us_template': 'With expertise in modern technologies and a passion for innovation, we deliver solutions that drive business growth.',
            'common_keywords': ['technology', 'software', 'IT', 'web development', 'digital'],
            'target_audience_suggestions': ['Small businesses', 'Startups', 'Enterprises', 'E-commerce companies'],
            'recommended_colors': ['#3498db', '#9b59b6', '#1abc9c', '#34495e']
        }
    )
    
    # Healthcare Industry  
    healthcare, created = IndustryTemplate.objects.get_or_create(
        industry_name='health',
        defaults={
            'display_name': 'Healthcare & Wellness',
            'description': 'Templates for medical practices, clinics, and wellness services',
            'common_services': [
                'General Consultation', 'Preventive Care', 'Health Screenings',
                'Wellness Programs', 'Nutrition Counseling', 'Physical Therapy',
                'Mental Health Support', 'Chronic Disease Management', 'Emergency Care'
            ],
            'business_description_template': 'We provide comprehensive healthcare services with a focus on patient care and wellness. Our experienced medical professionals are committed to your health.',
            'services_intro_template': 'Our healthcare services are designed to promote wellness and provide quality medical care for all ages.',
            'about_us_template': 'Dedicated to improving community health through compassionate care and modern medical practices.',
            'common_keywords': ['healthcare', 'medical', 'wellness', 'clinic', 'doctor'],
            'target_audience_suggestions': ['Patients', 'Families', 'Senior citizens', 'Health-conscious individuals'],
            'recommended_colors': ['#2ecc71', '#3498db', '#ffffff', '#ecf0f1']
        }
    )
    
    return [construction, technology, healthcare]

if __name__ == '__main__':
    print("Creating sample website templates...")
    templates = create_sample_templates()
    print(f"Created {len(templates)} website templates")
    
    print("Creating industry templates...")
    industries = create_industry_templates()
    print(f"Created {len(industries)} industry templates")
    
    print("Sample data creation complete!")