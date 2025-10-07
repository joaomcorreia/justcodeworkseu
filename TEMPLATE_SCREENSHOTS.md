# Template Screenshots Guide

## 📁 Directory Structure

Template screenshots are stored in the following structure:

```
media/
└── website_templates/
    ├── previews/          # Full-size preview images (800x600 recommended)
    │   ├── TP1_preview.png
    │   ├── TP2_preview.jpg
    │   └── ...
    └── thumbnails/        # Thumbnail images (400x300 recommended)
        ├── TP1_thumbnail.png
        ├── TP2_thumbnail.jpg
        └── ...
```

## 🎯 Image Requirements

### Preview Images
- **Size**: 800x600 pixels (recommended)
- **Format**: JPG, PNG, or WebP
- **Purpose**: Full-size template preview shown in selection interface
- **Naming**: `{template_id}_preview.{ext}`

### Thumbnail Images  
- **Size**: 400x300 pixels (recommended)
- **Format**: JPG, PNG, or WebP
- **Purpose**: Small preview for template galleries
- **Naming**: `{template_id}_thumbnail.{ext}`

## 🛠️ Adding Screenshots

### Method 1: Management Command (Recommended)

Copy your screenshot files and use the management command:

```bash
# Copy local files
python manage.py add_template_screenshots --template-id TP1 --preview my_preview.jpg --thumbnail my_thumb.jpg

# Use direct URLs
python manage.py add_template_screenshots --template-id TP1 --preview-url https://example.com/preview.jpg --thumbnail-url https://example.com/thumb.jpg
```

### Method 2: Direct File Placement

1. Copy your images to the appropriate directories:
   ```
   media/website_templates/previews/TP1_preview.jpg
   media/website_templates/thumbnails/TP1_thumbnail.jpg
   ```

2. Update the template in Django admin or shell:
   ```python
   template = WebsiteTemplate.objects.get(template_id='TP1')
   template.preview_image = '/media/website_templates/previews/TP1_preview.jpg'
   template.thumbnail_image = '/media/website_templates/thumbnails/TP1_thumbnail.jpg'
   template.save()
   ```

### Method 3: Generate Placeholders

Generate automatic placeholder screenshots for all templates:

```bash
# Install Pillow if not already installed
pip install Pillow

# Generate placeholder screenshots
python generate_template_screenshots.py
```

## 🎨 Screenshot Best Practices

### What Makes a Good Template Screenshot

1. **Show the Complete Layout**
   - Include header, navigation, main content sections, and footer
   - Display the template's color scheme and typography
   - Show responsive design elements

2. **Use Realistic Content**
   - Business name and logo placeholder
   - Sample navigation items (Home, About, Services, Contact)
   - Representative text content
   - Service/product showcases

3. **Highlight Key Features**
   - Special design elements (gradients, shadows, animations)
   - Layout structure (columns, grids, sections)
   - Call-to-action buttons and forms

4. **Professional Quality**
   - Clean, crisp images without artifacts
   - Proper lighting and contrast
   - Consistent aspect ratios across all templates

## 🔧 Technical Details

### Model Fields

The `WebsiteTemplate` model includes:

```python
class WebsiteTemplate(models.Model):
    # ... other fields ...
    preview_image = models.URLField(blank=True)      # Full preview URL
    thumbnail_image = models.URLField(blank=True)    # Thumbnail URL
    # ... other fields ...
```

### URL Patterns

Screenshots are served through Django's media handling:

- **Preview**: `/media/website_templates/previews/{template_id}_preview.{ext}`
- **Thumbnail**: `/media/website_templates/thumbnails/{template_id}_thumbnail.{ext}`

### Usage in Templates

Display screenshots in Django templates:

```html
<!-- Full preview -->
{% if template.preview_image %}
    <img src="{{ template.preview_image }}" alt="{{ template.name }} Preview" class="template-preview">
{% endif %}

<!-- Thumbnail -->
{% if template.thumbnail_image %}
    <img src="{{ template.thumbnail_image }}" alt="{{ template.name }}" class="template-thumbnail">
{% endif %}
```

## 📊 Current Templates

Run this command to see current template screenshot status:

```bash
python manage.py shell -c "
from website_builder.models import WebsiteTemplate;
for t in WebsiteTemplate.objects.all():
    preview = '✅' if t.preview_image else '❌'
    thumbnail = '✅' if t.thumbnail_image else '❌'
    print(f'{t.template_id}: {t.name} - Preview: {preview} Thumbnail: {thumbnail}')
"
```

## 🚀 Quick Start

1. **Create directories** (if they don't exist):
   ```bash
   mkdir -p media/website_templates/previews
   mkdir -p media/website_templates/thumbnails
   ```

2. **Generate placeholders** for testing:
   ```bash
   python generate_template_screenshots.py
   ```

3. **Replace with real screenshots** as you create them:
   ```bash
   python manage.py add_template_screenshots --template-id TP1 --preview real_screenshot.jpg
   ```

4. **Verify in the admin** or website builder interface

## 🎯 Integration with Live Preview

The screenshots work seamlessly with the real-time preview system:

- **Template Selection**: Users see thumbnails when choosing templates
- **Live Preview**: Real-time rendering shows the actual template
- **Fallback**: Screenshots serve as quick visual reference

This creates a complete visual experience where users can:
1. Browse template screenshots to make initial choices
2. See live preview as content is generated
3. Compare final result with screenshot expectations