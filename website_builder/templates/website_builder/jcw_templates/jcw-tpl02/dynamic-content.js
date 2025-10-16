/**
 * JCW Template 02 - Agriculture & Organic Dynamic Content System
 * Specialized for agriculture, organic farming, and food production businesses
 * Supports dynamic card generation (3-9 cards per section)
 */

class JCWTemplate02 {
    constructor() {
        this.magicAIEndpoint = '/tools/magicai/';
        this.maxCards = 9;
        this.minCards = 3;
        this.businessData = this.loadBusinessData();
        this.initializeTemplate();
    }

    initializeTemplate() {
        console.log('JCW-TPL02: Agriculture Template Initialized');
        this.generateDynamicSections();
        this.setupEventListeners();
    }

    loadBusinessData() {
        // Load business data from JCW-TPL00 or localStorage
        const stored = localStorage.getItem('jcw_business_data');
        return stored ? JSON.parse(stored) : {
            businessName: 'Agriculture Co.',
            businessType: 'agriculture',
            services: [],
            aboutText: '',
            contactInfo: {}
        };
    }

    generateDynamicSections() {
        // Generate initial content for dynamic sections
        this.generateServicesCards();
        this.generateGalleryItems();
        this.generateTestimonialCards();
        this.generateBlogCards();
    }

    generateServicesCards() {
        const container = document.getElementById('dynamicServicesContainer');
        if (!container) return;

        const services = this.getAgricultureServices();
        const cardsToGenerate = Math.min(services.length, 8); // Default 8 services

        container.innerHTML = '';
        for (let i = 0; i < cardsToGenerate; i++) {
            const service = services[i];
            container.appendChild(this.createServiceCard(service, i));
        }

        this.updateCardControls('services', cardsToGenerate);
    }

    generateGalleryItems() {
        const container = document.getElementById('dynamicGalleryContainer');
        if (!container) return;

        const galleryItems = this.getDefaultGalleryItems();
        const itemsToGenerate = Math.min(galleryItems.length, 6); // Default 6 images

        container.innerHTML = '';
        for (let i = 0; i < itemsToGenerate; i++) {
            container.appendChild(this.createGalleryItem(galleryItems[i], i));
        }

        this.updateCardControls('gallery', itemsToGenerate);
    }

    generateTestimonialCards() {
        const container = document.getElementById('dynamicTestimonialsContainer');
        if (!container) return;

        const testimonials = this.getDefaultTestimonials();
        const cardsToGenerate = Math.min(testimonials.length, 4); // Default 4 testimonials

        container.innerHTML = '';
        for (let i = 0; i < cardsToGenerate; i++) {
            container.appendChild(this.createTestimonialCard(testimonials[i], i));
        }

        this.updateCardControls('testimonials', cardsToGenerate);
    }

    generateBlogCards() {
        const container = document.getElementById('dynamicBlogContainer');
        if (!container) return;

        const blogPosts = this.getAgricultureBlogPosts();
        const cardsToGenerate = Math.min(blogPosts.length, 3); // Default 3 blog posts

        container.innerHTML = '';
        for (let i = 0; i < cardsToGenerate; i++) {
            container.appendChild(this.createBlogCard(blogPosts[i], i));
        }

        this.updateCardControls('blog', cardsToGenerate);
    }

    createServiceCard(service, index) {
        const card = document.createElement('div');
        card.className = 'col-lg-3 col-md-6 mb-4';
        card.innerHTML = `
            <div class="service-card">
                <div class="service-icon">
                    <i class="${service.icon}"></i>
                </div>
                <h5>${service.title}</h5>
                <p>${service.description}</p>
                <div class="card-controls mt-3" style="opacity: 0; transition: opacity 0.3s;">
                    <button class="ai-edit-btn small" onclick="editServiceCard(${index})">
                        <i class="fas fa-magic"></i> Edit AI
                    </button>
                    <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeCard('services', ${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;

        // Show controls on hover
        card.addEventListener('mouseenter', () => {
            const controls = card.querySelector('.card-controls');
            if (controls) controls.style.opacity = '1';
        });

        card.addEventListener('mouseleave', () => {
            const controls = card.querySelector('.card-controls');
            if (controls) controls.style.opacity = '0';
        });

        return card;
    }

    createGalleryItem(item, index) {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item position-relative';
        galleryItem.innerHTML = `
            <img src="${item.image}" alt="${item.caption}" class="img-fluid">
            <div class="gallery-overlay">
                <div class="card-controls">
                    <button class="ai-edit-btn small" onclick="editGalleryItem(${index})">
                        <i class="fas fa-magic"></i> Edit AI
                    </button>
                    <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeCard('gallery', ${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
        return galleryItem;
    }

    createTestimonialCard(testimonial, index) {
        const card = document.createElement('div');
        card.className = 'col-lg-6 col-md-6 mb-4';
        card.innerHTML = `
            <div class="testimonial-card">
                <img src="${testimonial.avatar}" alt="${testimonial.name}" class="testimonial-avatar">
                <div class="testimonial-text">"${testimonial.text}"</div>
                <div class="testimonial-name">${testimonial.name}</div>
                <div class="testimonial-title text-muted">${testimonial.title}</div>
                <div class="card-controls mt-3" style="opacity: 0; transition: opacity 0.3s;">
                    <button class="ai-edit-btn small" onclick="editTestimonialCard(${index})">
                        <i class="fas fa-magic"></i> Edit AI
                    </button>
                    <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeCard('testimonials', ${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;

        // Show controls on hover
        card.addEventListener('mouseenter', () => {
            const controls = card.querySelector('.card-controls');
            if (controls) controls.style.opacity = '1';
        });

        card.addEventListener('mouseleave', () => {
            const controls = card.querySelector('.card-controls');
            if (controls) controls.style.opacity = '0';
        });

        return card;
    }

    createBlogCard(post, index) {
        const card = document.createElement('div');
        card.className = 'col-lg-4 col-md-6 mb-4';
        card.innerHTML = `
            <div class="blog-card">
                <img src="${post.image}" alt="${post.title}" class="img-fluid">
                <div class="blog-card-body">
                    <div class="blog-date">${post.date}</div>
                    <h5 class="blog-title">${post.title}</h5>
                    <p class="text-muted">${post.excerpt}</p>
                    <div class="card-controls mt-3" style="opacity: 0; transition: opacity 0.3s;">
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

        // Show controls on hover
        card.addEventListener('mouseenter', () => {
            const controls = card.querySelector('.card-controls');
            if (controls) controls.style.opacity = '1';
        });

        card.addEventListener('mouseleave', () => {
            const controls = card.querySelector('.card-controls');
            if (controls) controls.style.opacity = '0';
        });

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
                newCard = this.createServiceCard(this.getAgricultureService(currentCount), currentCount);
                break;
            case 'gallery':
                newCard = this.createGalleryItem(this.getDefaultGalleryItem(currentCount), currentCount);
                break;
            case 'testimonials':
                newCard = this.createTestimonialCard(this.getDefaultTestimonial(currentCount), currentCount);
                break;
            case 'blog':
                newCard = this.createBlogCard(this.getAgricultureBlogPost(currentCount), currentCount);
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

    setupEventListeners() {
        // Newsletter form handling
        const newsletterForm = document.querySelector('.newsletter-form');
        if (newsletterForm) {
            newsletterForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleNewsletterSignup(e);
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

    handleNewsletterSignup(e) {
        const formData = new FormData(e.target);
        const email = e.target.querySelector('.newsletter-input').value;
        console.log('Newsletter signup:', email);
        alert('Thank you for subscribing to our newsletter!');
        e.target.reset();
    }

    // Agriculture-specific content generators
    getAgricultureServices() {
        return [
            {
                icon: 'fas fa-seedling',
                title: 'Organic Farming',
                description: 'Sustainable organic farming practices using natural methods and eco-friendly techniques.'
            },
            {
                icon: 'fas fa-carrot',
                title: 'Fresh Vegetables',
                description: 'Daily harvest of fresh, crisp vegetables grown without harmful pesticides or chemicals.'
            },
            {
                icon: 'fas fa-apple-alt',
                title: 'Seasonal Fruits',
                description: 'Tree-ripened seasonal fruits picked at peak freshness for maximum flavor and nutrition.'
            },
            {
                icon: 'fas fa-tractor',
                title: 'Farm Equipment',
                description: 'Modern farming equipment and machinery for efficient and sustainable agriculture.'
            },
            {
                icon: 'fas fa-leaf',
                title: 'Sustainable Practices',
                description: 'Environmentally conscious farming methods that preserve soil health and biodiversity.'
            },
            {
                icon: 'fas fa-truck',
                title: 'Farm Delivery',
                description: 'Fresh produce delivered directly from our farm to your doorstep with care.'
            },
            {
                icon: 'fas fa-users',
                title: 'Farm Tours',
                description: 'Educational farm visits to learn about organic farming and sustainable agriculture.'
            },
            {
                icon: 'fas fa-handshake',
                title: 'Consultation',
                description: 'Expert agricultural consultation for sustainable farming and organic certification.'
            }
        ];
    }

    getAgricultureService(index) {
        const services = this.getAgricultureServices();
        return services[index % services.length];
    }

    getDefaultGalleryItems() {
        return [
            {
                image: 'https://images.unsplash.com/photo-1595501605207-72858ba0dd28?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                caption: 'Experienced farmer with vegetables'
            },
            {
                image: 'https://images.unsplash.com/photo-1560493676-04071c5f467b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                caption: 'Fresh vegetables in basket'
            },
            {
                image: 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                caption: 'Organic farming in action'
            },
            {
                image: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                caption: 'Farm field at sunrise'
            },
            {
                image: 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                caption: 'Fresh harvest season'
            },
            {
                image: 'https://images.unsplash.com/photo-1592477725143-2e57dc728f3a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                caption: 'Sustainable farming practices'
            }
        ];
    }

    getDefaultGalleryItem(index) {
        const items = this.getDefaultGalleryItems();
        return items[index % items.length];
    }

    getDefaultTestimonials() {
        return [
            {
                name: 'Sarah Johnson',
                title: 'Local Restaurant Owner',
                text: 'The quality of vegetables from this farm is exceptional. Fresh, organic, and always delivered on time. Our customers love the taste!',
                avatar: 'https://images.unsplash.com/photo-1494790108755-2616b332261c?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            {
                name: 'Mike Chen',
                title: 'Health Food Store Manager',
                text: 'We have been working with this farm for over 3 years. Their organic certification and sustainable practices align perfectly with our values.',
                avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            {
                name: 'Emily Rodriguez',
                title: 'Nutritionist',
                text: 'I recommend this farm to all my clients. The nutritional value and freshness of their produce is unmatched in the region.',
                avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            {
                name: 'David Thompson',
                title: 'Family Customer',
                text: 'Our family has been buying from this farm for years. The kids love the taste of real, fresh vegetables and we love supporting local agriculture.',
                avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            }
        ];
    }

    getDefaultTestimonial(index) {
        const testimonials = this.getDefaultTestimonials();
        return testimonials[index % testimonials.length];
    }

    getAgricultureBlogPosts() {
        return [
            {
                title: 'Benefits of Organic Farming for Soil Health',
                excerpt: 'Discover how organic farming practices improve soil quality and support long-term agricultural sustainability.',
                image: 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                date: 'October 5, 2025'
            },
            {
                title: 'Seasonal Vegetable Guide: What to Plant When',
                excerpt: 'A comprehensive guide to seasonal vegetable planting for optimal harvest and flavor throughout the year.',
                image: 'https://images.unsplash.com/photo-1560493676-04071c5f467b?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                date: 'September 28, 2025'
            },
            {
                title: 'Sustainable Agriculture: Our Commitment to the Future',
                excerpt: 'Learn about our sustainable farming practices and commitment to environmental conservation for future generations.',
                image: 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                date: 'September 20, 2025'
            }
        ];
    }

    getAgricultureBlogPost(index) {
        const posts = this.getAgricultureBlogPosts();
        return posts[index % posts.length];
    }

    // AI Content Generation Methods
    async generateAIContent(section, context = {}) {
        const prompt = this.buildAgriculturePrompt(section, context);
        
        try {
            const response = await fetch(this.magicAIEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    prompt: prompt,
                    businessType: 'agriculture',
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

    buildAgriculturePrompt(section, context) {
        const businessName = this.businessData.businessName || 'Agriculture Co.';
        
        const prompts = {
            hero: `Create compelling hero section content for ${businessName}, an organic agriculture business. Focus on fresh, healthy produce and sustainable farming. Include headline, subtitle, and call-to-action.`,
            about: `Write an engaging about section for ${businessName}, highlighting farming experience, organic certification, and commitment to quality produce.`,
            services: `Generate agricultural service descriptions for ${businessName}. Include organic farming, fresh produce delivery, farm tours, and consultation services.`,
            testimonials: `Create customer testimonials for ${businessName} from restaurant owners, health food stores, and families who buy organic produce.`,
            blog: `Create agriculture blog post titles and excerpts about organic farming, seasonal vegetables, and sustainable agriculture practices.`,
            newsletter: `Write compelling newsletter signup content for an organic farm, focusing on seasonal updates and farming tips.`
        };

        return prompts[section] || `Generate professional agriculture content for ${section} section.`;
    }

    getFallbackContent(section) {
        // Return default agriculture content if AI generation fails
        const fallbacks = {
            hero: { headline: 'Fresh Organic Produce Daily', subtitle: 'Sustainable farming for healthy living' },
            about: { text: 'Over 50 years of experience in sustainable organic farming and fresh produce delivery.' },
            services: this.getAgricultureServices(),
            testimonials: this.getDefaultTestimonials(),
            blog: this.getAgricultureBlogPosts()
        };
        return fallbacks[section] || {};
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
    if (window.jcwTemplate02) {
        window.jcwTemplate02.generateAIContent(section).then(content => {
            console.log('Generated agriculture content:', content);
        });
    }
};

window.addCard = function(section) {
    if (window.jcwTemplate02) {
        window.jcwTemplate02.addCard(section);
    }
};

window.removeCard = function(section, index) {
    if (window.jcwTemplate02) {
        window.jcwTemplate02.removeCard(section, index);
    }
};

window.editServiceCard = function(index) {
    console.log(`Edit agriculture service card ${index} with AI`);
    if (window.jcwTemplate02) {
        window.jcwTemplate02.generateAIContent('services', { index, count: 1 });
    }
};

window.editGalleryItem = function(index) {
    console.log(`Edit gallery item ${index} with AI`);
    if (window.jcwTemplate02) {
        window.jcwTemplate02.generateAIContent('gallery', { index, count: 1 });
    }
};

window.editTestimonialCard = function(index) {
    console.log(`Edit testimonial card ${index} with AI`);
    if (window.jcwTemplate02) {
        window.jcwTemplate02.generateAIContent('testimonials', { index, count: 1 });
    }
};

window.editBlogCard = function(index) {
    console.log(`Edit blog card ${index} with AI`);
    if (window.jcwTemplate02) {
        window.jcwTemplate02.generateAIContent('blog', { index, count: 1 });
    }
};

// Initialize Template when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.jcwTemplate02 = new JCWTemplate02();
    console.log('JCW-TPL02 Agriculture Template System Ready');
});