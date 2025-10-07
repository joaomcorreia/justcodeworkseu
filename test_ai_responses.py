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

def test_ai_powered_responses():
    """Test AI-powered business recognition"""
    
    print("🧪 Testing AI-Powered Business Recognition")
    print("=" * 50)
    
    clippy = ClippyWebsiteBuilder()
    
    # Test AI recognition
    test_cases = [
        "Joly's Window Washing and Paint",
        "Mike's Italian Restaurant", 
        "Downtown Dental Care",
        "Elite Auto Repair"
    ]
    
    for business_name in test_cases:
        print(f"\n📝 Testing: '{business_name}'")
        print("-" * 40)
        
        try:
            # Detect industries first
            detected = clippy._detect_multiple_industries(business_name.lower())
            print(f"🔍 Detected Industries: {detected}")
            
            # Test AI recognition
            ai_response = clippy._generate_ai_business_recognition(business_name, detected)
            
            if ai_response:
                print("✅ AI Response Generated!")
                print(f"🤖 Recognition: {ai_response.get('recognition_message', 'N/A')}")
                print(f"🛠️ AI Services ({len(ai_response.get('suggested_services', []))}):")
                for i, service in enumerate(ai_response.get('suggested_services', [])[:5], 1):
                    print(f"   {i}. {service}")
                if len(ai_response.get('suggested_services', [])) > 5:
                    print(f"   ... and {len(ai_response.get('suggested_services', [])) - 5} more")
            else:
                print("❌ AI response failed, would use fallback")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_ai_powered_responses()