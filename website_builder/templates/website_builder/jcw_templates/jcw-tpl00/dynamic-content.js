/**
 * JCW-TPL00 Dynamic Content System
 * Handles business-type specific content updates for services, about, and contact sections
 */

// Business Type Content Definitions
const JCW_TEMPLATE_CONTENT = {
    services: {
        'automotive': {
            title: 'Our Auto Services',
            subtitle: 'Expert automotive care for your vehicle',
            services: [
                { icon: 'fas fa-car', title: 'Oil Changes', description: 'Regular maintenance to keep your engine running smoothly', color: '#dc3545' },
                { icon: 'fas fa-cog', title: 'Engine Repair', description: 'Professional diagnostics and engine repair services', color: '#28a745' },
                { icon: 'fas fa-tools', title: 'Brake Service', description: 'Complete brake inspection and repair for your safety', color: '#ffc107' },
                { icon: 'fas fa-battery-full', title: 'Battery Service', description: 'Testing, maintenance, and battery replacement services', color: '#17a2b8' },
                { icon: 'fas fa-tire', title: 'Tire Services', description: 'Tire installation, balancing, and alignment services', color: '#6f42c1' },
                { icon: 'fas fa-wrench', title: 'General Maintenance', description: 'Comprehensive vehicle maintenance and inspections', color: '#fd7e14' }
            ]
        },
        'construction': {
            title: 'Construction Services',
            subtitle: 'Building excellence from foundation to finish',
            services: [
                { icon: 'fas fa-home', title: 'Residential Construction', description: 'Custom homes built with quality and craftsmanship', color: '#28a745' },
                { icon: 'fas fa-building', title: 'Commercial Projects', description: 'Professional commercial construction services', color: '#007bff' },
                { icon: 'fas fa-hammer', title: 'Renovations', description: 'Transform your space with expert renovation services', color: '#ffc107' },
                { icon: 'fas fa-hard-hat', title: 'Project Management', description: 'Complete project oversight from start to finish', color: '#dc3545' },
                { icon: 'fas fa-ruler-combined', title: 'Design & Planning', description: 'Architectural design and construction planning', color: '#6f42c1' },
                { icon: 'fas fa-tools', title: 'General Contracting', description: 'Licensed general contracting for all project types', color: '#17a2b8' }
            ]
        },
        'healthcare': {
            title: 'Healthcare Services',
            subtitle: 'Comprehensive care for your health and wellness',
            services: [
                { icon: 'fas fa-stethoscope', title: 'General Medicine', description: 'Primary care and routine health maintenance', color: '#28a745' },
                { icon: 'fas fa-heartbeat', title: 'Cardiology', description: 'Specialized heart and cardiovascular care', color: '#dc3545' },
                { icon: 'fas fa-user-md', title: 'Specialist Care', description: 'Expert medical specialists for complex conditions', color: '#007bff' },
                { icon: 'fas fa-ambulance', title: 'Emergency Care', description: '24/7 emergency medical services', color: '#ffc107' },
                { icon: 'fas fa-pills', title: 'Pharmacy Services', description: 'On-site pharmacy and medication management', color: '#6f42c1' },
                { icon: 'fas fa-clipboard-check', title: 'Health Screenings', description: 'Preventive care and health screening programs', color: '#17a2b8' }
            ]
        },
        'restaurant': {
            title: 'Dining Experience',
            subtitle: 'Exceptional cuisine and memorable dining experiences',
            services: [
                { icon: 'fas fa-utensils', title: 'Fine Dining', description: 'Exquisite cuisine prepared by expert chefs', color: '#fd7e14' },
                { icon: 'fas fa-wine-glass', title: 'Wine Selection', description: 'Curated wine list to complement your meal', color: '#6f42c1' },
                { icon: 'fas fa-birthday-cake', title: 'Special Events', description: 'Private dining and special occasion catering', color: '#e83e8c' },
                { icon: 'fas fa-truck', title: 'Delivery Service', description: 'Fresh meals delivered to your doorstep', color: '#28a745' },
                { icon: 'fas fa-coffee', title: 'Catering', description: 'Professional catering for events and meetings', color: '#17a2b8' },
                { icon: 'fas fa-cocktail', title: 'Bar Service', description: 'Craft cocktails and premium beverage service', color: '#dc3545' }
            ]
        },
        'portfolio': {
            title: 'Creative Services',
            subtitle: 'Innovative design solutions for your brand',
            services: [
                { icon: 'fas fa-paint-brush', title: 'Brand Design', description: 'Complete brand identity and visual design', color: '#6f42c1' },
                { icon: 'fas fa-laptop-code', title: 'Web Development', description: 'Modern, responsive websites and applications', color: '#007bff' },
                { icon: 'fas fa-camera', title: 'Photography', description: 'Professional photography for all your needs', color: '#28a745' },
                { icon: 'fas fa-bullhorn', title: 'Digital Marketing', description: 'Strategic marketing campaigns that deliver results', color: '#dc3545' },
                { icon: 'fas fa-palette', title: 'Graphic Design', description: 'Creative visual solutions for print and digital', color: '#ffc107' },
                { icon: 'fas fa-video', title: 'Video Production', description: 'Professional video content and production services', color: '#17a2b8' }
            ]
        }
    },

    about: {
        'automotive': {
            title: 'About Our Automotive Shop',
            description: 'We are a trusted automotive service center with certified technicians and state-of-the-art equipment. Our team is committed to keeping your vehicle running safely and efficiently with honest, reliable service.',
            mission: 'Our mission is to provide exceptional automotive care that keeps you on the road with confidence. We believe in transparent pricing, quality workmanship, and building lasting relationships with our customers.',
            years: '15+',
            clients: '2000+',
            icon: 'fas fa-car',
            imageText: 'Professional Auto Care',
            gradient: 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)'
        },
        'construction': {
            title: 'About Our Construction Company',
            description: 'We are a full-service construction company specializing in residential and commercial projects. From new builds to renovations, our experienced team delivers quality craftsmanship on time and within budget.',
            mission: 'Our mission is to build lasting relationships through exceptional construction services. We take pride in turning your vision into reality with attention to detail and unwavering commitment to quality.',
            years: '20+',
            clients: '800+',
            icon: 'fas fa-hard-hat',
            imageText: 'Quality Construction',
            gradient: 'linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%)'
        },
        'healthcare': {
            title: 'About Our Healthcare Practice',
            description: 'We are a dedicated healthcare practice focused on providing comprehensive, compassionate care to our patients. Our experienced medical professionals are committed to your health and well-being.',
            mission: 'Our mission is to deliver exceptional healthcare services that promote wellness and improve quality of life. We believe in treating each patient with dignity, respect, and personalized attention.',
            years: '12+',
            clients: '5000+',
            icon: 'fas fa-user-md',
            imageText: 'Compassionate Care',
            gradient: 'linear-gradient(135deg, #28a745 0%, #20c997 100%)'
        },
        'restaurant': {
            title: 'About Our Restaurant',
            description: 'We are a family-owned restaurant passionate about creating memorable dining experiences. Using fresh, locally-sourced ingredients, we craft delicious meals that bring people together.',
            mission: 'Our mission is to provide exceptional food and service in a warm, welcoming atmosphere. We believe that great meals create lasting memories and bring communities together.',
            years: '8+',
            clients: '10000+',
            icon: 'fas fa-utensils',
            imageText: 'Culinary Excellence',
            gradient: 'linear-gradient(135deg, #fd7e14 0%, #e8590c 100%)'
        },
        'portfolio': {
            title: 'About Our Creative Studio',
            description: 'We are a creative studio specializing in innovative design solutions that help brands tell their story. Our talented team combines artistic vision with strategic thinking to deliver impactful results.',
            mission: 'Our mission is to transform ideas into powerful visual experiences that connect brands with their audiences. We believe in the power of creativity to inspire, engage, and drive success.',
            years: '10+',
            clients: '300+',
            icon: 'fas fa-palette',
            imageText: 'Creative Innovation',
            gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }
    },

    contact: {
        'automotive': {
            title: 'Schedule Your Service',
            subtitle: 'Get your vehicle serviced by certified professionals. Contact us today for a free estimate!',
            formTitle: 'Book Your Appointment',
            serviceLabel: 'Service Type',
            serviceOptions: ['Oil Change', 'Brake Repair', 'Engine Diagnostics'],
            address: '456 Auto Service Blvd<br>Mechanic City, ST 54321',
            phone: '(555) CAR-CARE',
            email: 'service@autoshop.com',
            hours: 'Mon-Fri: 7:00 AM - 6:00 PM<br>Sat: 8:00 AM - 4:00 PM<br>Sun: Emergency Only',
            mapTitle: 'Visit Our Shop',
            mapAddress: '456 Auto Service Blvd, Mechanic City, ST'
        },
        'construction': {
            title: 'Start Your Project',
            subtitle: 'Ready to build your dream? Get a free consultation and quote from our expert team!',
            formTitle: 'Request a Quote',
            serviceLabel: 'Project Type',
            serviceOptions: ['New Construction', 'Renovation', 'Commercial Project'],
            address: '789 Builder\'s Way<br>Construction City, ST 67890',
            phone: '(555) BUILD-IT',
            email: 'projects@constructco.com',
            hours: 'Mon-Fri: 6:00 AM - 5:00 PM<br>Sat: 7:00 AM - 3:00 PM<br>Sun: Closed',
            mapTitle: 'Find Our Office',
            mapAddress: '789 Builder\'s Way, Construction City, ST'
        },
        'healthcare': {
            title: 'Book Your Appointment',
            subtitle: 'Your health is our priority. Schedule your appointment with our experienced medical team.',
            formTitle: 'Schedule Appointment',
            serviceLabel: 'Appointment Type',
            serviceOptions: ['General Checkup', 'Specialist Consultation', 'Emergency Care'],
            address: '321 Health Plaza<br>Medical Center, ST 13579',
            phone: '(555) HEALTH-1',
            email: 'appointments@healthcenter.com',
            hours: 'Mon-Fri: 8:00 AM - 6:00 PM<br>Sat: 9:00 AM - 2:00 PM<br>Sun: Emergency Only',
            mapTitle: 'Visit Our Clinic',
            mapAddress: '321 Health Plaza, Medical Center, ST'
        },
        'restaurant': {
            title: 'Make a Reservation',
            subtitle: 'Experience exceptional dining! Reserve your table or place an order for pickup.',
            formTitle: 'Table Reservation',
            serviceLabel: 'Service Type',
            serviceOptions: ['Dine-In Reservation', 'Takeout Order', 'Catering Inquiry'],
            address: '654 Culinary Street<br>Food District, ST 24680',
            phone: '(555) FOOD-YUM',
            email: 'reservations@restaurant.com',
            hours: 'Mon-Thu: 11:00 AM - 10:00 PM<br>Fri-Sat: 11:00 AM - 11:00 PM<br>Sun: 12:00 PM - 9:00 PM',
            mapTitle: 'Find Our Restaurant',
            mapAddress: '654 Culinary Street, Food District, ST'
        },
        'portfolio': {
            title: 'Start Your Project',
            subtitle: 'Let\'s bring your creative vision to life! Contact us to discuss your next project.',
            formTitle: 'Project Inquiry',
            serviceLabel: 'Project Type',
            serviceOptions: ['Web Design', 'Branding', 'Marketing Campaign'],
            address: '987 Creative Ave<br>Design District, ST 97531',
            phone: '(555) CREATE-1',
            email: 'hello@creativestudio.com',
            hours: 'Mon-Fri: 9:00 AM - 6:00 PM<br>Sat: 10:00 AM - 4:00 PM<br>Sun: By Appointment',
            mapTitle: 'Visit Our Studio',
            mapAddress: '987 Creative Ave, Design District, ST'
        }
    }
};

// Default content for unsupported business types
const DEFAULT_CONTENT = {
    services: {
        title: 'Our Services',
        subtitle: 'Discover what we can do for you',
        services: [
            { icon: 'fas fa-cogs', title: 'Professional Service', description: 'High-quality service tailored to your needs', color: '#007bff' },
            { icon: 'fas fa-users', title: 'Expert Team', description: 'Experienced professionals at your service', color: '#28a745' },
            { icon: 'fas fa-clock', title: '24/7 Support', description: 'Always available when you need us', color: '#ffc107' },
            { icon: 'fas fa-shield-alt', title: 'Guaranteed Quality', description: '100% satisfaction guaranteed', color: '#dc3545' },
            { icon: 'fas fa-star', title: 'Premium Experience', description: 'Excellence in every interaction', color: '#6f42c1' },
            { icon: 'fas fa-handshake', title: 'Trusted Partner', description: 'Your reliable business partner', color: '#17a2b8' }
        ]
    },
    about: {
        title: 'About Our Company',
        description: 'We are a professional business dedicated to providing exceptional services to our clients. With years of experience in our industry, we have built a reputation for quality, reliability, and customer satisfaction.',
        mission: 'Our mission is to deliver outstanding results that exceed expectations while maintaining the highest standards of professionalism and integrity in everything we do.',
        years: '10+',
        clients: '500+',
        icon: 'fas fa-building',
        imageText: 'Professional Excellence',
        gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    },
    contact: {
        title: 'Get In Touch',
        subtitle: 'Ready to work with us? Contact us today for more information!',
        formTitle: 'Send us a Message',
        serviceLabel: 'Service Needed',
        serviceOptions: ['Consultation', 'Free Quote', 'General Inquiry'],
        address: '123 Business Street<br>City, State 12345',
        phone: '(555) 123-4567',
        email: 'info@business.com',
        hours: 'Mon-Fri: 9:00 AM - 6:00 PM<br>Sat: 9:00 AM - 4:00 PM<br>Sun: Closed',
        mapTitle: 'Find Our Location',
        mapAddress: '123 Business Street, City, State'
    }
};

/**
 * Update services section content based on business type
 */
function updateServicesContent(businessType) {
    const content = JCW_TEMPLATE_CONTENT.services[businessType] || DEFAULT_CONTENT.services;
    
    // Update titles
    const title = document.getElementById('servicesTitle');
    const subtitle = document.getElementById('servicesSubtitle');
    if (title) title.textContent = content.title;
    if (subtitle) subtitle.textContent = content.subtitle;
    
    // Update services grid
    const grid = document.getElementById('servicesGrid');
    if (grid && content.services) {
        grid.innerHTML = content.services.map(service => `
            <div class="service-card">
                <div class="service-icon" style="background: linear-gradient(135deg, ${service.color} 0%, ${service.color}CC 100%);">
                    <i class="${service.icon}"></i>
                </div>
                <h4 class="service-title">${service.title}</h4>
                <p class="service-description">${service.description}</p>
            </div>
        `).join('');
    }
}

/**
 * Update about section content based on business type
 */
function updateAboutContent(businessType) {
    const content = JCW_TEMPLATE_CONTENT.about[businessType] || DEFAULT_CONTENT.about;
    
    // Update about section elements
    const elements = {
        aboutTitle: content.title,
        aboutDescription: content.description,
        aboutMission: content.mission,
        aboutYears: content.years,
        aboutClients: content.clients,
        aboutImageText: content.imageText
    };
    
    Object.entries(elements).forEach(([id, text]) => {
        const element = document.getElementById(id);
        if (element) element.textContent = text;
    });
    
    // Update icon and gradient
    const icon = document.getElementById('aboutIcon');
    const container = document.getElementById('aboutImageContainer');
    if (icon) icon.className = content.icon;
    if (container) container.style.background = content.gradient;
}

/**
 * Update contact section content based on business type
 */
function updateContactContent(businessType) {
    const content = JCW_TEMPLATE_CONTENT.contact[businessType] || DEFAULT_CONTENT.contact;
    
    // Update contact section elements
    const elements = {
        contactTitle: content.title,
        contactSubtitle: content.subtitle,
        formTitle: content.formTitle,
        serviceLabel: content.serviceLabel,
        businessPhone: content.phone,
        businessEmail: content.email,
        mapTitle: content.mapTitle,
        mapAddress: content.mapAddress
    };
    
    Object.entries(elements).forEach(([id, text]) => {
        const element = document.getElementById(id);
        if (element) {
            if (id === 'businessAddress' || id === 'businessHours') {
                element.innerHTML = text;
            } else {
                element.textContent = text;
            }
        }
    });
    
    // Update address and hours (HTML content)
    const address = document.getElementById('businessAddress');
    const hours = document.getElementById('businessHours');
    if (address) address.innerHTML = content.address;
    if (hours) hours.innerHTML = content.hours;
}

/**
 * Initialize template with business type
 */
function initializeTemplate(businessType = 'default', businessData = {}) {
    // Update all sections
    updateServicesContent(businessType);
    updateAboutContent(businessType);
    updateContactContent(businessType);
    
    // Apply any custom business data
    if (businessData.business_name) {
        const nameElements = document.querySelectorAll('#heroTitle, #aboutImageText');
        nameElements.forEach(el => {
            if (el.textContent.includes('Your Business') || el.textContent.includes('About Our')) {
                el.textContent = el.textContent.replace(/Your Business|About Our \w+/, businessData.business_name);
            }
        });
    }
    
    console.log('JCW-TPL00 initialized for business type:', businessType);
}