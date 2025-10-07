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

def test_multi_industry_detection():
    """Test the multi-industry detection system"""
    
    print("🧪 Testing Multi-Industry Detection System")
    print("=" * 50)
    
    clippy = ClippyWebsiteBuilder()
    
    # Test cases
    test_cases = [
        "Joly's Window Washing and Paint",
        "ABC Plumbing and Electrical", 
        "Mike's Auto Repair and Tires",
        "Simple Bakery"  # Single industry for comparison
    ]
    
    for business_name in test_cases:
        print(f"\n📝 Testing: '{business_name}'")
        print("-" * 30)
        
        try:
            # Test the detection method directly
            detected = clippy._detect_multiple_industries(business_name.lower())
            
            print(f"🔍 Detected Industries: {detected}")
            
            if len(detected) > 1:
                print(f"✅ Multi-industry business detected: {', '.join([ind.replace('_', ' ').title() for ind in detected])}")
            elif detected and detected[0] != 'unknown':
                print(f"✅ Single industry detected: {detected[0].replace('_', ' ').title()}")
            else:
                print("🤔 No specific industry detected")
            
            # Test service combination
            combined_services = []
            for industry in detected:
                services = clippy.industry_services.get(industry, [])
                combined_services.extend(services)
            
            # Remove duplicates
            combined_services = list(dict.fromkeys(combined_services))[:10]
            
            print(f"�️ Combined Services ({len(combined_services)}): {', '.join(combined_services[:5])}{'...' if len(combined_services) > 5 else ''}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_multi_industry_detection()