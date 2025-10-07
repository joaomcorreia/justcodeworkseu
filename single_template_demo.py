import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justcodeworks.settings')
BASE_DIR = Path(__file__).resolve().parent
import sys
sys.path.append(str(BASE_DIR))

django.setup()

from website_builder.models import WebsiteTemplate

def show_single_template_system():
    """Demonstrate the single template approach"""
    
    print("🎯 Single Template System - Quality Over Quantity")
    print("=" * 60)
    
    template = WebsiteTemplate.objects.first()
    
    if template:
        print(f"🎨 **{template.name}**")
        print(f"   ID: {template.template_id}")
        print(f"   Category: {template.category}")
        print(f"   Rating: ⭐ {template.rating}/5.0")
        print(f"   Color Schemes: {len(template.color_schemes)} options")
        print(f"   Font Options: {len(template.font_options)} choices")
        print(f"   One Page: {'✅' if template.supports_one_page else '❌'}")
        print(f"   Multi Page: {'✅' if template.supports_multi_page else '❌'}")
        
        print(f"\n📝 Description:")
        print(f"   {template.description}")
        
        print(f"\n🎨 Available Color Schemes:")
        for scheme in template.color_schemes:
            print(f"   • {scheme.replace('-', ' ').title()}")
            
        print(f"\n🔤 Available Fonts:")
        for font in template.font_options:
            print(f"   • {font}")
            
        print(f"\n📸 Media:")
        print(f"   Preview: {template.preview_image}")
        print(f"   Thumbnail: {template.thumbnail_image}")
        print(f"   Demo: {template.demo_url}")
        
    else:
        print("❌ No template found!")
        return
    
    print(f"\n✨ Single Template Benefits:")
    print("─" * 30)
    print("✅ Focus on one excellent design")
    print("✅ Perfect for all business types")
    print("✅ Consistent user experience")
    print("✅ Easy to maintain and update")
    print("✅ Fully customizable appearance")
    print("✅ Modern, responsive design")
    print("✅ Fast loading and SEO optimized")
    
    print(f"\n🔧 Template Features:")
    print("─" * 20)
    print("• Hero section with business intro")
    print("• About section with company story")
    print("• Services showcase with icons")
    print("• Contact form and information")
    print("• Professional navigation")
    print("• Responsive mobile design")
    print("• Smooth animations")
    print("• Bootstrap 5 framework")
    print("• Font Awesome icons")
    print("• Custom CSS variables")
    
    print(f"\n🎯 User Experience:")
    print("─" * 17)
    print("1. 👀 User sees single, excellent template showcase")
    print("2. 📱 Large preview image shows quality")
    print("3. 🎨 Features highlighted (responsive, customizable)")
    print("4. ✅ Simple choice: 'Use This Template'")
    print("5. 🚀 No decision paralysis - just one great option")
    
    print(f"\n💻 Technical Specifications:")
    print("─" * 27)
    print(f"📄 HTML Template: {len(template.html_template)} characters")
    print(f"🎨 CSS Template: {len(template.css_template)} characters") 
    print(f"⚡ JavaScript: {len(template.js_template)} characters")
    print(f"🔧 Total Template Size: {len(template.html_template) + len(template.css_template) + len(template.js_template):,} chars")
    
    print(f"\n🎪 Why Single Template Works:")
    print("─" * 30)
    print("• Eliminates choice overload")
    print("• Focuses on customization over selection")
    print("• Ensures consistent quality")
    print("• Easier to perfect one design")
    print("• Faster development and testing")
    print("• Better user experience")
    print("• Works for any business type")

if __name__ == "__main__":
    show_single_template_system()