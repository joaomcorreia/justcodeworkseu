"""
Template filters for website builder
"""
from django import template

register = template.Library()

@register.filter
def format_business_type(value):
    """Format business type with emoji and proper display name"""
    if not value:
        return "Not specified"
    
    business_type_map = {
        'construction': '🏗️ Construction & Contracting',
        'automotive': '🚗 Automotive & Repair',
        'plumbing': '🔧 Plumbing & HVAC',
        'electrical': '⚡ Electrical Services',
        'cleaning': '🧹 Cleaning Services',
        'landscaping': '🌿 Landscaping & Gardening',
        'home_services': '🏠 Home Services',
        'legal': '⚖️ Legal Services',
        'accounting': '📊 Accounting & Finance',
        'consulting': '💼 Consulting',
        'real_estate': '🏡 Real Estate',
        'insurance': '🛡️ Insurance',
        'healthcare': '🏥 Healthcare & Medical',
        'portfolio': '🎨 Portfolio & Creative',
        'photography': '📸 Photography',
        'design': '✨ Design & Graphics',
        'marketing': '📈 Marketing & Advertising',
        'web_development': '💻 Web Development',
        'retail': '🛍️ Retail Store',
        'ecommerce': '🛒 E-commerce',
        'restaurant': '🍽️ Restaurant & Food',
        'fashion': '👗 Fashion & Clothing',
        'beauty': '💄 Beauty & Wellness',
        'technology': '💻 Technology & IT',
        'education': '🎓 Education & Training',
        'fitness': '💪 Fitness & Sports',
        'nonprofit': '❤️ Non-profit & Community',
        'other': '🏢 Other Business Type'
    }
    
    return business_type_map.get(value.lower(), value.replace('_', ' ').title())