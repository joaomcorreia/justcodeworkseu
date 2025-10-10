"""
Website Builder AI Assistant - Clippy 2.0 for JustCodeWorks
Interactive website building through conversational AI
"""
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from django.conf import settings
from django.contrib.auth.models import User
from ai_assistant.magic_ai import MagicAI
from .models import (
    WebsiteProject, BusinessService, WebsiteTemplate, 
    WebsiteBuilderConversation, IndustryTemplate
)


class ClippyWebsiteBuilder(MagicAI):
    """
    Clippy 2.0 - AI Website Building Assistant
    Inherits from MagicAI and adds specialized website building capabilities
    """
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Enable AI-powered responses (set to True to use MagicAI)
        self.use_ai_responses = True
        
        # Conversation flow configuration
        self.conversation_steps = {
            'welcome': self._step_welcome,
            'business_name': self._step_business_name,
            'industry_selection': self._step_industry_selection,
            'services_selection': self._step_services_selection,
            'business_details': self._step_business_details,
            'template_selection': self._step_template_selection,
            'content_generation': self._step_content_generation,
            'content_review': self._step_content_review,
            'final_review': self._step_final_review,
            'completion': self._step_completion,
        }
        
        # Comprehensive industry-specific service suggestions
        self.industry_services = {
            # AUTOMOTIVE & TRANSPORTATION
            'automotive': [
                'Tire Installation & Repair', 'Tire Sales (New & Used)', 'Wheel Alignment', 
                'Wheel Balancing', 'Brake Service', 'Oil Change', 'Engine Diagnostics',
                'Transmission Repair', 'Air Conditioning Repair', 'Battery Service',
                'General Auto Repair', 'Vehicle Inspection', 'Suspension Repair'
            ],
            'tires': [
                'New Tire Sales', 'Used Tire Sales', 'Tire Installation', 'Tire Repair & Patching',
                'Wheel Alignment', 'Wheel Balancing', 'Tire Rotation', 'Puncture Repair',
                'Run-Flat Tire Service', 'Commercial Tire Service', 'Emergency Roadside Tire Service'
            ],
            'transportation': [
                'Taxi Service', 'Airport Transfer', 'Corporate Transportation', 'Event Transportation',
                'Long Distance Travel', 'Medical Transport', 'School Transport', 'Delivery Service'
            ],
            
            # CONSTRUCTION & TRADES
            'construction': [
                'Home Renovation', 'Kitchen Remodeling', 'Bathroom Renovation',
                'Flooring Installation', 'Painting Services', 'Roofing',
                'Plumbing', 'Electrical Work', 'General Contracting', 'Drywall Installation'
            ],
            'plumbing': [
                'Pipe Repair', 'Drain Cleaning', 'Water Heater Installation', 'Leak Detection',
                'Bathroom Plumbing', 'Kitchen Plumbing', 'Emergency Plumbing', 'Sewer Line Repair'
            ],
            'electrical': [
                'Electrical Installation', 'Wiring Repair', 'Panel Upgrades', 'Lighting Installation',
                'Outlet Installation', 'Circuit Breaker Service', 'Emergency Electrical Service'
            ],
            'painting': [
                'Interior Painting', 'Exterior Painting', 'Commercial Painting', 'Residential Painting',
                'Pressure Washing', 'Wallpaper Installation', 'Color Consultation', 'Touch-Up Services'
            ],
            'roofing': [
                'Roof Installation', 'Roof Repair', 'Gutter Installation', 'Roof Inspection',
                'Emergency Roof Service', 'Roof Maintenance', 'Skylight Installation'
            ],
            
            # HEALTHCARE & WELLNESS
            'healthcare': [
                'General Consultation', 'Preventive Care', 'Health Screenings',
                'Wellness Programs', 'Nutrition Counseling', 'Physical Therapy',
                'Mental Health Support', 'Chronic Disease Management', 'Emergency Care'
            ],
            'dental': [
                'General Dentistry', 'Teeth Cleaning', 'Dental Checkups', 'Fillings',
                'Root Canal', 'Teeth Whitening', 'Orthodontics', 'Dental Implants', 'Emergency Dental'
            ],
            'physiotherapy': [
                'Sports Injury Treatment', 'Back Pain Treatment', 'Joint Rehabilitation',
                'Post-Surgery Recovery', 'Mobility Training', 'Pain Management', 'Exercise Therapy'
            ],
            'veterinary': [
                'Pet Checkups', 'Vaccinations', 'Pet Surgery', 'Emergency Pet Care',
                'Dental Care for Pets', 'Grooming', 'Pet Boarding', 'Nutritional Counseling'
            ],
            
            # FOOD & HOSPITALITY
            'restaurant': [
                'Dine-in Service', 'Takeout & Delivery', 'Catering',
                'Private Events', 'Corporate Catering', 'Special Dietary Options',
                'Wine Selection', 'Live Entertainment', 'Outdoor Seating'
            ],
            'cafe': [
                'Coffee & Espresso', 'Fresh Pastries', 'Light Meals', 'Wifi & Study Space',
                'Takeout Coffee', 'Catering', 'Event Hosting', 'Specialty Drinks'
            ],
            'catering': [
                'Wedding Catering', 'Corporate Events', 'Private Parties', 'Buffet Service',
                'Formal Dinner Service', 'Cocktail Catering', 'Holiday Catering', 'Delivery Service'
            ],
            'bakery': [
                'Fresh Bread', 'Custom Cakes', 'Wedding Cakes', 'Pastries & Desserts',
                'Cupcakes', 'Cookies', 'Special Occasion Cakes', 'Gluten-Free Options'
            ],
            
            # TECHNOLOGY & IT
            'technology': [
                'Web Development', 'Mobile App Development', 'Software Consulting',
                'IT Support', 'Cloud Services', 'Cybersecurity',
                'Database Management', 'UI/UX Design', 'Digital Marketing'
            ],
            'computer_repair': [
                'Laptop Repair', 'Desktop Repair', 'Virus Removal', 'Data Recovery',
                'Hardware Upgrades', 'Software Installation', 'Network Setup', 'Screen Replacement'
            ],
            'web_design': [
                'Website Design', 'E-commerce Development', 'SEO Services', 'Website Maintenance',
                'Domain & Hosting', 'Logo Design', 'Social Media Setup', 'Online Marketing'
            ],
            
            # BEAUTY & PERSONAL CARE
            'beauty_salon': [
                'Haircuts & Styling', 'Hair Coloring', 'Manicure & Pedicure', 'Facial Treatments',
                'Eyebrow Shaping', 'Wedding Hair & Makeup', 'Hair Extensions', 'Scalp Treatment'
            ],
            'barbershop': [
                'Mens Haircuts', 'Beard Trimming', 'Shaving Services', 'Hair Styling',
                'Mustache Grooming', 'Hot Towel Treatment', 'Hair Washing', 'Scalp Massage'
            ],
            'spa': [
                'Massage Therapy', 'Facial Treatments', 'Body Treatments', 'Relaxation Therapy',
                'Aromatherapy', 'Hot Stone Massage', 'Deep Tissue Massage', 'Couples Massage'
            ],
            
            # RETAIL & COMMERCE
            'retail': [
                'Product Sales', 'Customer Service', 'Personal Shopping', 'Gift Wrapping',
                'Returns & Exchanges', 'Product Consultation', 'Delivery Service', 'Custom Orders'
            ],
            'clothing': [
                'Mens Clothing', 'Womens Clothing', 'Childrens Clothing', 'Accessories',
                'Personal Styling', 'Alterations', 'Custom Tailoring', 'Special Occasion Wear'
            ],
            'jewelry': [
                'Custom Jewelry Design', 'Jewelry Repair', 'Watch Repair', 'Appraisals',
                'Engagement Rings', 'Wedding Bands', 'Gemstone Setting', 'Engraving'
            ],
            
            # PROFESSIONAL SERVICES
            'legal': [
                'Legal Consultation', 'Contract Review', 'Business Law', 'Family Law',
                'Real Estate Law', 'Wills & Estates', 'Immigration Law', 'Personal Injury'
            ],
            'accounting': [
                'Tax Preparation', 'Bookkeeping', 'Business Accounting', 'Payroll Services',
                'Financial Planning', 'Audit Services', 'Tax Planning', 'Business Consultation'
            ],
            'real_estate': [
                'Home Sales', 'Property Management', 'Real Estate Investment', 'Rental Properties',
                'Commercial Real Estate', 'Property Valuation', 'Market Analysis', 'Buyer Representation'
            ],
            'insurance': [
                'Auto Insurance', 'Home Insurance', 'Life Insurance', 'Business Insurance',
                'Health Insurance', 'Travel Insurance', 'Claims Processing', 'Risk Assessment'
            ],
            
            # FITNESS & SPORTS
            'fitness': [
                'Personal Training', 'Group Fitness Classes', 'Gym Membership', 'Nutrition Coaching',
                'Weight Loss Programs', 'Strength Training', 'Cardio Training', 'Fitness Assessment'
            ],
            'sports': [
                'Sports Training', 'Team Coaching', 'Individual Lessons', 'Sports Equipment',
                'Athletic Performance', 'Sports Medicine', 'Youth Sports Programs', 'Adult Leagues'
            ],
            
            # EDUCATION & CHILDCARE
            'education': [
                'Tutoring Services', 'Test Preparation', 'Language Learning', 'Academic Support',
                'Study Skills Training', 'Homework Help', 'Online Learning', 'Educational Consulting'
            ],
            'childcare': [
                'Daycare Services', 'After School Care', 'Summer Programs', 'Educational Activities',
                'Meal Services', 'Transportation', 'Infant Care', 'Preschool Programs'
            ],
            
            # HOME & GARDEN
            'landscaping': [
                'Lawn Care', 'Garden Design', 'Tree Service', 'Irrigation Systems',
                'Hardscaping', 'Seasonal Cleanup', 'Fertilization', 'Pest Control'
            ],
            'cleaning': [
                'House Cleaning', 'Office Cleaning', 'Deep Cleaning', 'Move-in/Move-out Cleaning',
                'Carpet Cleaning', 'Window Cleaning', 'Post-Construction Cleaning', 'Regular Maintenance'
            ],
            'pest_control': [
                'Insect Control', 'Rodent Control', 'Termite Treatment', 'Bed Bug Treatment',
                'Ant Control', 'Spider Control', 'Preventive Treatment', 'Emergency Service'
            ],
            
            # ENTERTAINMENT & EVENTS
            'photography': [
                'Wedding Photography', 'Portrait Photography', 'Event Photography', 'Commercial Photography',
                'Family Photos', 'Product Photography', 'Real Estate Photography', 'Photo Editing'
            ],
            'music': [
                'Music Lessons', 'Performance Services', 'Recording Services', 'Music Production',
                'DJ Services', 'Live Music', 'Sound Equipment Rental', 'Music Therapy'
            ],
            'event_planning': [
                'Wedding Planning', 'Corporate Events', 'Birthday Parties', 'Anniversary Celebrations',
                'Venue Coordination', 'Vendor Management', 'Event Design', 'Day-of Coordination'
            ],
            
            # MANUFACTURING & INDUSTRIAL
            'manufacturing': [
                'Custom Manufacturing', 'Product Development', 'Quality Control', 'Assembly Services',
                'Packaging Services', 'Supply Chain Management', 'Industrial Design', 'Prototype Development'
            ],
            'printing': [
                'Digital Printing', 'Offset Printing', 'Large Format Printing', 'Business Cards',
                'Brochures', 'Banners & Signs', 'Custom Printing', 'Graphic Design'
            ],
            
            # GENERAL FALLBACK
            'professional_services': [
                'Consultation', 'Project Management', 'Strategic Planning',
                'Training & Development', 'Quality Assurance', 'Risk Assessment',
                'Compliance Management', 'Business Analysis', 'Process Optimization'
            ]
        }
    
    def start_conversation(self, user: User, project_name: str = None) -> Tuple[WebsiteProject, str]:
        """
        Initialize a new website building conversation
        """
        try:
            # Create new website project
            project = WebsiteProject.objects.create(
                user=user,
                project_name=project_name or f"Website Project {user.username}",
                business_name="",  # Will be collected in conversation
            )
            
            # Create conversation tracker
            conversation = WebsiteBuilderConversation.objects.create(
                project=project,
                current_step='welcome'
            )
            
            # Generate welcome message
            welcome_message = self._step_welcome(conversation, user_input=None)
            
            return project, welcome_message
            
        except Exception as e:
            self.logger.error(f"Error starting conversation: {e}")
            return None, "Sorry, I encountered an error starting our conversation. Please try again."
    
    def process_conversation(self, project_id: str, user_input: str, user: User) -> Dict[str, Any]:
        """
        Process user input and generate AI response based on current conversation step
        """
        try:
            project = WebsiteProject.objects.get(project_id=project_id, user=user)
            conversation = project.ai_conversation
            
            # Get current step handler
            step_handler = self.conversation_steps.get(conversation.current_step)
            if not step_handler:
                return self._error_response(f"Invalid conversation step: {conversation.current_step}")
            
            # Process the current step
            response = step_handler(conversation, user_input)
            
            # Update conversation data
            conversation.total_messages += 1
            conversation.save()
            
            # Prepare template data for live preview
            template_data = {}
            if project.template:
                template_data = {
                    'primaryColor': '#007bff',  # Default blue
                    'secondaryColor': '#6c757d',
                    'fontFamily': 'Arial, sans-serif',
                    'textColor': '#333',
                    'cardBackground': '#f8f9fa'
                }
                
                # If template has specific styles, use those
                if project.template.color_schemes:
                    try:
                        schemes = json.loads(project.template.color_schemes)
                        if schemes and len(schemes) > 0:
                            default_scheme = schemes[0]
                            template_data.update({
                                'primaryColor': default_scheme.get('primary', '#007bff'),
                                'secondaryColor': default_scheme.get('secondary', '#6c757d'),
                                'textColor': default_scheme.get('text', '#333'),
                            })
                    except:
                        pass
            
            # Prepare services data for preview
            services_data = []
            for service in project.services.all():
                services_data.append({
                    'name': service.name,
                    'description': service.description or None
                })
            
            return {
                'success': True,
                'message': response,
                'current_step': conversation.current_step,
                'progress': project.get_completion_percentage(),
                'project_data': {
                    'name': project.business_name,
                    'business_name': project.business_name,
                    'industry': project.industry,
                    'about': project.business_description or None,
                    'services': services_data,
                    'services_count': project.services.count(),
                    'status': project.status,
                    'tagline': f"Professional {project.industry.replace('_', ' ').title()} Services" if project.industry else "Professional Services You Can Trust"
                },
                'template_data': template_data
            }
            
        except WebsiteProject.DoesNotExist:
            return self._error_response("Project not found")
        except Exception as e:
            self.logger.error(f"Error processing conversation: {e}")
            return self._error_response("An error occurred processing your request")
    
    def _generate_ai_business_recognition(self, business_name: str, detected_industries: List[str]) -> Dict[str, Any]:
        """
        Use MagicAI to generate personalized business recognition and service suggestions
        """
        if not self.use_ai_responses or not detected_industries:
            return None
            
        try:
            # Prepare industry context
            if len(detected_industries) > 1:
                industry_context = f"multiple industries: {', '.join([ind.replace('_', ' ').title() for ind in detected_industries])}"
            else:
                industry_context = f"the {detected_industries[0].replace('_', ' ').title()} industry"
            
            prompt = f"""
            A business owner just told me their business name is "{business_name}" and I've detected they operate in {industry_context}.
            
            As Clippy 2.0, a friendly AI website builder assistant, I need to:
            1. Give an enthusiastic, personalized recognition of their business
            2. Suggest 8-10 relevant services they might offer
            3. Keep the tone conversational and encouraging
            
            Make the recognition message feel personal and specific to their business name and industry.
            For multi-industry businesses, acknowledge how they combine different services.
            
            Return as JSON:
            {{
                "recognition_message": "Enthusiastic recognition message mentioning the business name and industry",
                "suggested_services": ["Service 1", "Service 2", ..., "Service 8-10"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Clippy 2.0, an enthusiastic AI assistant that helps build websites. You're knowledgeable about different industries and always encouraging. Keep responses concise but warm."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            content_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            import json
            return json.loads(content_text)
            
        except Exception as e:
            self.logger.error(f"Error generating AI business recognition: {e}")
            return None

    def _step_welcome(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Welcome step - introduce Clippy 2.0 and ask for business name
        """
        user_name = conversation.project.user.first_name or conversation.project.user.username
        
        welcome_message = f"""Hello, I'm Clippy 2.0, I am here to help you build your website. What is the name of your business?"""
        
        # Advance to next step
        conversation.advance_step()
        
        return welcome_message.strip()
    
    def _step_business_name(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Collect business name and automatically detect industry when possible
        """
        if not user_input or len(user_input.strip()) < 2:
            return "Please enter your business name (at least 2 characters). What would you like to call your business?"

        # Save business name
        business_name = user_input.strip()
        conversation.project.business_name = business_name
        conversation.project.save()

        # Store in conversation data
        conversation.conversation_data['business_name'] = business_name
        conversation.save()

        # Try to automatically detect multiple industries from business name
        detected_industries = self._detect_multiple_industries(business_name.lower())
        
        # If we detected specific industries from the business name, auto-advance
        if detected_industries and detected_industries[0] != 'unknown':
            # Handle multiple industries - combine services and use primary industry
            primary_industry = detected_industries[0]
            industry_list = ', '.join([ind.replace('_', ' ').title() for ind in detected_industries])
            
            # Save the primary industry (first detected)
            conversation.project.industry = primary_industry
            conversation.project.save()
            conversation.conversation_data['industry'] = primary_industry
            conversation.conversation_data['detected_industries'] = detected_industries
            conversation.conversation_data['industry_input'] = business_name
            conversation.save()
            
            # Combine services from all detected industries
            suggested_services = []
            for industry in detected_industries:
                services = self.industry_services.get(industry, [])
                suggested_services.extend(services)
            
            # Remove duplicates and limit to reasonable number
            suggested_services = list(dict.fromkeys(suggested_services))[:10]
            
            if not suggested_services:
                suggested_services = [
                    'Main Service', 'Consultation', 'Customer Support', 
                    'Quality Assurance', 'Custom Solutions'
                ]
            
            # Try AI-powered recognition first, fallback to predefined messages
            ai_response = self._generate_ai_business_recognition(business_name, detected_industries)
            
            if ai_response and 'recognition_message' in ai_response:
                # Use AI-generated recognition and services
                industry_recognition = ai_response['recognition_message']
                if 'suggested_services' in ai_response and ai_response['suggested_services']:
                    suggested_services = ai_response['suggested_services'][:10]  # Limit to 10
            else:
                # Fallback to predefined messages
                industry_messages = {
                    'tires': f"Excellent! I can see that **{business_name}** is in the **tire business** 🚗. Perfect!",
                    'automotive': f"Great! **{business_name}** is clearly an **automotive business** 🔧. I've got you covered!",
                    'plumbing': f"Perfect! **{business_name}** is a **plumbing business** 🔧. I know exactly what services to suggest!",
                    'dental': f"Wonderful! **{business_name}** is a **dental practice** 🦷. I'll help you create a professional dental website!",
                    'beauty_salon': f"Fantastic! **{business_name}** is a **beauty salon** ✨. Let's showcase your beauty services!",
                    'restaurant': f"Delicious! **{business_name}** is a **restaurant** 🍽️. Let's create a mouth-watering website!",
                    'construction': f"Excellent! **{business_name}** is a **construction business** 🏗️. I'll help you build a strong online presence!"
                }
                
                # Get the smart message or use default
                if len(detected_industries) > 1:
                    # Multi-industry business
                    industry_names = [industry.replace('_', ' ').title() for industry in detected_industries]
                    industry_recognition = f"Excellent! **{business_name}** spans multiple industries: **{' & '.join(industry_names)}**. I'll help you create a comprehensive website!"
                else:
                    # Single industry business
                    industry_recognition = industry_messages.get(
                        primary_industry, 
                        f"Perfect! I can see that **{business_name}** is in the **{primary_industry.replace('_', ' ').title()}** industry."
                    )
            
            message = f"""
            Great! **{business_name}** is a wonderful name! 🎉
            
            {industry_recognition}
            
            Now, let's talk about your services. I've prepared some common services for your industry type. 
            **Please select which services you offer:**
            
            <div class="services-selection mt-3 mb-3">
            """
            
            # Add service options with real checkboxes
            for i, service in enumerate(suggested_services[:8], 1):  # Limit to 8 services for readability
                service_id = f"service_{i}"
                message += f'                <div class="form-check mb-2">\n'
                message += f'                    <input class="form-check-input" type="checkbox" id="{service_id}" name="services" value="{service}">\n'
                message += f'                    <label class="form-check-label" for="{service_id}"><strong>{service}</strong></label>\n'
                message += f'                </div>\n'
            
            if len(suggested_services) > 8:
                message += f'<p class="text-muted mt-2"><em>...and we can add more services later!</em></p>\n'
            
            message += f"""
            </div>
            
            <div class="mt-4 mb-3">
                <button type="button" class="btn btn-primary" onclick="submitSelectedServices()">
                    ✅ Submit Selected Services
                </button>
            </div>
            
            **Or you can also:**
            - Simply type your services in your own words
            - Describe what your business does
            - Don't worry about getting it perfect - I'll help you refine everything!
            
            What services does **{business_name}** provide? 🛠️
            """
            
            # Skip industry_selection step and go directly to services_selection
            conversation.advance_step()  # This will go to industry_selection
            conversation.advance_step()  # This will go to services_selection
            
            return message.strip()
        
        # If no industry detected, ask for manual selection
        message = f"""
        Great! **{business_name}** is a wonderful name! 🎉
        
        Now, to help me create the perfect website for you, what industry or profession best describes your business?
        
        **Please choose from these popular categories:**
        
        🏗️ **Construction & Building** - Contractors, renovations, building services
        💻 **Technology & IT** - Software, web services, tech consulting  
        🍽️ **Restaurant & Food** - Restaurants, catering, food services
        🏥 **Healthcare & Wellness** - Medical, dental, fitness, wellness
        🚗 **Automotive** - Car repair, maintenance, auto services
        💼 **Professional Services** - Consulting, legal, accounting, business services
        🎨 **Creative & Design** - Photography, graphic design, arts
        🛍️ **Retail & E-commerce** - Stores, online shopping, products
        
        **Or simply tell me what type of business you have!**
        """

        # Advance to next step
        conversation.advance_step()

        return message.strip()

    def _step_industry_selection(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Process industry selection and suggest relevant services
        """
        if not user_input:
            return "Please tell me what type of business you have so I can help you better!"
        
        # Analyze industry from user input
        industry = self._detect_industry(user_input.lower())
        
        # Save industry
        conversation.project.industry = industry
        conversation.project.save()
        
        # Store in conversation data
        conversation.conversation_data['industry'] = industry
        conversation.conversation_data['industry_input'] = user_input
        conversation.save()
        
        # Get suggested services for this industry
        suggested_services = self.industry_services.get(industry, [
            'Main Service', 'Consultation', 'Customer Support', 
            'Quality Assurance', 'Custom Solutions'
        ])
        
        # Create smart response based on detection
        business_name = conversation.project.business_name
        
        # Smart industry recognition messages
        industry_messages = {
            'tires': f"Excellent! I can see that **{business_name}** is in the **tire business** 🚗. Perfect!",
            'automotive': f"Great! **{business_name}** is clearly an **automotive business** 🔧. I've got you covered!",
            'plumbing': f"Perfect! **{business_name}** is a **plumbing business** 🔧. I know exactly what services to suggest!",
            'dental': f"Wonderful! **{business_name}** is a **dental practice** 🦷. I'll help you create a professional dental website!",
            'beauty_salon': f"Fantastic! **{business_name}** is a **beauty salon** ✨. Let's showcase your beauty services!",
            'restaurant': f"Delicious! **{business_name}** is a **restaurant** 🍽️. Let's create a mouth-watering website!",
            'construction': f"Excellent! **{business_name}** is a **construction business** 🏗️. I'll help you build a strong online presence!"
        }
        
        # Get the smart message or use default
        industry_recognition = industry_messages.get(
            industry, 
            f"Perfect! I understand that **{business_name}** is in the **{industry.replace('_', ' ').title()}** industry."
        )
        
        message = f"""
        {industry_recognition}
        
        Now, let's talk about your services. I've prepared some common services for your industry type. 
        **Please select which services you offer:**
        
        <div class="services-selection mt-3">
        """
        
        # Add service options with real checkboxes
        for i, service in enumerate(suggested_services[:8], 1):  # Limit to 8 services for readability
            service_id = f"service_{i}"
            message += f'<div class="form-check mb-2">\n'
            message += f'<input class="form-check-input" type="checkbox" id="{service_id}" name="services" value="{service}">\n'
            message += f'<label class="form-check-label" for="{service_id}"><strong>{service}</strong></label>\n'
            message += f'</div>\n'
        
        if len(suggested_services) > 8:
            message += f'<p class="text-muted mt-2"><em>...and we can add more services later!</em></p>\n'
        
        message += f"""
        </div>
        
        <div class="mt-3">
        <button type="button" class="btn btn-primary btn-sm" onclick="submitSelectedServices()">
            ✅ Submit Selected Services
        </button>
        </div>
        
        **Or you can also:**
        - Simply type your services in your own words
        - Describe what your business does  
        - Don't worry about getting it perfect - I'll help you refine everything!
        
        What services does **{business_name}** provide? 🛠️
        """
        
        # Advance to next step
        conversation.advance_step()
        
        return message.strip()
    
    def _step_services_selection(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Process selected services and create service objects
        """
        if not user_input or len(user_input.strip()) < 3:
            return "Please tell me about the services you offer. What does your business do for customers?"
        
        # Parse services from user input
        services = self._parse_services(user_input, conversation.project.industry)
        
        # Create BusinessService objects
        for i, service in enumerate(services):
            BusinessService.objects.create(
                project=conversation.project,
                service_name=service,
                display_order=i,
                is_primary=(i == 0)  # First service is primary
            )
        
        # Store in conversation data
        conversation.conversation_data['services'] = services
        conversation.save()
        
        # Generate business details collection message
        business_name = conversation.project.business_name
        services_list = "\n".join([f"• **{service}**" for service in services])
        
        message = f"""
        Excellent! I've noted that **{business_name}** offers these services:
        
        {services_list}
        
        Now I need a few more details to create compelling content for your website:
        
        **1. Where are you located?** - City, region, or "We serve [area]"
        
        **2. Contact information:**
        - Phone number (optional)
        - Email address (optional)
        
        You can answer all at once or one at a time - whatever feels comfortable! 😊
        """
        
        # Advance to next step
        conversation.advance_step()
        
        return message.strip()
    
    def _step_business_details(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Collect business details and prepare for template selection
        """
        if not user_input:
            return "Please share some information about your business - even a brief description helps!"
        
        # Parse and store business details
        details = self._parse_business_details(user_input)
        
        # Update project with collected details
        project = conversation.project
        if details.get('description'):
            project.business_description = details['description']
        if details.get('target_audience'):
            project.target_audience = details['target_audience']
        if details.get('location'):
            project.location = details['location']
        if details.get('phone'):
            project.phone = details['phone']
        if details.get('email'):
            project.email = details['email']
        
        project.save()
        
        # Store in conversation data
        conversation.conversation_data.update(details)
        conversation.save()
        
        # Generate template selection message
        business_name = project.business_name
        industry = project.industry
        
        # Get recommended templates for this industry
        templates = WebsiteTemplate.objects.filter(
            category=industry, 
            is_active=True,
            supports_one_page=True
        ).order_by('-rating')[:3]
        
        if not templates.exists():
            # Fallback to general business templates
            templates = WebsiteTemplate.objects.filter(
                category='business',
                is_active=True,
                supports_one_page=True
            ).order_by('-rating')[:3]
        
        message = f"""
        Fantastic! I have all the information I need about **{business_name}**! 🎉
        
        Perfect! I've designed a **professional, universal template** that's perfect for your business in the {industry.replace('_', ' ').title()} industry.
        
        This template features:
        • Modern, responsive design that works on all devices
        • Professional service showcase section
        • About section with your company story
        • Contact form and business information
        • Fully customizable colors and fonts
        • Fast loading and SEO optimized
        
        **Here's your website template:**
        
        """
        
        # Show the single excellent template
        if templates.exists():
            template = templates.first()  # Get the single template
            preview_url = template.thumbnail_image or template.preview_image or "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop"
            
            message += f'''
        <div class="template-showcase mt-4 mb-4">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="card template-card-single h-100" onclick="selectTemplate(1)" data-template="{template.template_id}">
                        <div class="template-image-container">
                            <img src="{preview_url}" class="card-img-top template-preview-large" alt="{template.name}" loading="lazy">
                            <div class="template-overlay">
                                <div class="template-overlay-content">
                                    <i class="fas fa-eye fa-2x mb-2"></i>
                                    <h5>Preview Your Website</h5>
                                    <p>See how your website will look</p>
                                </div>
                            </div>
                        </div>
                        <div class="card-body text-center">
                            <h4 class="card-title text-primary mb-3">{template.name}</h4>
                            <p class="card-text">{template.description}</p>
                            <div class="template-features mb-3">
                                <div class="row">
                                    <div class="col-6">
                                        <i class="fas fa-mobile-alt text-primary"></i>
                                        <small class="d-block">Mobile Responsive</small>
                                    </div>
                                    <div class="col-6">
                                        <i class="fas fa-palette text-primary"></i>
                                        <small class="d-block">Customizable Colors</small>
                                    </div>
                                </div>
                                <div class="row mt-2">
                                    <div class="col-6">
                                        <i class="fas fa-rocket text-primary"></i>
                                        <small class="d-block">Fast Loading</small>
                                    </div>
                                    <div class="col-6">
                                        <i class="fas fa-search text-primary"></i>
                                        <small class="d-block">SEO Optimized</small>
                                    </div>
                                </div>
                            </div>
                            <div class="template-stats mb-3">
                                <span class="badge bg-success me-2">⭐ {template.rating}/5.0 Rating</span>
                                <span class="badge bg-info">🎨 {len(template.color_schemes)} Color Schemes</span>
                            </div>
                        </div>
                        <div class="card-footer bg-transparent">
                            <div class="d-flex gap-2">
                                <button class="btn btn-outline-primary btn-lg flex-grow-1" onclick="event.stopPropagation(); previewTemplate('{preview_url}', '{template.name}')">
                                    👁️ Preview Template
                                </button>
                                <button class="btn btn-primary btn-lg flex-grow-1" onclick="event.stopPropagation(); selectTemplate(1)">
                                    ✅ Use This Template
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
            '''
        else:
            message += '<div class="template-selection mt-4 mb-4">\n'
            message += '    <div class="row">\n'
            
            templates_fallback = [
                {
                    'name': 'Professional Business',
                    'description': 'Clean, modern design perfect for any business. Features service showcase, about section, and contact form.',
                    'rating': 4.8,
                    'usage': 1250,
                    'preview': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop&crop=center'
                },
                {
                    'name': 'Industry Expert', 
                    'description': 'Professional layout highlighting expertise and experience. Great for service-based businesses.',
                    'rating': 4.9,
                    'usage': 980,
                    'preview': 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=400&h=300&fit=crop&crop=center'
                },
                {
                    'name': 'Modern Corporate',
                    'description': 'Contemporary design with focus on trust and professionalism. Ideal for established businesses.',
                    'rating': 4.7,
                    'usage': 870,
                    'preview': 'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400&h=300&fit=crop&crop=center'
                }
            ]
            
            for i, template in enumerate(templates_fallback, 1):
                preview_url = template['preview']
                message += f'''
        <div class="col-md-4 mb-3">
            <div class="card template-card h-100" onclick="selectTemplate({i})" data-template="template_{i}">
                <div class="template-image-container">
                    <img src="{preview_url}" class="card-img-top template-preview" alt="{template['name']}" loading="lazy">
                    <div class="template-overlay">
                        <div class="template-overlay-content">
                            <i class="fas fa-eye"></i>
                            <span>Preview Template</span>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <h6 class="card-title"><strong>Template {i}: {template['name']}</strong></h6>
                    <p class="card-text small">{template['description']}</p>
                    <div class="template-stats">
                        <small class="text-muted">
                            ⭐ {template['rating']}/5.0 | 👥 {template['usage']} users
                        </small>
                    </div>
                </div>
                <div class="card-footer bg-transparent">
                    <div class="d-flex gap-2">
                        <button class="btn btn-outline-info btn-sm flex-grow-1" onclick="event.stopPropagation(); previewTemplate('{preview_url}', '{template['name']}')">
                            👁️ Preview
                        </button>
                        <button class="btn btn-primary btn-sm flex-grow-1" onclick="event.stopPropagation(); selectTemplate({i})">
                            ✅ Choose
                        </button>
                    </div>
                </div>
            </div>
        </div>
                '''
            
            message += '    </div>\n'
            message += '</div>\n'
        
        message += """
        <div class="template-selection-help mt-4">
            <div class="alert alert-info text-center">
                <h5><i class="fas fa-magic me-2"></i>Ready to Create Your Website!</h5>
                <p class="mb-2"><strong>Click "Use This Template" above to get started!</strong></p>
                <p class="mb-0">
                    <small>💡 You can also just type "yes" or "1" to proceed</small><br>
                    <small>✨ We'll customize colors, content, and styling to match your business perfectly!</small>
                </p>
            </div>
        </div>
        """
        
        # Advance to next step
        conversation.advance_step()
        
        return message.strip()
    
    def _step_template_selection(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Process template selection and start content generation
        """
        if not user_input:
            return "Please choose a template (1, 2, or 3) or tell me what style you prefer!"
        
        # Process template choice
        template_choice = self._parse_template_choice(user_input)
        
        # Save template selection
        conversation.project.template_id = template_choice
        conversation.project.save()
        
        conversation.conversation_data['template_choice'] = template_choice
        conversation.save()
        
        # Start content generation
        business_name = conversation.project.business_name
        
        message = f"""
        Perfect choice! ✨ I'll use **{template_choice}** for **{business_name}**.
        
        🤖 **Now I'm generating your website content...**
        
        I'm creating:
        • Compelling headlines and descriptions
        • Professional service descriptions  
        • About us section highlighting your expertise
        • Contact information and call-to-actions
        
        This will take just a moment... ⏳
        
        **While I work, let me ask:** 
        What tone would you prefer for your website content?
        
        📝 **Professional** - Formal, trustworthy, business-focused
        😊 **Friendly** - Warm, approachable, conversational  
        🎨 **Creative** - Unique, artistic, standout messaging
        
        Type "professional", "friendly", or "creative" (or I'll use professional as default).
        """
        
        # Advance to next step  
        conversation.advance_step()
        
        return message.strip()
    
    def _step_content_generation(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Generate website content using AI and present for review
        """
        # Parse content tone preference
        tone = self._parse_content_tone(user_input) if user_input else 'professional'
        
        conversation.project.content_tone = tone
        conversation.project.save()
        
        # Generate content using MagicAI
        try:
            content = self._generate_website_content(conversation.project)
            
            # Store generated content
            conversation.project.generated_content = content
            conversation.project.status = 'content_review'
            conversation.project.save()
            
            business_name = conversation.project.business_name
            
            message = f"""
            🎉 **Content Generated Successfully!**
            
            Here's what I've created for **{business_name}**:
            
            **🏆 HERO SECTION:**
            *{content.get('hero_headline', 'Professional Business Solutions')}*
            
            {content.get('hero_description', 'We provide exceptional services to help your business grow and succeed.')}
            
            **📋 SERVICES SECTION:**
            """
            
            # Add service descriptions
            services = conversation.project.services.all()
            for service in services[:3]:  # Show first 3 services
                service_desc = content.get('services', {}).get(service.service_name, 
                    f"Professional {service.service_name.lower()} services tailored to your needs.")
                message += f"\n• **{service.service_name}:** {service_desc}"
            
            if services.count() > 3:
                message += f"\n...and {services.count() - 3} more services"
            
            message += f"""
            
            **ℹ️ ABOUT US:**
            {content.get('about_content', f'{business_name} is committed to delivering exceptional results through professional service and attention to detail.')}
            
            ---
            
            **What do you think?** 
            
            ✅ **"Looks great!"** - Proceed with this content
            ✏️ **"Change [section]"** - Request specific changes  
            📏 **"Too long"** - I'll create a shorter version
            📏 **"Too short"** - I'll expand the content
            🎨 **"Different tone"** - I'll adjust the writing style
            
            What would you like to do?
            """
            
            # Advance to next step
            conversation.advance_step()
            
            return message.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating content: {e}")
            return """
            I encountered an issue generating your content. Let me try a different approach.
            
            Please tell me:
            1. What's the main message you want visitors to see?
            2. What makes your business unique?
            
            I'll create custom content based on your input!
            """
    
    def _step_content_review(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Handle content review and revisions
        """
        if not user_input:
            return "Please let me know what you think of the content - any changes needed?"
        
        user_feedback = user_input.lower()
        
        if any(word in user_feedback for word in ['great', 'good', 'perfect', 'looks good', 'approve']):
            # User approves content - move to final review
            business_name = conversation.project.business_name
            
            message = f"""
            🎉 **Excellent!** I'm so glad you love the content for **{business_name}**!
            
            **📋 FINAL PROJECT SUMMARY:**
            
            ✅ **Business:** {business_name}
            ✅ **Industry:** {conversation.project.industry.replace('_', ' ').title()}
            ✅ **Services:** {conversation.project.services.count()} services defined
            ✅ **Template:** {conversation.project.template_id} 
            ✅ **Content:** {conversation.project.content_tone.title()} tone
            ✅ **Page Type:** One-page website
            
            **🚀 Ready to build your website?**
            
            Once you confirm, I'll:
            • Generate the final HTML and CSS code
            • Apply your chosen template and styling
            • Create a fully functional website
            • Provide you with the files and instructions
            
            **Type "BUILD MY WEBSITE" to create your site!** 🎯
            
            Or if you want to make any last-minute changes, just let me know what to adjust.
            """
            
            # Advance to final review
            conversation.advance_step()
            
            return message.strip()
            
        elif 'too long' in user_feedback:
            return self._handle_content_too_long(conversation)
            
        elif 'too short' in user_feedback:
            return self._handle_content_too_short(conversation)
            
        elif any(word in user_feedback for word in ['change', 'different', 'modify', 'adjust']):
            return self._handle_content_changes(conversation, user_input)
            
        else:
            return """
            I'd love to help you perfect the content! 
            
            Please be specific about what you'd like me to change:
            
            • "Make it shorter" - Reduce content length
            • "Make it longer" - Add more details  
            • "Change the about section" - Modify specific parts
            • "More professional tone" - Adjust writing style
            • "Add [specific information]" - Include details
            
            What specifically would you like me to adjust?
            """
    
    def _step_final_review(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Final review before building the website
        """
        if not user_input:
            return 'Please type "BUILD MY WEBSITE" to create your site, or let me know if you want to make changes!'
        
        if 'build' in user_input.lower():
            # Generate final website files
            try:
                html_content, css_content = self._build_final_website(conversation.project)
                
                # Save final files
                conversation.project.final_html = html_content
                conversation.project.final_css = css_content
                conversation.project.status = 'completed'
                conversation.project.completion_percentage = 100
                conversation.project.save()
                
                business_name = conversation.project.business_name
                
                message = f"""
                🎉🎊 **CONGRATULATIONS!** 🎊🎉
                
                Your website for **{business_name}** is now complete!
                
                **✨ What you've got:**
                • Professional one-page website
                • Mobile-responsive design
                • SEO-optimized content
                • Contact forms and call-to-actions
                • Modern, fast-loading code
                
                **🚀 Next Steps:**
                1. **Preview your website** - Check the design and content
                2. **Request hosting** - We'll deploy it to your domain
                3. **Make final tweaks** - Small adjustments as needed
                4. **Go live!** - Launch your professional web presence
                
                **📞 Ready to publish?**
                Your website is saved in your dashboard. Contact our team to:
                • Set up hosting and domain
                • Make any final adjustments  
                • Launch your site to the world!
                
                Thank you for letting me help build your website! 😊
                
                **Clippy 2.0 signing off!** ✨
                """
                
                # Mark conversation as completed
                conversation.advance_step()
                
                return message.strip()
                
            except Exception as e:
                self.logger.error(f"Error building final website: {e}")
                return """
                I encountered an issue building your final website files. 
                Don't worry - all your content is saved!
                
                Our technical team will review your project and have your website ready shortly.
                You'll receive an email with your completed website within 24 hours.
                
                Thank you for your patience! 😊
                """
        else:
            return """
            No problem! What would you like to review or change?
            
            • Business information
            • Services offered  
            • Website content
            • Template choice
            • Content tone
            
            Just let me know what to adjust, or type "BUILD MY WEBSITE" when you're ready! 🚀
            """
    
    def _step_completion(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """
        Conversation completed - provide support options
        """
        return """
        Your website project is complete! 🎉
        
        If you need any assistance:
        • Contact our support team
        • Request design changes
        • Upgrade to multi-page website
        • Add new features
        
        We're here to help your business succeed online! 😊
        """
    
    # Helper methods for conversation processing
    
    def _detect_multiple_industries(self, user_input: str) -> List[str]:
        """Detect multiple industries from business names and descriptions"""
        user_input_lower = user_input.lower()
        detected_industries = []
        
        # Comprehensive industry keyword mapping with business name patterns
        industry_keywords = {
            # AUTOMOTIVE & TRANSPORTATION (High Priority - Specific Names)
            'tires': [
                'tyre', 'tyres', 'tire', 'tires', 'wheel', 'wheels', 'rubber',
                "jo's tyres", "joe's tires", "tire shop", "tyre shop", "wheel shop"
            ],
            'automotive': [
                'auto', 'automotive', 'car', 'vehicle', 'mechanic', 'garage', 'motor',
                'repair shop', 'service center', 'auto repair', 'car service', 'muffler'
            ],
            'transportation': [
                'taxi', 'transport', 'cab', 'uber', 'lyft', 'shuttle', 'delivery',
                'logistics', 'courier', 'freight', 'moving', 'limousine', 'chauffeur'
            ],
            
            # CONSTRUCTION & TRADES
            'construction': [
                'construction', 'building', 'contractor', 'renovation', 'remodel',
                'builders', 'carpentry', 'masonry', 'drywall', 'flooring'
            ],
            'plumbing': ['plumber', 'plumbing', 'pipes', 'drain', 'water', 'sewer'],
            'electrical': ['electrician', 'electrical', 'electric', 'wiring', 'lighting'],
            'painting': ['painter', 'painting', 'paint', 'decorating', 'colors'],
            'roofing': ['roofing', 'roofer', 'roof', 'shingle', 'gutter', 'slate'],
            
            # HEALTHCARE & WELLNESS
            'healthcare': ['medical', 'health', 'doctor', 'physician', 'clinic', 'hospital'],
            'dental': ['dental', 'dentist', 'teeth', 'orthodontist', 'oral', 'smile'],
            'physiotherapy': ['physio', 'therapy', 'rehabilitation', 'massage', 'chiropractor'],
            'veterinary': ['vet', 'veterinary', 'animal', 'pet', 'dog', 'cat', 'pets'],
            
            # FOOD & HOSPITALITY
            'restaurant': ['restaurant', 'dining', 'eatery', 'bistro', 'grill', 'kitchen'],
            'cafe': ['cafe', 'coffee', 'espresso', 'cappuccino', 'latte', 'barista'],
            'catering': ['catering', 'caterer', 'events', 'banquet', 'party'],
            'bakery': ['bakery', 'baker', 'bread', 'cake', 'pastry', 'dessert', 'sweets'],
            
            # TECHNOLOGY & IT
            'technology': ['tech', 'software', 'IT', 'digital', 'computer', 'coding'],
            'computer_repair': ['computer repair', 'pc repair', 'laptop repair', 'tech support'],
            'web_design': ['web design', 'website', 'web dev', 'digital agency', 'online'],
            
            # BEAUTY & PERSONAL CARE
            'beauty_salon': ['salon', 'beauty', 'hair', 'hairdresser', 'stylist', 'nails'],
            'barbershop': ['barber', 'barbershop', 'mens hair', 'shave', 'beard'],
            'spa': ['spa', 'massage', 'wellness', 'relaxation', 'facial', 'skincare'],
            
            # RETAIL & COMMERCE
            'retail': ['shop', 'store', 'retail', 'boutique', 'market', 'outlet'],
            'clothing': ['fashion', 'clothing', 'apparel', 'dress', 'tailor'],
            'jewelry': ['jewelry', 'jewellery', 'diamond', 'gold', 'watch', 'ring'],
            
            # PROFESSIONAL SERVICES
            'legal': ['law', 'legal', 'attorney', 'lawyer', 'solicitor', 'advocate'],
            'accounting': ['accounting', 'accountant', 'tax', 'bookkeeping', 'finance'],
            'real_estate': ['real estate', 'property', 'realtor', 'estate', 'homes'],
            'insurance': ['insurance', 'coverage', 'policy', 'claims', 'broker'],
            
            # FITNESS & SPORTS
            'fitness': ['gym', 'fitness', 'workout', 'training', 'exercise', 'crossfit'],
            'sports': ['sports', 'athletics', 'coaching', 'team', 'league'],
            
            # EDUCATION & CHILDCARE
            'education': ['school', 'education', 'tutoring', 'learning', 'academy'],
            'childcare': ['daycare', 'childcare', 'nursery', 'kids', 'children'],
            
            # HOME & GARDEN
            'landscaping': ['landscape', 'lawn', 'garden', 'yard', 'tree', 'grass'],
            'cleaning': ['cleaning', 'cleaner', 'maid', 'janitorial', 'housekeeping', 'window washing', 'window cleaner', 'windows', 'washing'],
            'pest_control': ['pest', 'exterminator', 'bug', 'termite', 'rodent'],
            
            # ENTERTAINMENT & EVENTS
            'photography': ['photo', 'photography', 'photographer', 'camera', 'studio'],
            'music': ['music', 'musician', 'band', 'dj', 'sound', 'recording'],
            'event_planning': ['events', 'planning', 'wedding', 'party', 'celebration'],
            
            # MANUFACTURING & INDUSTRIAL
            'manufacturing': ['manufacturing', 'factory', 'production', 'industrial'],
            'printing': ['printing', 'printer', 'graphics', 'signs', 'design']
        }
        
        # First, try exact business name matches (for cases like "Jo's Tyres", "Window Washing")
        # Use word boundaries to avoid partial matches (e.g., "care" matching "car")
        import re
        for industry, keywords in industry_keywords.items():
            for keyword in keywords:
                # Use word boundaries for single words, direct match for phrases
                if ' ' in keyword:
                    # Multi-word phrases - use direct match
                    if keyword in user_input_lower:
                        if industry not in detected_industries:
                            detected_industries.append(industry)
                else:
                    # Single words - use word boundaries to avoid partial matches
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    if re.search(pattern, user_input_lower):
                        if industry not in detected_industries:
                            detected_industries.append(industry)
        
        # Fallback to general business terms (only if no specific industries found)
        if not detected_industries:
            general_keywords = {
                'professional_services': ['consulting', 'business', 'service', 'company', 'solutions', 'group', 'corp', 'llc', 'inc']
            }
            
            for industry, keywords in general_keywords.items():
                for keyword in keywords:
                    if keyword in user_input_lower:
                        detected_industries.append(industry)
        
        # Return detected industries or unknown
        return detected_industries if detected_industries else ['unknown']

    def _detect_industry(self, user_input: str) -> str:
        """Single industry detection (legacy method for compatibility)"""
        industries = self._detect_multiple_industries(user_input)
        return industries[0] if industries else 'unknown'
    
    def _parse_services(self, user_input: str, industry: str) -> List[str]:
        """Parse services from user input"""
        # Simple parsing - split by common separators
        separators = [',', '\n', ';', ' and ', ' & ']
        services = [user_input]
        
        for sep in separators:
            new_services = []
            for service in services:
                new_services.extend([s.strip() for s in service.split(sep) if s.strip()])
            services = new_services
        
        # Clean and limit services
        services = [s.title() for s in services if len(s) > 2][:8]  # Max 8 services
        
        if not services:
            # Fallback to industry defaults
            services = self.industry_services.get(industry, ['Main Service'])[:3]
        
        return services
    
    def _parse_business_details(self, user_input: str) -> Dict[str, str]:
        """Parse business details from user input"""
        details = {}
        
        # Simple parsing logic - you can enhance this
        lines = user_input.split('\n')
        full_text = user_input.lower()
        
        # Extract email
        import re
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', user_input)
        if email_match:
            details['email'] = email_match.group()
        
        # Extract phone
        phone_match = re.search(r'[\+]?[\d\s\-\(\)]{10,}', user_input)
        if phone_match:
            details['phone'] = phone_match.group().strip()
        
        # Store full text as description for now
        details['description'] = user_input
        
        return details
    
    def _parse_template_choice(self, user_input: str) -> str:
        """Parse template choice from user input"""
        # With single template, always return the universal template
        return 'professional_universal_v1'
    
    def _parse_content_tone(self, user_input: str) -> str:
        """Parse content tone preference"""
        user_input_lower = user_input.lower()
        if 'friendly' in user_input_lower:
            return 'friendly'
        elif 'creative' in user_input_lower:
            return 'creative'
        else:
            return 'professional'
    
    def _generate_website_content(self, project: WebsiteProject) -> Dict[str, Any]:
        """Generate website content using AI"""
        business_info = {
            'company_name': project.business_name,
            'industry': project.industry,
            'location': project.location,
            'services': ', '.join([s.service_name for s in project.services.all()]),
            'target_audience': project.target_audience,
            'tone': project.content_tone,
        }
        
        # Use parent class method to generate content
        return self.generate_website_content(business_info)
    
    def _build_final_website(self, project: WebsiteProject) -> Tuple[str, str]:
        """Build final HTML and CSS for the website"""
        # This would generate the actual website files
        # For now, return basic template
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{project.business_name}</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <header>
                <h1>{project.business_name}</h1>
                <nav>
                    <a href="#services">Services</a>
                    <a href="#about">About</a>
                    <a href="#contact">Contact</a>
                </nav>
            </header>
            
            <section class="hero">
                <h2>{project.generated_content.get('hero_headline', 'Professional Services')}</h2>
                <p>{project.generated_content.get('hero_description', 'Quality service you can trust')}</p>
            </section>
            
            <section id="services">
                <h2>Our Services</h2>
                <div class="services-grid">
        """
        
        for service in project.services.all():
            html_template += f"""
                    <div class="service-card">
                        <h3>{service.service_name}</h3>
                        <p>{service.short_description or 'Professional service tailored to your needs.'}</p>
                    </div>
            """
        
        html_template += f"""
                </div>
            </section>
            
            <section id="about">
                <h2>About Us</h2>
                <p>{project.business_description or project.generated_content.get('about_content', 'We are committed to excellence.')}</p>
            </section>
            
            <section id="contact">
                <h2>Contact Us</h2>
                <p>Location: {project.location}</p>
                <p>Phone: {project.phone}</p>
                <p>Email: {project.email}</p>
            </section>
        </body>
        </html>
        """
        
        css_template = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        header { background: #333; color: white; padding: 1rem; }
        nav a { color: white; margin: 0 1rem; text-decoration: none; }
        .hero { background: #f4f4f4; padding: 3rem 1rem; text-align: center; }
        section { padding: 2rem 1rem; }
        .services-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
        .service-card { background: #f9f9f9; padding: 1rem; border-radius: 5px; }
        """
        
        return html_template, css_template
    
    def _handle_content_too_long(self, conversation: WebsiteBuilderConversation) -> str:
        """Handle request to shorten content"""
        return """
        I understand you'd like shorter content! 
        
        I have two options:
        
        **Option 1: Shorter Content** ✂️
        I'll create a more concise version that fits perfectly on a one-page site.
        
        **Option 2: Multi-Page Website** 📄
        Keep the detailed content but spread it across multiple pages (Home, Services, About, Contact).
        
        Which would you prefer?
        - Type "shorter" for concise one-page content
        - Type "multi-page" to upgrade to a multi-page website
        """
    
    def _handle_content_too_short(self, conversation: WebsiteBuilderConversation) -> str:
        """Handle request to expand content"""
        return """
        Perfect! I'll add more detailed content to better showcase your business.
        
        What would you like me to expand on?
        • More detailed service descriptions
        • Longer about us section
        • Customer testimonials section
        • Your experience and expertise
        • Company history and values
        
        Or I can expand everything to create richer, more comprehensive content?
        """
    
    def _handle_content_changes(self, conversation: WebsiteBuilderConversation, user_input: str) -> str:
        """Handle specific content change requests"""
        return f"""
        I'd be happy to make those changes!
        
        You mentioned: "{user_input}"
        
        To make the perfect adjustments:
        
        **Which section needs changes?**
        • Hero headline/description
        • Service descriptions  
        • About us content
        • Overall tone/style
        
        **What specific changes?**
        • Different wording
        • More/less formal tone
        • Add specific information
        • Remove certain parts
        
        Please tell me exactly what to change and I'll update it right away! ✨
        """
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """Generate error response"""
        return {
            'success': False,
            'message': f"❌ {message}",
            'error': True
        }