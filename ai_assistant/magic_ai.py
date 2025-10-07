"""
MagicAI Integration for JustCodeWorks
OpenAI-powered content generation and AI assistant
"""
import os
import openai
import logging
from typing import Dict, Any, List, Optional
from django.conf import settings
from django.utils import timezone
from .models import Conversation, Message, AIKnowledgeBase


class MagicAI:
    """
    Core AI service class for JustCodeWorks platform
    """
    
    def __init__(self):
        """Initialize MagicAI with OpenAI configuration"""
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in settings")
        
        # Configure OpenAI client
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
    
    def generate_website_content(self, business_info: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate complete website content based on business information
        """
        try:
            prompt = f"""
            Generate professional website content for a {business_info.get('industry', 'business')} company:
            
            Company Name: {business_info.get('company_name', 'Business')}
            Industry: {business_info.get('industry', 'General Business')}
            Location: {business_info.get('location', 'Europe')}
            Services: {business_info.get('services', 'Professional services')}
            Target Audience: {business_info.get('target_audience', 'Business clients')}
            
            Generate content for:
            1. Homepage hero section (compelling headline + description)
            2. About Us page content
            3. Services overview
            4. Contact page content
            5. SEO meta description
            
            Make it engaging, professional, and conversion-focused.
            Return as JSON format with keys: hero_headline, hero_description, about_content, services_content, contact_content, meta_description
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert copywriter specializing in business websites. Generate compelling, professional content that drives conversions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                import json
                content_data = json.loads(content_text)
                return content_data
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured fallback
                return self._get_fallback_content(business_info)
                
        except Exception as e:
            self.logger.error(f"Error generating website content: {e}")
            return self._get_fallback_content(business_info)
    
    def generate_blog_content(self, topic: str, content_type: str = 'tutorial', language: str = 'en') -> Dict[str, str]:
        """
        Generate blog post content for tutorials and business tips
        """
        try:
            language_names = {
                'en': 'English',
                'nl': 'Dutch', 
                'de': 'German',
                'fr': 'French',
                'es': 'Spanish',
                'pt': 'Portuguese'
            }
            
            prompt = f"""
            Write a comprehensive {content_type} blog post about: {topic}
            
            Target audience: Small business owners and entrepreneurs using JustCodeWorks
            Language: {language_names.get(language, 'English')}
            Focus: Actionable advice that helps grow online business
            
            Include:
            1. Engaging title
            2. Brief excerpt/summary (max 300 characters)
            3. Full article content (800-1200 words)
            4. SEO meta description
            5. Suggested tags (comma-separated)
            
            Make it practical, actionable, and relate back to website/online business success.
            Return as JSON: title, excerpt, content, meta_description, tags
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert business advisor and content creator. Write practical, actionable content that helps small businesses succeed online."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content_text = response.choices[0].message.content.strip()
            
            try:
                import json
                return json.loads(content_text)
            except json.JSONDecodeError:
                return {
                    "title": f"How to {topic}",
                    "excerpt": f"Learn practical strategies for {topic} to grow your online business.",
                    "content": f"This comprehensive guide covers everything you need to know about {topic}...",
                    "meta_description": f"Learn {topic} with our step-by-step guide for small businesses.",
                    "tags": "business, tutorial, online, growth"
                }
                
        except Exception as e:
            self.logger.error(f"Error generating blog content: {e}")
            return {
                "title": f"Guide: {topic}",
                "excerpt": "Practical business guidance for online success.",
                "content": "Coming soon - comprehensive guide content.",
                "meta_description": f"Learn about {topic} for your business.",
                "tags": "business, guide"
            }
    
    def chat_with_assistant(self, user_message: str, conversation_id: str, language: str = 'en') -> Dict[str, Any]:
        """
        Handle AI assistant chat conversations
        """
        try:
            # Get or create conversation
            conversation = self._get_conversation(conversation_id)
            
            # Get relevant knowledge base content
            knowledge_context = self._get_relevant_knowledge(user_message, language)
            
            # Build conversation history
            recent_messages = self._get_recent_messages(conversation)
            
            # Analyze user intent
            user_intent = self._analyze_user_intent(user_message)
            
            # Generate AI response
            system_prompt = f"""
            You are a helpful AI assistant for JustCodeWorks.EU, a platform that empowers anyone to create professional websites effortlessly.
            
            Language: English (EU-based platform)
            User Intent: {user_intent}
            
            Key Information about JustCodeWorks:
            - Empowers people to build websites without technical knowledge
            - AI-powered platform that handles everything automatically  
            - Focus on simplicity and independence - no customer service needed
            - Clean, professional results without complexity
            - EU-based platform serving European businesses
            
            Relevant Knowledge:
            {knowledge_context}
            
            Be helpful and encouraging. Focus on how easy and empowering our platform is.
            Avoid technical jargon - speak to entrepreneurs and small business owners.
            """
            
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history
            for msg in recent_messages:
                role = "user" if msg.message_type == "user" else "assistant"
                messages.append({"role": role, "content": msg.content})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get AI response
            start_time = timezone.now()
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=500,
                temperature=0.8
            )
            end_time = timezone.now()
            
            ai_response = response.choices[0].message.content.strip()
            response_time = (end_time - start_time).total_seconds()
            
            # Save messages
            self._save_conversation_messages(
                conversation, user_message, ai_response, 
                user_intent, response_time, response.usage
            )
            
            # Generate smart suggestions
            suggestions = self._generate_smart_suggestions(user_intent, conversation)
            
            return {
                'response': ai_response,
                'suggestions': suggestions,
                'intent': user_intent,
                'conversation_id': conversation_id
            }
            
        except Exception as e:
            self.logger.error(f"Error in AI chat: {e}")
            return {
                'response': "I apologize, but I'm having trouble right now. Please try again or contact our support team.",
                'suggestions': ["Contact Support", "Try Again", "Learn More About Our Services"],
                'intent': 'error',
                'conversation_id': conversation_id
            }
    
    def _get_conversation(self, conversation_id: str) -> Conversation:
        """Get or create conversation"""
        conversation, created = Conversation.objects.get_or_create(
            session_id=conversation_id,
            defaults={'is_active': True}
        )
        return conversation
    
    def _get_relevant_knowledge(self, user_message: str, language: str) -> str:
        """Get relevant knowledge base content"""
        try:
            # Simple keyword matching for now
            knowledge_items = AIKnowledgeBase.objects.filter(
                is_active=True
            ).order_by('-priority', '-usage_count')[:3]
            
            context = ""
            for item in knowledge_items:
                content = item.get_localized_content(language)
                context += f"\n{item.title}: {content[:200]}...\n"
            
            return context
        except Exception:
            return ""
    
    def _get_recent_messages(self, conversation: Conversation, limit: int = 6) -> List[Message]:
        """Get recent conversation messages"""
        return conversation.messages.order_by('-timestamp')[:limit]
    
    def _analyze_user_intent(self, message: str) -> str:
        """Analyze user message to determine intent"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['price', 'cost', 'how much', 'pricing']):
            return 'pricing_inquiry'
        elif any(word in message_lower for word in ['help', 'support', 'problem']):
            return 'support_request'
        elif any(word in message_lower for word in ['create', 'build', 'make', 'website']):
            return 'service_inquiry'
        elif any(word in message_lower for word in ['how', 'what', 'explain']):
            return 'information_seeking'
        else:
            return 'general_chat'
    
    def _save_conversation_messages(self, conversation: Conversation, user_message: str, 
                                  ai_response: str, intent: str, response_time: float, usage):
        """Save conversation messages"""
        # Save user message
        Message.objects.create(
            conversation=conversation,
            message_type='user',
            content=user_message,
            intent_detected=intent
        )
        
        # Save AI response
        Message.objects.create(
            conversation=conversation,
            message_type='assistant',
            content=ai_response,
            ai_model='gpt-4',
            response_time=response_time,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens
        )
        
        # Update conversation stats
        conversation.message_count += 2
        conversation.detected_intent = intent
        conversation.save()
    
    def _generate_smart_suggestions(self, intent: str, conversation: Conversation) -> List[str]:
        """Generate contextual suggestions"""
        suggestions_map = {
            'pricing_inquiry': [
                "Get a Custom Quote",
                "Compare Plans",
                "Schedule a Demo",
                "View Sample Websites"
            ],
            'service_inquiry': [
                "Start Building Now",
                "See Examples",
                "Learn About Features",
                "Contact Sales"
            ],
            'support_request': [
                "View Documentation",
                "Contact Support",
                "Common Solutions",
                "Video Tutorials"
            ],
            'information_seeking': [
                "Learn More",
                "See Case Studies",
                "Read Blog Posts",
                "Watch Demo"
            ]
        }
        
        return suggestions_map.get(intent, [
            "Tell me more",
            "Get Started",
            "Contact Us",
            "View Examples"
        ])
    
    def _get_fallback_content(self, business_info: Dict[str, Any]) -> Dict[str, str]:
        """Provide fallback content when AI generation fails"""
        company_name = business_info.get('company_name', 'Your Business')
        industry = business_info.get('industry', 'business')
        
        return {
            "hero_headline": f"Professional {industry.title()} Services",
            "hero_description": f"Welcome to {company_name}. We provide excellent {industry} services with dedication and expertise.",
            "about_content": f"{company_name} is a trusted {industry} company committed to delivering exceptional results.",
            "services_content": f"We offer comprehensive {industry} solutions tailored to meet your specific needs.",
            "contact_content": f"Get in touch with {company_name} today to discuss your requirements.",
            "meta_description": f"{company_name} - Professional {industry} services. Contact us for expert solutions."
        }

    def crawl_website_pages(self, base_url: str = None) -> bool:
        """
        Crawl website pages and add content to knowledge base
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            import os
            from django.conf import settings
            
            # If no base_url provided, read static pages directly
            if not base_url:
                return self._read_static_pages()
            
            # List of pages to crawl
            pages_to_crawl = [
                ('/', 'homepage', 'Homepage content and services'),
                ('/static/index/', 'static_homepage', 'Static homepage with pricing and features'),
                ('/static/about/', 'about_page', 'Company information and team'),
                ('/static/contact/', 'contact_page', 'Contact information and services'),
                ('/static/privacy/', 'privacy_page', 'Privacy policy information'),
                ('/static/terms/', 'terms_page', 'Terms of service')
            ]
            
            success_count = 0
            for url_path, page_type, description in pages_to_crawl:
                try:
                    full_url = base_url.rstrip('/') + url_path
                    response = requests.get(full_url, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract meaningful content
                        content = self._extract_page_content(soup, page_type)
                        
                        if content:
                            # Save to knowledge base
                            self._save_page_to_knowledge_base(
                                title=f"Website: {description}",
                                content=content,
                                page_type=page_type,
                                keywords=self._extract_keywords_from_content(content)
                            )
                            success_count += 1
                            
                except Exception as e:
                    self.logger.error(f"Error crawling {url_path}: {e}")
                    continue
            
            self.logger.info(f"Successfully crawled {success_count} pages")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error in website crawling: {e}")
            return False

    def _read_static_pages(self) -> bool:
        """
        Read static HTML pages directly from filesystem
        """
        try:
            from bs4 import BeautifulSoup
            import os
            from django.conf import settings
            
            static_pages_dir = os.path.join(settings.BASE_DIR, 'static', 'pages')
            
            if not os.path.exists(static_pages_dir):
                self.logger.error(f"Static pages directory not found: {static_pages_dir}")
                return False
            
            pages_info = [
                ('index.html', 'homepage', 'Homepage with pricing and services'),
                ('about.html', 'about_page', 'Company information and team'),
                ('contact.html', 'contact_page', 'Contact information and services'),
                ('privacy.html', 'privacy_page', 'Privacy policy information'),
                ('terms.html', 'terms_page', 'Terms of service')
            ]
            
            success_count = 0
            for filename, page_type, description in pages_info:
                file_path = os.path.join(static_pages_dir, filename)
                
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            html_content = file.read()
                            
                        soup = BeautifulSoup(html_content, 'html.parser')
                        content = self._extract_page_content(soup, page_type)
                        
                        if content:
                            self._save_page_to_knowledge_base(
                                title=f"Website Page: {description}",
                                content=content,
                                page_type=page_type,
                                keywords=self._extract_keywords_from_content(content)
                            )
                            success_count += 1
                            
                    except Exception as e:
                        self.logger.error(f"Error reading {filename}: {e}")
                        continue
            
            self.logger.info(f"Successfully processed {success_count} static pages")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error reading static pages: {e}")
            return False

    def _extract_page_content(self, soup: 'BeautifulSoup', page_type: str) -> str:
        """
        Extract meaningful content from HTML soup
        """
        try:
            content_parts = []
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            if title:
                content_parts.append(f"Page Title: {title.get_text().strip()}")
            
            # Extract main headings
            for heading in soup.find_all(['h1', 'h2', 'h3']):
                heading_text = heading.get_text().strip()
                if heading_text and not heading_text.startswith('EDIT THIS'):
                    content_parts.append(f"Heading: {heading_text}")
            
            # Extract paragraphs and important content
            for element in soup.find_all(['p', 'li', '.lead', '.card-body']):
                text = element.get_text().strip()
                if text and len(text) > 20 and not text.startswith('EDIT THIS'):
                    content_parts.append(text)
            
            # Extract pricing information if present
            for price_element in soup.find_all(class_=['price', 'pricing', 'cost']):
                price_text = price_element.get_text().strip()
                if price_text:
                    content_parts.append(f"Pricing: {price_text}")
            
            # Join all content
            full_content = "\n".join(content_parts)
            
            # Clean up and limit length
            return full_content[:2000] if full_content else ""
            
        except Exception as e:
            self.logger.error(f"Error extracting content: {e}")
            return ""

    def _extract_keywords_from_content(self, content: str) -> list:
        """
        Extract relevant keywords from content for knowledge base matching
        """
        try:
            import re
            
            # Common business keywords
            business_keywords = [
                'website', 'development', 'design', 'service', 'company', 'business',
                'contact', 'about', 'team', 'price', 'pricing', 'cost', 'support',
                'professional', 'quality', 'experience', 'client', 'customer'
            ]
            
            # Extract words from content
            words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
            
            # Find relevant keywords
            relevant_keywords = []
            for keyword in business_keywords:
                if keyword in content.lower():
                    relevant_keywords.append(keyword)
            
            # Add some high-frequency words from content
            word_freq = {}
            for word in words:
                if len(word) > 4 and word.isalpha():
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Add top frequent words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            for word, _ in top_words:
                if word not in relevant_keywords:
                    relevant_keywords.append(word)
            
            return relevant_keywords[:10]  # Limit to 10 keywords
            
        except Exception:
            return ['website', 'service', 'business']

    def _save_page_to_knowledge_base(self, title: str, content: str, page_type: str, keywords: list):
        """
        Save page content to AI knowledge base
        """
        try:
            from django.contrib.auth.models import User
            
            # Get or create admin user for knowledge entries
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = User.objects.create_user(
                    username='system_crawler',
                    email='system@justcodeworks.eu',
                    is_staff=True
                )
            
            # Check if knowledge entry already exists
            existing = AIKnowledgeBase.objects.filter(
                title=title,
                content_type='service'
            ).first()
            
            if existing:
                # Update existing entry
                existing.content = content
                existing.keywords = keywords
                existing.save()
                self.logger.info(f"Updated knowledge base entry: {title}")
            else:
                # Create new entry
                AIKnowledgeBase.objects.create(
                    title=title,
                    content_type='service',
                    content=content,
                    keywords=keywords,
                    priority=5,  # High priority for website content
                    created_by=admin_user
                )
                self.logger.info(f"Created knowledge base entry: {title}")
                
        except Exception as e:
            self.logger.error(f"Error saving to knowledge base: {e}")


# Initialize global MagicAI instance
magic_ai = MagicAI()