"""
Generate placeholder template screenshots
Usage: python generate_template_screenshots.py
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import random

# Add Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'justcodeworks.settings')
import django
django.setup()

from website_builder.models import WebsiteTemplate

def create_template_screenshot(template, width=800, height=600):
    """Create a placeholder screenshot for a template"""
    
    # Color schemes for different template categories
    color_schemes = {
        'business': ['#007bff', '#6c757d', '#343a40'],
        'construction': ['#fd7e14', '#495057', '#f8f9fa'],
        'technology': ['#20c997', '#17a2b8', '#343a40'],
        'restaurant': ['#dc3545', '#ffc107', '#343a40'],
        'health': ['#28a745', '#17a2b8', '#f8f9fa'],
        'creative': ['#e83e8c', '#fd7e14', '#343a40'],
        'ecommerce': ['#6f42c1', '#20c997', '#343a40'],
        'portfolio': ['#6610f2', '#e83e8c', '#343a40'],
    }
    
    # Get colors for this template category
    colors = color_schemes.get(template.category, ['#007bff', '#6c757d', '#343a40'])
    
    # Create image
    img = Image.new('RGB', (width, height), colors[2])
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default if not available
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("arial.ttf", 36)
        text_font = ImageFont.truetype("arial.ttf", 18)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except:
        # Fall back to default font
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw header
    header_height = 80
    draw.rectangle([0, 0, width, header_height], fill=colors[0])
    
    # Draw title
    title = template.name
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 20), title, fill='white', font=title_font)
    
    # Draw navigation menu
    nav_items = ['Home', 'About', 'Services', 'Contact']
    nav_y = header_height + 20
    nav_item_width = width // len(nav_items)
    
    for i, item in enumerate(nav_items):
        x = i * nav_item_width + 20
        draw.text((x, nav_y), item, fill=colors[1], font=text_font)
    
    # Draw content sections
    content_y = nav_y + 50
    section_height = 80
    
    # Hero section
    hero_rect = [20, content_y, width-20, content_y + section_height]
    draw.rectangle(hero_rect, fill=colors[0], outline=colors[1], width=2)
    draw.text((40, content_y + 20), "Hero Section", fill='white', font=text_font)
    draw.text((40, content_y + 45), "Welcome to our business", fill='white', font=small_font)
    
    # Services section
    content_y += section_height + 20
    services_rect = [20, content_y, width-20, content_y + section_height]
    draw.rectangle(services_rect, fill='white', outline=colors[1], width=2)
    draw.text((40, content_y + 20), "Services", fill=colors[1], font=text_font)
    
    # Draw service boxes
    service_width = (width - 80) // 3
    for i in range(3):
        service_x = 40 + i * (service_width + 10)
        service_rect = [service_x, content_y + 45, service_x + service_width - 10, content_y + 70]
        draw.rectangle(service_rect, fill=colors[0])
    
    # Footer
    footer_y = height - 60
    draw.rectangle([0, footer_y, width, height], fill=colors[1])
    draw.text((20, footer_y + 20), f"© 2025 {template.name}", fill='white', font=small_font)
    
    # Add template ID watermark
    watermark = f"Template: {template.template_id}"
    watermark_bbox = draw.textbbox((0, 0), watermark, font=small_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    draw.text((width - watermark_width - 20, height - 30), watermark, fill='white', font=small_font)
    
    return img

def generate_screenshots():
    """Generate screenshots for all templates"""
    
    # Create directories
    media_dir = 'media/website_templates'
    preview_dir = f'{media_dir}/previews'
    thumbnail_dir = f'{media_dir}/thumbnails'
    
    os.makedirs(preview_dir, exist_ok=True)
    os.makedirs(thumbnail_dir, exist_ok=True)
    
    templates = WebsiteTemplate.objects.all()
    
    for template in templates:
        print(f"Generating screenshots for {template.name} ({template.template_id})...")
        
        # Generate preview (800x600)
        preview_img = create_template_screenshot(template, 800, 600)
        preview_path = f'{preview_dir}/{template.template_id}_preview.png'
        preview_img.save(preview_path)
        
        # Generate thumbnail (400x300)
        thumbnail_img = create_template_screenshot(template, 400, 300)
        thumbnail_path = f'{thumbnail_dir}/{template.template_id}_thumbnail.png'
        thumbnail_img.save(thumbnail_path)
        
        # Update template with image URLs
        template.preview_image = f'/media/website_templates/previews/{template.template_id}_preview.png'
        template.thumbnail_image = f'/media/website_templates/thumbnails/{template.template_id}_thumbnail.png'
        template.save()
        
        print(f"  ✅ Preview: {preview_path}")
        print(f"  ✅ Thumbnail: {thumbnail_path}")
    
    print(f"\n🎉 Generated screenshots for {templates.count()} templates!")
    print("\n📂 Template Screenshots Location:")
    print(f"  Preview Images:   {os.path.abspath(preview_dir)}")
    print(f"  Thumbnail Images: {os.path.abspath(thumbnail_dir)}")
    print("\n💡 Usage Examples:")
    print("  - Replace with your own images by copying to the same filenames")
    print("  - Use management command: python manage.py add_template_screenshots --template-id TP1 --preview myimage.jpg")
    print("  - Images should be 800x600 for previews, 400x300 for thumbnails")

if __name__ == '__main__':
    try:
        generate_screenshots()
    except ImportError:
        print("❌ PIL (Pillow) is required to generate placeholder images.")
        print("Install it with: pip install Pillow")
        print("\nAlternatively, you can:")
        print("1. Create your own screenshots manually")
        print("2. Place them in media/website_templates/previews/ and media/website_templates/thumbnails/")
        print("3. Use the management command to associate them with templates")