"""
Management command to create a single, high-quality template
Focus on one excellent template instead of multiple mediocre ones
"""
import os
from django.core.management.base import BaseCommand
from website_builder.models import WebsiteTemplate


class Command(BaseCommand):
    help = 'Create one high-quality professional template'

    def handle(self, *args, **options):
        """Create a single, excellent template"""
        
        # Remove existing templates
        WebsiteTemplate.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('🗑️ Cleared existing templates'))
        
        # Create one high-quality template
        template = WebsiteTemplate.objects.create(
            template_id='professional_universal_v1',
            name='Professional Business Universal',
            category='business',
            description='A versatile, modern template perfect for any business. Features responsive design, service showcase, about section, testimonials, and contact form. Fully customizable colors and content.',
            
            # HTML Template
            html_template=self.get_html_template(),
            
            # CSS Template
            css_template=self.get_css_template(),
            
            # JS Template
            js_template=self.get_js_template(),
            
            # Configuration
            supports_one_page=True,
            supports_multi_page=False,
            color_schemes=[
                'professional-blue', 'modern-green', 'corporate-gray', 
                'creative-purple', 'warm-orange', 'clean-teal'
            ],
            font_options=['Inter', 'Roboto', 'Open Sans', 'Poppins', 'Lato'],
            
            # Preview images
            preview_image='https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop',
            thumbnail_image='https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop',
            demo_url='https://demo.justcodeworks.eu/professional-universal',
            
            # Stats
            usage_count=0,
            rating=5.0,
            is_active=True,
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Created excellent template: {template.name}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'   Template ID: {template.template_id}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'   Description: {template.description}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'   Color Schemes: {len(template.color_schemes)} options')
        )
        self.stdout.write(
            self.style.SUCCESS(f'   Font Options: {len(template.font_options)} choices')
        )
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Single high-quality template created successfully!')
        )
        self.stdout.write(
            self.style.SUCCESS('This template can be customized for any business type.'))

    def get_html_template(self):
        """Return the HTML template structure"""
        return '''<!DOCTYPE html>
<html lang="{{language|default:'en'}}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{business_name}} - {{tagline|default:'Professional Services'}}</title>
    <meta name="description" content="{{meta_description}}">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <style>{{custom_css}}</style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="#">{{business_name}}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="#services">Services</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero-section">
        <div class="container">
            <div class="row align-items-center min-vh-100">
                <div class="col-lg-6">
                    <h1 class="display-4 fw-bold mb-4">{{hero_headline}}</h1>
                    <p class="lead mb-4">{{hero_description}}</p>
                    <div class="hero-buttons">
                        <a href="#services" class="btn btn-primary btn-lg me-3">Our Services</a>
                        <a href="#contact" class="btn btn-outline-primary btn-lg">Get In Touch</a>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="hero-image">
                        <img src="{{hero_image|default:'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=600&h=400&fit=crop'}}" 
                             class="img-fluid rounded shadow" alt="{{business_name}}">
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-5 bg-light">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 text-center mb-5">
                    <h2 class="fw-bold">About {{business_name}}</h2>
                    <div class="section-divider"></div>
                </div>
            </div>
            <div class="row align-items-center">
                <div class="col-lg-6">
                    <h3>{{about_headline|default:'Our Story'}}</h3>
                    <p>{{about_content}}</p>
                    <div class="about-stats">
                        <div class="row text-center">
                            <div class="col-4">
                                <h4 class="text-primary">{{years_experience|default:'10+'}}></h4>
                                <small>Years Experience</small>
                            </div>
                            <div class="col-4">
                                <h4 class="text-primary">{{happy_clients|default:'500+'}}></h4>
                                <small>Happy Clients</small>
                            </div>
                            <div class="col-4">
                                <h4 class="text-primary">{{projects_completed|default:'1000+'}}></h4>
                                <small>Projects</small>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <img src="{{about_image|default:'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&h=400&fit=crop'}}" 
                         class="img-fluid rounded shadow" alt="About Us">
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="py-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 text-center mb-5">
                    <h2 class="fw-bold">Our Services</h2>
                    <div class="section-divider"></div>
                    <p class="lead">{{services_intro|default:'We provide professional services tailored to your needs'}}</p>
                </div>
            </div>
            <div class="row">
                {{#each services}}
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="service-card h-100">
                        <div class="service-icon">
                            <i class="{{icon|default:'fas fa-cogs'}}"></i>
                        </div>
                        <h4>{{name}}</h4>
                        <p>{{description}}</p>
                    </div>
                </div>
                {{/each}}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-5 bg-primary text-white">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 text-center mb-5">
                    <h2 class="fw-bold">Get In Touch</h2>
                    <div class="section-divider bg-white"></div>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-6">
                    <h4>Contact Information</h4>
                    <div class="contact-info">
                        <div class="contact-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>{{address}}</span>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-phone"></i>
                            <span>{{phone}}</span>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-envelope"></i>
                            <span>{{email}}</span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <form class="contact-form">
                        <div class="mb-3">
                            <input type="text" class="form-control" placeholder="Your Name" required>
                        </div>
                        <div class="mb-3">
                            <input type="email" class="form-control" placeholder="Your Email" required>
                        </div>
                        <div class="mb-3">
                            <textarea class="form-control" rows="5" placeholder="Your Message" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-light btn-lg w-100">Send Message</button>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4">
        <div class="container">
            <div class="row">
                <div class="col-lg-6">
                    <p>&copy; 2025 {{business_name}}. All rights reserved.</p>
                </div>
                <div class="col-lg-6 text-end">
                    <p>Powered by <a href="https://justcodeworks.eu" class="text-white">JustCodeWorks</a></p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>{{custom_js}}</script>
</body>
</html>'''

    def get_css_template(self):
        """Return the CSS template"""
        return '''/* Professional Universal Template CSS */
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --info-color: #17a2b8;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --light-color: #f8f9fa;
    --dark-color: #343a40;
    --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

body {
    font-family: var(--font-family);
    line-height: 1.6;
    color: var(--dark-color);
}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
    color: white;
    padding-top: 80px;
}

.hero-buttons .btn {
    border-radius: 50px;
    padding: 12px 30px;
    font-weight: 600;
}

/* Section Divider */
.section-divider {
    width: 80px;
    height: 4px;
    background: var(--primary-color);
    margin: 0 auto 2rem;
    border-radius: 2px;
}

.section-divider.bg-white {
    background: white;
}

/* Service Cards */
.service-card {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #f0f0f0;
}

.service-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.15);
}

.service-icon {
    font-size: 3rem;
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.service-card h4 {
    color: var(--dark-color);
    font-weight: 600;
    margin-bottom: 1rem;
}

/* Contact Section */
.contact-info {
    margin-top: 2rem;
}

.contact-item {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.contact-item i {
    width: 25px;
    margin-right: 15px;
    font-size: 1.2rem;
}

.contact-form .form-control {
    border-radius: 10px;
    border: none;
    padding: 15px;
    font-size: 1rem;
}

.contact-form .form-control:focus {
    box-shadow: 0 0 0 0.25rem rgba(255,255,255,0.25);
}

/* About Stats */
.about-stats {
    margin-top: 2rem;
    padding: 2rem;
    background: white;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-section {
        text-align: center;
    }
    
    .hero-buttons {
        margin-top: 2rem;
    }
    
    .hero-buttons .btn {
        display: block;
        width: 100%;
        margin-bottom: 1rem;
    }
    
    .service-card {
        margin-bottom: 2rem;
    }
}

/* Smooth Scrolling */
html {
    scroll-behavior: smooth;
}

/* Navbar Styling */
.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
}

.navbar-nav .nav-link {
    font-weight: 500;
    margin: 0 10px;
    transition: color 0.3s ease;
}

.navbar-nav .nav-link:hover {
    color: var(--warning-color) !important;
}'''

    def get_js_template(self):
        """Return the JavaScript template"""
        return '''// Professional Universal Template JS

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Contact form handling
document.querySelector('.contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(this);
    const name = this.querySelector('input[type="text"]').value;
    const email = this.querySelector('input[type="email"]').value;
    const message = this.querySelector('textarea').value;
    
    // Simple validation
    if (!name || !email || !message) {
        alert('Please fill in all fields.');
        return;
    }
    
    // Simulate form submission
    const button = this.querySelector('button[type="submit"]');
    const originalText = button.textContent;
    button.textContent = 'Sending...';
    button.disabled = true;
    
    setTimeout(() => {
        alert('Thank you for your message! We will get back to you soon.');
        this.reset();
        button.textContent = originalText;
        button.disabled = false;
    }, 2000);
});

// Animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe service cards
document.querySelectorAll('.service-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});'''