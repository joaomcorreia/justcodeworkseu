/**
 * JCW Template 01 - AI-Powered Dynamic Content System
 * Integrates with MagicAI plugin at tools.justcodeworks.net
 * Supports dynamic card generation (3-9 cards per section)
 */

class JCWTemplate01 {
    constructor() {
        this.magicAIEndpoint = '/tools/magicai/';
        this.maxCards = 9;
        this.minCards = 3;
        this.businessData = this.loadBusinessData();
        this.initializeTemplate();
    }

    initializeTemplate() {
        console.log('JCW-TPL01: AI-Powered Template Initialized');
        this.generateDynamicSections();
        this.setupEventListeners();
    }

    loadBusinessData() {
        // Load business data from JCW-TPL00 or localStorage
        const stored = localStorage.getItem('jcw_business_data');
        return stored ? JSON.parse(stored) : {
            businessName: 'Your Business',
            businessType: 'general',
            services: [],
            aboutText: '',
            contactInfo: {}
        };
    }

    generateDynamicSections() {
        // Generate initial cards based on business data
        this.generateServicesCards();
        this.generateBlogCards();
        this.generateTeamCards();
        this.generateFAQCards();
        this.updateNavigationVisibility();
    }

    generateServicesCards() {
        const container = document.getElementById('dynamicServicesContainer');
        if (!container) return;

        const services = this.businessData.services || this.getDefaultServices();
        const cardsToGenerate = Math.min(services.length, this.maxCards);

        container.innerHTML = '';
        for (let i = 0; i < cardsToGenerate; i++) {
            const service = services[i] || this.getDefaultService(i);
            container.appendChild(this.createServiceCard(service, i));
        }

        this.updateCardControls('services', cardsToGenerate);
    }

    generateBlogCards() {
        const container = document.getElementById('dynamicBlogContainer');
        if (!container) return;

        const blogPosts = this.getDefaultBlogPosts();
        const cardsToGenerate = Math.min(blogPosts.length, 3); // Start with 3 blog posts

        container.innerHTML = '';
        for (let i = 0; i < cardsToGenerate; i++) {
            container.appendChild(this.createBlogCard(blogPosts[i], i));
        }

        this.updateCardControls('blog', cardsToGenerate);
    }

    generateTeamCards() {
        const container = document.getElementById('dynamicTeamContainer');
        if (!container) return;

        const teamMembers = this.getDefaultTeamMembers();
        const cardsToGenerate = Math.min(teamMembers.length, 3); // Start with 3 team members

        container.innerHTML = '';
        for (let i = 0; i < cardsToGenerate; i++) {
            container.appendChild(this.createTeamCard(teamMembers[i], i));
        }

        this.updateCardControls('team', cardsToGenerate);
    }

    generateFAQCards() {
        const container = document.getElementById('dynamicFAQContainer');
        if (!container) return;

        const faqs = this.getDefaultFAQs();
        const cardsToGenerate = Math.min(faqs.length, 3); // Start with 3 FAQs

        container.innerHTML = '';
        for (let i = 0; i < cardsToGenerate; i++) {
            container.appendChild(this.createFAQCard(faqs[i], i));
        }

        this.updateCardControls('faq', cardsToGenerate);
    }

    createServiceCard(service, index) {
        const card = document.createElement('div');
        card.className = 'col-lg-4 col-md-6 mb-4';
        card.innerHTML = `
            <div class="content-card h-100 text-center">
                <div class="mb-3">
                    <i class="${service.icon} fa-3x text-success"></i>
                </div>
                <h5 class="mb-3">${service.title}</h5>
                <p class="mb-3">${service.description}</p>
                <div class="card-controls">
                    <button class="ai-edit-btn small" onclick="editServiceCard(${index})">
                        <i class="fas fa-magic"></i> Edit AI
                    </button>
                    <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeCard('services', ${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
        return card;
    }

    createBlogCard(post, index) {
        const card = document.createElement('div');
        card.className = 'col-lg-4 col-md-6 mb-4';
        card.innerHTML = `
            <div class="content-card h-100">
                <img src="${post.image}" class="card-img-top" alt="${post.title}" style="height: 200px; object-fit: cover;">
                <div class="card-body">
                    <h6 class="card-title">${post.title}</h6>
                    <p class="card-text small">${post.excerpt}</p>
                    <small class="text-muted">${post.date}</small>
                    <div class="card-controls mt-3">
                        <button class="ai-edit-btn small" onclick="editBlogCard(${index})">
                            <i class="fas fa-magic"></i> Edit AI
                        </button>
                        <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeCard('blog', ${index})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        return card;
    }

    createTeamCard(member, index) {
        const card = document.createElement('div');
        card.className = 'col-lg-4 col-md-6 mb-4';
        card.innerHTML = `
            <div class="content-card text-center h-100">
                <img src="${member.photo}" class="rounded-circle mb-3" alt="${member.name}" style="width: 100px; height: 100px; object-fit: cover;">
                <h6>${member.name}</h6>
                <p class="text-muted small mb-2">${member.position}</p>
                <p class="small">${member.bio}</p>
                <div class="card-controls">
                    <button class="ai-edit-btn small" onclick="editTeamCard(${index})">
                        <i class="fas fa-magic"></i> Edit AI
                    </button>
                    <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeCard('team', ${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
        return card;
    }

    createFAQCard(faq, index) {
        const card = document.createElement('div');
        card.className = 'col-12 mb-3';
        card.innerHTML = `
            <div class="content-card">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="mb-2">${faq.question}</h6>
                        <p class="mb-0 small text-muted">${faq.answer}</p>
                    </div>
                    <div class="card-controls ms-3">
                        <button class="ai-edit-btn small" onclick="editFAQCard(${index})">
                            <i class="fas fa-magic"></i> Edit AI
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="removeCard('faq', ${index})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        return card;
    }

    addCard(section) {
        const container = document.getElementById(`dynamic${this.capitalize(section)}Container`);
        if (!container) return;

        const currentCount = container.children.length;
        if (currentCount >= this.maxCards) {
            alert(`Maximum of ${this.maxCards} ${section} allowed`);
            return;
        }

        let newCard;
        switch (section) {
            case 'services':
                newCard = this.createServiceCard(this.getDefaultService(currentCount), currentCount);
                break;
            case 'blog':
                newCard = this.createBlogCard(this.getDefaultBlogPost(currentCount), currentCount);
                break;
            case 'team':
                newCard = this.createTeamCard(this.getDefaultTeamMember(currentCount), currentCount);
                break;
            case 'faq':
                newCard = this.createFAQCard(this.getDefaultFAQ(currentCount), currentCount);
                break;
        }

        if (newCard) {
            container.appendChild(newCard);
            this.updateCardControls(section, currentCount + 1);
        }
    }

    removeCard(section, index) {
        const container = document.getElementById(`dynamic${this.capitalize(section)}Container`);
        if (!container) return;

        const cards = Array.from(container.children);
        if (cards.length <= this.minCards) {
            alert(`Minimum of ${this.minCards} ${section} required`);
            return;
        }

        if (cards[index]) {
            cards[index].remove();
            this.updateCardControls(section, cards.length - 1);
            this.reindexCards(section);
        }
    }

    reindexCards(section) {
        const container = document.getElementById(`dynamic${this.capitalize(section)}Container`);
        if (!container) return;

        Array.from(container.children).forEach((card, index) => {
            // Update button onclick handlers with new index
            const editBtn = card.querySelector('.ai-edit-btn');
            const removeBtn = card.querySelector('.btn-outline-danger');
            
            if (editBtn) editBtn.setAttribute('onclick', `edit${this.capitalize(section)}Card(${index})`);
            if (removeBtn) removeBtn.setAttribute('onclick', `removeCard('${section}', ${index})`);
        });
    }

    updateCardControls(section, count) {
        const addBtn = document.querySelector(`[onclick="addCard('${section}')"]`);
        if (addBtn) {
            addBtn.style.display = count >= this.maxCards ? 'none' : 'inline-block';
        }
    }

    updateNavigationVisibility() {
        const teamContainer = document.getElementById('dynamicTeamContainer');
        const teamNavItem = document.querySelector('a[href="#team"]');
        
        if (teamContainer && teamNavItem) {
            const hasTeamMembers = teamContainer.children.length > 0;
            teamNavItem.parentElement.style.display = hasTeamMembers ? 'block' : 'none';
        }
    }

    setupEventListeners() {
        // Contact form handling
        const contactForm = document.getElementById('contactForm');
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleContactForm(e);
            });
        }

        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    handleContactForm(e) {
        const formData = new FormData(e.target);
        console.log('Contact form submitted:', Object.fromEntries(formData));
        alert('Thank you for your message! We will get back to you soon.');
        e.target.reset();
    }

    // AI Content Generation Methods
    async generateAIContent(section, context = {}) {
        const prompt = this.buildPromptForSection(section, context);
        
        try {
            const response = await fetch(this.magicAIEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    prompt: prompt,
                    businessType: this.businessData.businessType,
                    section: section
                })
            });

            if (!response.ok) throw new Error('AI generation failed');
            
            const result = await response.json();
            return result.content;
        } catch (error) {
            console.error('AI Content Generation Error:', error);
            return this.getFallbackContent(section);
        }
    }

    buildPromptForSection(section, context) {
        const businessType = this.businessData.businessType || 'general business';
        const businessName = this.businessData.businessName || 'Your Business';

        const prompts = {
            hero: `Create compelling hero section content for ${businessName}, a ${businessType} company. Include headline, subtitle, and call-to-action.`,
            about: `Write an engaging about section for ${businessName}, a ${businessType} company. Focus on expertise, experience, and value proposition.`,
            services: `Generate professional service descriptions for ${businessName}, a ${businessType} company. Create ${context.count || 6} services with titles, descriptions, and appropriate icons.`,
            blog: `Create ${context.count || 3} relevant blog post titles and excerpts for ${businessName}, a ${businessType} company.`,
            team: `Generate ${context.count || 3} team member profiles for ${businessName}, including names, positions, and brief bios.`,
            faq: `Create ${context.count || 5} frequently asked questions and answers for ${businessName}, a ${businessType} company.`,
            contact: `Write contact section content for ${businessName}, including compelling call-to-action and business benefits.`
        };

        return prompts[section] || `Generate professional content for ${section} section of ${businessName} website.`;
    }

    getFallbackContent(section) {
        // Return default content if AI generation fails
        const fallbacks = {
            hero: { headline: 'Professional Business Solutions', subtitle: 'Excellence in every service we provide' },
            about: { text: 'We are dedicated to providing exceptional service and delivering outstanding results for our clients.' },
            services: this.getDefaultServices(),
            blog: this.getDefaultBlogPosts(),
            team: this.getDefaultTeamMembers(),
            faq: this.getDefaultFAQs()
        };
        return fallbacks[section] || {};
    }

    // Default Content Generators
    getDefaultServices() {
        const serviceTemplates = {
            construction: [
                { icon: 'fas fa-hammer', title: 'Home Renovation', description: 'Complete home renovation services from kitchen remodels to full house makeovers.' },
                { icon: 'fas fa-wrench', title: 'Plumbing Services', description: 'Professional plumbing installation, repair, and maintenance services.' },
                { icon: 'fas fa-bolt', title: 'Electrical Work', description: 'Licensed electrical services for residential and commercial properties.' },
                { icon: 'fas fa-paint-brush', title: 'Painting & Decorating', description: 'Interior and exterior painting services with premium materials.' },
                { icon: 'fas fa-tools', title: 'General Repairs', description: 'Comprehensive repair services for all your maintenance needs.' },
                { icon: 'fas fa-home', title: 'New Construction', description: 'Custom home building and commercial construction projects.' }
            ],
            technology: [
                { icon: 'fas fa-code', title: 'Web Development', description: 'Custom web applications and responsive website development.' },
                { icon: 'fas fa-mobile-alt', title: 'Mobile Apps', description: 'Native and cross-platform mobile application development.' },
                { icon: 'fas fa-cloud', title: 'Cloud Solutions', description: 'Scalable cloud infrastructure and migration services.' },
                { icon: 'fas fa-shield-alt', title: 'Cybersecurity', description: 'Comprehensive security solutions to protect your business.' },
                { icon: 'fas fa-chart-line', title: 'Data Analytics', description: 'Business intelligence and data visualization solutions.' },
                { icon: 'fas fa-cogs', title: 'IT Support', description: '24/7 technical support and system maintenance services.' }
            ],
            general: [
                { icon: 'fas fa-star', title: 'Premium Service', description: 'High-quality service tailored to your specific needs and requirements.' },
                { icon: 'fas fa-users', title: 'Expert Team', description: 'Experienced professionals dedicated to delivering exceptional results.' },
                { icon: 'fas fa-clock', title: 'Timely Delivery', description: 'Reliable service delivery within agreed timelines and budgets.' },
                { icon: 'fas fa-handshake', title: 'Client Focus', description: 'Personalized approach ensuring complete client satisfaction.' },
                { icon: 'fas fa-award', title: 'Quality Guarantee', description: 'Committed to excellence with our comprehensive quality assurance.' },
                { icon: 'fas fa-phone', title: '24/7 Support', description: 'Round-the-clock customer support for all your service needs.' }
            ]
        };

        const businessType = this.businessData.businessType || 'general';
        return serviceTemplates[businessType] || serviceTemplates.general;
    }

    getDefaultService(index) {
        const services = this.getDefaultServices();
        return services[index % services.length];
    }

    getDefaultBlogPosts() {
        return [
            {
                title: 'Industry Best Practices',
                excerpt: 'Discover the latest trends and best practices in our industry.',
                image: 'https://via.placeholder.com/400x200?text=Blog+Post+1',
                date: 'March 15, 2024'
            },
            {
                title: 'Success Stories',
                excerpt: 'Read about our recent successful projects and client achievements.',
                image: 'https://via.placeholder.com/400x200?text=Blog+Post+2',
                date: 'March 10, 2024'
            },
            {
                title: 'Expert Tips',
                excerpt: 'Professional tips and insights from our experienced team.',
                image: 'https://via.placeholder.com/400x200?text=Blog+Post+3',
                date: 'March 5, 2024'
            }
        ];
    }

    getDefaultBlogPost(index) {
        const posts = this.getDefaultBlogPosts();
        return posts[index % posts.length];
    }

    getDefaultTeamMembers() {
        return [
            {
                name: 'John Smith',
                position: 'CEO & Founder',
                bio: 'Leading our team with 15+ years of industry experience.',
                photo: 'https://via.placeholder.com/150x150?text=Team+Member+1'
            },
            {
                name: 'Sarah Johnson',
                position: 'Operations Manager',
                bio: 'Ensuring smooth operations and exceptional service delivery.',
                photo: 'https://via.placeholder.com/150x150?text=Team+Member+2'
            },
            {
                name: 'Mike Davis',
                position: 'Technical Lead',
                bio: 'Expert technical guidance for all our projects and solutions.',
                photo: 'https://via.placeholder.com/150x150?text=Team+Member+3'
            }
        ];
    }

    getDefaultTeamMember(index) {
        const members = this.getDefaultTeamMembers();
        return members[index % members.length];
    }

    getDefaultFAQs() {
        return [
            {
                question: 'What services do you offer?',
                answer: 'We provide a comprehensive range of professional services tailored to meet your specific business needs and requirements.'
            },
            {
                question: 'How long does a typical project take?',
                answer: 'Project timelines vary depending on scope and complexity. We provide detailed timelines during our initial consultation.'
            },
            {
                question: 'Do you offer support after project completion?',
                answer: 'Yes, we provide ongoing support and maintenance services to ensure your continued success and satisfaction.'
            },
            {
                question: 'How do you ensure quality?',
                answer: 'We follow industry best practices and have comprehensive quality assurance processes throughout every project phase.'
            },
            {
                question: 'What are your pricing options?',
                answer: 'We offer flexible pricing options tailored to your budget and requirements. Contact us for a personalized quote.'
            }
        ];
    }

    getDefaultFAQ(index) {
        const faqs = this.getDefaultFAQs();
        return faqs[index % faqs.length];
    }

    // Utility Methods
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }
}

// Global Functions for Template Interaction
window.editContent = function(section) {
    console.log(`Edit AI content for section: ${section}`);
    // This will integrate with MagicAI plugin
    if (window.jcwTemplate01) {
        window.jcwTemplate01.generateAIContent(section).then(content => {
            console.log('Generated content:', content);
            // Update the section with new content
        });
    }
};

window.addCard = function(section) {
    if (window.jcwTemplate01) {
        window.jcwTemplate01.addCard(section);
    }
};

window.removeCard = function(section, index) {
    if (window.jcwTemplate01) {
        window.jcwTemplate01.removeCard(section, index);
    }
};

window.editServiceCard = function(index) {
    console.log(`Edit service card ${index} with AI`);
    if (window.jcwTemplate01) {
        window.jcwTemplate01.generateAIContent('services', { index, count: 1 });
    }
};

window.editBlogCard = function(index) {
    console.log(`Edit blog card ${index} with AI`);
    if (window.jcwTemplate01) {
        window.jcwTemplate01.generateAIContent('blog', { index, count: 1 });
    }
};

window.editTeamCard = function(index) {
    console.log(`Edit team card ${index} with AI`);
    if (window.jcwTemplate01) {
        window.jcwTemplate01.generateAIContent('team', { index, count: 1 });
    }
};

window.editFAQCard = function(index) {
    console.log(`Edit FAQ card ${index} with AI`);
    if (window.jcwTemplate01) {
        window.jcwTemplate01.generateAIContent('faq', { index, count: 1 });
    }
};

// Initialize Template when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.jcwTemplate01 = new JCWTemplate01();
    console.log('JCW-TPL01 AI-Powered Template System Ready');
});