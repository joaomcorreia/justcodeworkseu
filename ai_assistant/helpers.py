"""
AI Assistant Helper Functions for JustCodeWorks
Easy functions to manage and train your AI assistant
"""

def train_ai_with_website():
    """
    Simple function to train AI with current website content
    Call this whenever you update your static pages
    """
    from ai_assistant.magic_ai import magic_ai
    
    print("🤖 Training AI assistant with website content...")
    
    try:
        success = magic_ai.crawl_website_pages()
        
        if success:
            print("✅ AI training successful!")
            print("💡 Your AI can now answer questions about:")
            print("   - Your services and pricing")
            print("   - Company information") 
            print("   - Contact details")
            print("   - Privacy policy and terms")
            return True
        else:
            print("❌ AI training failed. Check logs for details.")
            return False
            
    except Exception as e:
        print(f"❌ Error training AI: {e}")
        return False


def add_custom_knowledge(title, content, content_type='faq', keywords=None, priority=3):
    """
    Add custom knowledge to AI assistant
    
    Args:
        title: Title for the knowledge entry
        content: The actual content/answer
        content_type: Type of content ('faq', 'service', 'pricing', 'process', 'feature', 'policy')
        keywords: List of keywords that trigger this content
        priority: Priority level (1-10, higher = more important)
    
    Example:
        add_custom_knowledge(
            title="Website Development Timeline",
            content="Our websites typically take 5-10 business days to complete, depending on complexity.",
            content_type="service",
            keywords=["timeline", "how long", "delivery", "when ready"],
            priority=5
        )
    """
    try:
        from ai_assistant.models import AIKnowledgeBase
        from django.contrib.auth.models import User
        
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Please create one first.")
            return False
        
        # Set default keywords if none provided
        if keywords is None:
            keywords = []
        
        # Create knowledge entry
        knowledge = AIKnowledgeBase.objects.create(
            title=title,
            content_type=content_type,
            content=content,
            keywords=keywords,
            priority=priority,
            created_by=admin_user
        )
        
        print(f"✅ Added knowledge: {title}")
        print(f"📝 Content type: {content_type}")
        print(f"🔍 Keywords: {', '.join(keywords) if keywords else 'None'}")
        return True
        
    except Exception as e:
        print(f"❌ Error adding knowledge: {e}")
        return False


def test_ai_response(question, language='en'):
    """
    Test how your AI responds to a question
    
    Args:
        question: The question to ask
        language: Language code ('en', 'nl', 'de', 'fr', 'es', 'pt')
    
    Example:
        test_ai_response("How much does a website cost?")
        test_ai_response("Wat kost een website?", language='nl')
    """
    try:
        from ai_assistant.magic_ai import magic_ai
        
        print(f"❓ Question: {question}")
        print(f"🌍 Language: {language}")
        print("🤖 AI Response:")
        print("-" * 50)
        
        # Create a test conversation
        response = magic_ai.chat_with_assistant(
            user_message=question,
            conversation_id=f"test_{hash(question)}",
            language=language
        )
        
        print(response.get('message', 'No response'))
        print("-" * 50)
        
        suggestions = response.get('suggestions', [])
        if suggestions:
            print("💡 Suggested follow-up questions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
        
        return response
        
    except Exception as e:
        print(f"❌ Error testing AI: {e}")
        return None


def get_ai_knowledge_stats():
    """
    Get statistics about your AI's knowledge base
    """
    try:
        from ai_assistant.models import AIKnowledgeBase
        
        total_entries = AIKnowledgeBase.objects.count()
        active_entries = AIKnowledgeBase.objects.filter(is_active=True).count()
        
        # Count by content type
        content_types = AIKnowledgeBase.objects.values_list('content_type', flat=True).distinct()
        
        print("📊 AI Knowledge Base Statistics")
        print("=" * 40)
        print(f"📚 Total entries: {total_entries}")
        print(f"✅ Active entries: {active_entries}")
        print(f"❌ Inactive entries: {total_entries - active_entries}")
        print()
        
        print("📋 Content by type:")
        for content_type in content_types:
            count = AIKnowledgeBase.objects.filter(content_type=content_type).count()
            print(f"   {content_type}: {count}")
        
        print()
        print("🔥 Most used knowledge:")
        top_used = AIKnowledgeBase.objects.filter(usage_count__gt=0).order_by('-usage_count')[:5]
        for knowledge in top_used:
            print(f"   {knowledge.title} (used {knowledge.usage_count} times)")
        
        from django.db import models
        
        return {
            'total': total_entries,
            'active': active_entries,
            'content_types': dict(AIKnowledgeBase.objects.values('content_type').annotate(count=models.Count('id')).values_list('content_type', 'count'))
        }
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return None


# Quick helper functions for common use cases
def quick_faq(question, answer, keywords=None):
    """Quick way to add FAQ"""
    return add_custom_knowledge(
        title=f"FAQ: {question}",
        content=answer,
        content_type='faq',
        keywords=keywords or [],
        priority=4
    )

def quick_service_info(service_name, description, keywords=None):
    """Quick way to add service information"""
    return add_custom_knowledge(
        title=f"Service: {service_name}",
        content=description,
        content_type='service',
        keywords=keywords or [],
        priority=5
    )

def quick_pricing_info(item, price_info, keywords=None):
    """Quick way to add pricing information"""
    return add_custom_knowledge(
        title=f"Pricing: {item}",
        content=price_info,
        content_type='pricing',
        keywords=keywords or ['price', 'cost', 'pricing'],
        priority=6
    )


if __name__ == "__main__":
    # Example usage
    print("🤖 JustCodeWorks AI Assistant Helper")
    print("Available functions:")
    print("- train_ai_with_website()")
    print("- add_custom_knowledge(title, content, ...)")
    print("- test_ai_response(question)")
    print("- get_ai_knowledge_stats()")
    print("- quick_faq(question, answer)")
    print("- quick_service_info(name, description)")
    print("- quick_pricing_info(item, price_info)")