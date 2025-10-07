# 🚀 JustCodeWorks.EU - European SME Digital Transformation Platform

**Government Grant Demo Ready** | **Live Clients** | **Production Deployment**  
**October 8, 2025 - Complete Platform with AI-Powered Website Builder**

A comprehensive Django platform combining **automated SaaS website creation** with **professional custom development services** for European SMEs.

## 🎯 **Business Model Overview**

### 🤖 **Automated SaaS Platform**
- **Self-service website creation** with Clippy 2.0 AI assistant
- **Multi-tenant subdomain architecture** (customer.justcodeworks.eu)
- **Real-time split-screen preview** showing live website building
- **Professional templates** with visual selection system
- **Revenue**: €29-99/month subscriptions

### 🏢 **Professional Custom Development**  
- **Direct client management** through Django admin
- **Custom Django applications** for complex business needs
- **Zero-downtime migration** from existing PHP sites
- **Revenue**: €500-2000/project

## 🌟 **Latest Features (October 2025)**

### ✨ **AI-Powered Website Builder with Real-Time Preview**
- **Clippy 2.0**: Conversational AI assistant using GPT-4
- **Split-screen interface**: Content generation on left, live preview on right
- **Real-time updates**: Watch websites build as you chat
- **Smart industry detection**: AI recognizes business type and suggests services
- **Template screenshots system**: Visual template selection with auto-generated previews

### 🎨 **Advanced Template System**
- **Professional Business Universal** template with 6 color schemes, 5 font options
- **Visual template selection** with preview screenshots and thumbnails
- **Template screenshots management** with automatic generation using Pillow
- **Responsive design** with desktop/mobile preview toggle
- **Management commands** for easy template screenshot administration

### 🏗️ **Complete Technical Stack**
- **Django 5.2.7** with production-ready architecture
- **OpenAI GPT-4** integration for AI conversations
- **Bootstrap 5.3.0** for responsive, modern UI
- **Multi-tenant support** using django-tenants
- **Real-time preview** using iframe with generated HTML
- **Media management** for template screenshots and uploads

## 📊 **Current Live Client Portfolio**

- ✅ **HMD Klusbedrijf** (hmdklusbedrijf.nl) - Converting to Django
- ✅ **Taxi Pro Service** (taxiproservice.nl) - 90% Django Ready  
- ✅ **AutoFix Garage** (autofixgarage.nl) - Migration Pipeline
- ✅ **Oficina Paulo** (oficinapaulocalibra.pt) - E-commerce Expansion

### **Government Meeting Demo:** October 7, 2025 ✅ Success!

## 🏗️ **Project Structure**

```
justcodeworkseu/
├── justcodeworks/              # Main Django project
├── website_builder/            # AI Website Builder with Clippy 2.0
│   ├── models.py              # WebsiteProject, WebsiteTemplate models
│   ├── views.py               # Chat API, dashboard, preview system
│   ├── clippy_assistant.py    # AI conversation engine with GPT-4
│   ├── templates/             # Split-screen chat interface
│   └── management/commands/   # Template screenshot management
├── ai_assistant/              # Core AI integration (MagicAI)
├── tenants/                   # Multi-tenant architecture
├── static/                    # Static assets and styling
├── templates/                 # Django templates
├── media/                     # File uploads and template screenshots
│   └── website_templates/
│       ├── previews/          # Template preview images (800x600)
│       └── thumbnails/        # Template thumbnails (400x300)
└── requirements.txt           # Production dependencies
```

## ⚡ **Quick Start**

### 1. **Clone and Setup**
```bash
git clone https://github.com/joaomcorreia/justcodeworkseu.git
cd justcodeworkseu
pip install -r requirements.txt
```

### 2. **Environment Setup**
```bash
# Create .env file with:
SECRET_KEY=your-secret-key
DEBUG=True
OPENAI_API_KEY=your-openai-key
```

### 3. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py create_single_template
```

### 4. **Generate Template Screenshots**
```bash
pip install Pillow
python generate_template_screenshots.py
```

### 5. **Run Development Server**
```bash
python manage.py runserver
```

## 🎮 **Access Points**

- **Main Platform**: http://127.0.0.1:8000/
- **Website Builder**: http://127.0.0.1:8000/website-builder/
- **Admin Dashboard**: http://127.0.0.1:8000/admin/
- **Django Admin**: http://127.0.0.1:8000/django-admin/

## 🛠️ **Key Management Commands**

### **Template Screenshot Management**
```bash
# Add screenshots to existing templates
python manage.py add_template_screenshots --template-id professional_universal_v1 --preview screenshot.jpg --thumbnail thumb.jpg

# Generate placeholder screenshots for all templates
python generate_template_screenshots.py

# View template screenshot status
python manage.py shell -c "
from website_builder.models import WebsiteTemplate;
for t in WebsiteTemplate.objects.all():
    preview = '✅' if t.preview_image else '❌'
    thumbnail = '✅' if t.thumbnail_image else '❌'
    print(f'{t.template_id}: {t.name} - Preview: {preview} Thumbnail: {thumbnail}')
"
```

### **Template Management**
```bash
# Create new single template
python manage.py create_single_template

# Add template preview URLs
python manage.py add_template_previews
```

## 🔧 **Core Features**

### **AI Website Builder**
- ✅ Conversational AI using GPT-4
- ✅ Real-time split-screen preview
- ✅ Smart business industry detection
- ✅ Service suggestion system
- ✅ Multi-step conversation flow
- ✅ Template selection with screenshots

### **Template System**
- ✅ Professional responsive templates
- ✅ Visual template selection interface
- ✅ Screenshot management system
- ✅ Color scheme and font customization
- ✅ Template preview generation

### **Multi-Tenant Architecture**
- ✅ Subdomain-based tenant routing
- ✅ Isolated tenant data
- ✅ Shared public schema
- ✅ Tenant-specific websites

### **Professional Admin**
- ✅ 5-star rated admin dashboard
- ✅ Client project management
- ✅ Website builder integration
- ✅ Real-time preview system

## 📁 **Template Screenshots System**

The platform includes a comprehensive template screenshots system:

### **Directory Structure**
```
media/website_templates/
├── previews/          # Full-size screenshots (800x600)
└── thumbnails/        # Thumbnail images (400x300)
```

### **Management Tools**
- **Automatic generation**: Creates professional placeholder screenshots
- **Manual upload**: Management commands for custom screenshots
- **Visual integration**: Screenshots display in template selection
- **Fallback system**: Uses stock images if screenshots unavailable

See `TEMPLATE_SCREENSHOTS.md` for complete documentation.

## 🚀 **Production Deployment**

The platform is production-ready with:

- ✅ **CSRF protection** on all forms
- ✅ **Environment-based configuration**
- ✅ **Static/media file handling**
- ✅ **Database migrations**
- ✅ **Error handling and logging**
- ✅ **Multi-tenant support**

### **Infrastructure**
- **Production Server**: 46.202.152.237
- **Legacy PHP Server**: 31.97.36.47 (migration in progress)
- **Domain**: justcodeworks.eu
- **Client Subdomains**: customer.justcodeworks.eu

## 💡 **The Perfect Solution for European SMEs**

> *"From the government meeting success to new customer acquisition - this platform delivers professional websites that make businesses and customers happy!"*

**Mission Accomplished!** 🎯

- **Government Demo**: ✅ Success!
- **Customer Acquisition**: ✅ Professional platform ready!
- **AI Integration**: ✅ Clippy 2.0 with real-time preview!
- **Template System**: ✅ Visual selection with screenshots!
- **Happy Customers**: ✅ Tools to deliver quality service!

---

**Your hybrid platform is LIVE and ready for European business growth! 🇪🇺🚀**

## 📞 **Contact & Support**

For platform support and business inquiries:
- **Email**: info@justcodeworks.eu
- **Platform**: justcodeworks.eu
- **GitHub**: github.com/joaomcorreia/justcodeworkseu

## 📄 **License**

This project is proprietary software for the JustCodeWorks.EU platform.
© 2025 JustCodeWorks.EU - European SME Digital Transformation Platform