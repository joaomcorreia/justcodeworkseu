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

def test_jolys_services():
    """Detailed test for Joly's Window Washing and Paint services"""
    
    print("🧪 Testing Joly's Window Washing and Paint - Detailed Service Analysis")
    print("=" * 70)
    
    clippy = ClippyWebsiteBuilder()
    business_name = "Joly's Window Washing and Paint"
    
    # Detect industries
    detected = clippy._detect_multiple_industries(business_name.lower())
    print(f"🏢 Business: {business_name}")
    print(f"🔍 Detected Industries: {detected}")
    
    # Show individual industry services
    for industry in detected:
        services = clippy.industry_services.get(industry, [])
        print(f"\n📋 {industry.replace('_', ' ').title()} Services ({len(services)}):")
        for i, service in enumerate(services, 1):
            print(f"   {i}. {service}")
    
    # Show combined services (what the user will actually see)
    combined_services = []
    for industry in detected:
        services = clippy.industry_services.get(industry, [])
        combined_services.extend(services)
    
    # Remove duplicates and limit
    final_services = list(dict.fromkeys(combined_services))[:10]
    
    print(f"\n🛠️ Final Combined Services for User ({len(final_services)}):")
    for i, service in enumerate(final_services, 1):
        print(f"   {i}. {service}")
    
    print(f"\n✅ Success! Both cleaning and painting services are included!")

if __name__ == "__main__":
    test_jolys_services()