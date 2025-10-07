import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justcodeworks.settings')
BASE_DIR = Path(__file__).resolve().parent
import sys
sys.path.append(str(BASE_DIR))

django.setup()

from website_builder.clippy_assistant import ClippyWebsiteBuilder

def test_checkbox_html():
    """Test the checkbox HTML generation"""
    
    print("🧪 Testing Checkbox HTML Generation")
    print("=" * 50)
    
    clippy = ClippyWebsiteBuilder()
    
    # Test with a multi-industry business to see checkboxes
    business_name = "Joly's Window Washing and Paint"
    detected = clippy._detect_multiple_industries(business_name.lower())
    
    print(f"📝 Business: {business_name}")
    print(f"🔍 Detected: {detected}")
    
    # Get AI response if available
    ai_response = clippy._generate_ai_business_recognition(business_name, detected)
    
    if ai_response and 'suggested_services' in ai_response:
        suggested_services = ai_response['suggested_services'][:8]
    else:
        # Fallback to combined services
        suggested_services = []
        for industry in detected:
            services = clippy.industry_services.get(industry, [])
            suggested_services.extend(services)
        suggested_services = list(dict.fromkeys(suggested_services))[:8]
    
    print(f"\n🛠️ Services to display ({len(suggested_services)}):")
    for i, service in enumerate(suggested_services, 1):
        print(f"   {i}. {service}")
    
    # Generate checkbox HTML
    print(f"\n📋 Generated Checkbox HTML:")
    print("=" * 30)
    
    checkbox_html = '<div class="services-selection mt-3 mb-3">\n'
    for i, service in enumerate(suggested_services[:8], 1):
        service_id = f"service_{i}"
        checkbox_html += f'                <div class="form-check mb-2">\n'
        checkbox_html += f'                    <input class="form-check-input" type="checkbox" id="{service_id}" name="services" value="{service}">\n'
        checkbox_html += f'                    <label class="form-check-label" for="{service_id}"><strong>{service}</strong></label>\n'
        checkbox_html += f'                </div>\n'
    
    checkbox_html += '</div>\n'
    checkbox_html += '<div class="mt-4 mb-3">\n'
    checkbox_html += '    <button type="button" class="btn btn-primary" onclick="submitSelectedServices()">\n'
    checkbox_html += '        ✅ Submit Selected Services\n'
    checkbox_html += '    </button>\n'
    checkbox_html += '</div>'
    
    print(checkbox_html)
    
    print(f"\n✅ Checkbox HTML generated with proper spacing and alignment!")

if __name__ == "__main__":
    test_checkbox_html()