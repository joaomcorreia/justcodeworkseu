"""
Frontend AI Chat Widget Views
Customer support assistant that reads website pages
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from ai_assistant.magic_ai import magic_ai

logger = logging.getLogger(__name__)


def chat_widget_page(request):
    """
    Demo page showing the AI chat widget in action
    """
    context = {
        'page_title': 'AI Assistant Demo - JustCodeWorks.EU',
        'company_name': 'JustCodeWorks.EU'
    }
    return render(request, 'ai_assistant/chat_widget_demo.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def frontend_chat_api(request):
    """
    API endpoint for frontend AI assistant
    Handles customer support queries
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        language = data.get('language', 'en')
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
        
        # Get AI response
        response = magic_ai.chat_with_assistant(
            user_message=user_message,
            conversation_id=session_id,
            language=language
        )
        
        # Format response for frontend
        return JsonResponse({
            'success': True,
            'message': response.get('message', 'I apologize, but I cannot respond at the moment.'),
            'suggestions': response.get('suggestions', []),
            'session_id': session_id,
            'intent': response.get('intent', 'general'),
            'response_time': response.get('response_time', 0)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Frontend chat API error: {e}")
        return JsonResponse({
            'error': 'Sorry, I encountered an error. Please try again.',
            'success': False
        }, status=500)


@csrf_exempt  
@require_http_methods(["POST"])
def collect_visitor_info(request):
    """
    Collect visitor information during chat for lead generation
    """
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        visitor_info = data.get('visitor_info', {})
        
        if not session_id:
            return JsonResponse({'error': 'Session ID required'}, status=400)
        
        # Update conversation with visitor info
        from ai_assistant.models import Conversation
        
        try:
            conversation = Conversation.objects.get(session_id=session_id)
            
            # Update visitor information
            if visitor_info.get('name'):
                conversation.visitor_name = visitor_info['name']
            if visitor_info.get('email'):
                conversation.visitor_email = visitor_info['email']
            if visitor_info.get('company'):
                conversation.visitor_company = visitor_info['company']
            if visitor_info.get('phone'):
                conversation.visitor_phone = visitor_info['phone']
                
            # Update session type based on collected info
            if conversation.visitor_email:
                conversation.session_type = 'lead'
            
            conversation.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Information saved successfully'
            })
            
        except Conversation.DoesNotExist:
            return JsonResponse({'error': 'Conversation not found'}, status=404)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Visitor info collection error: {e}")
        return JsonResponse({'error': 'Failed to save information'}, status=500)


def chat_widget_config(request):
    """
    Configuration endpoint for chat widget
    Returns widget settings and initial data
    """
    config = {
        'welcome_message': 'Hi! 👋 I\'m here to help you with any questions about JustCodeWorks.EU services. How can I assist you today?',
        'company_name': 'JustCodeWorks.EU',
        'support_languages': ['en', 'nl', 'de', 'fr', 'es', 'pt'],
        'quick_questions': [
            'What services do you offer?',
            'How much does a website cost?',
            'How long does development take?',
            'Do you provide ongoing support?',
            'Can you help with SEO?'
        ],
        'business_hours': {
            'timezone': 'Europe/Amsterdam',
            'weekdays': '9:00 AM - 6:00 PM CET',
            'weekend': '10:00 AM - 4:00 PM CET',
            'sunday': 'Closed'
        },
        'contact_info': {
            'email': 'info@justcodeworks.eu',
            'phone': '+31 (123) 456-789'
        }
    }
    
    return JsonResponse(config)