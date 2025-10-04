# 🚀 JustCodeWorks.EU - European SME Digital Transformation Platform

**Government Grant Demo Ready** | **Live Clients** | **Production Deployment**

A comprehensive Django platform combining **automated SaaS website creation** with **professional custom development services** for European SMEs.

## 🎯 **Business Model Overview**

### **Two-Tier Service Strategy:**

#### 🤖 **Automated SaaS Platform** 
- Self-service website creation flow
- Multi-tenant subdomain architecture  
- Instant template deployment
- **Revenue**: €29-99/month subscriptions

#### 🏢 **Professional Custom Development**
- Direct client management system
- Custom Django applications  
- Premium website development
- **Revenue**: €500-2000/project

## 📊 **Current Status (October 2025)**

### **Live Client Portfolio:**
- ✅ **HMD Klusbedrijf** (hmdklusbedrijf.nl) - Converting to Django
- ✅ **Taxi Pro Service** (taxiproservice.nl) - 90% Django Ready  
- ✅ **AutoFix Garage** (autofixgarage.nl) - Migration Pipeline
- ✅ **Oficina Paulo** (oficinapaulocalibra.pt) - E-commerce Expansion

### **Government Meeting Demo:** October 7, 2025

## 🏗️ **Technical Architecture**

```
justcodeworkseu/
├── justcodeworks/          # Main Django project + settings
├── shared/                 # Shared apps (public schema)
├── tenants/               # Multi-tenant management
├── websites/              # Tenant website functionality + signup flow
├── templates/             # Professional templates system
│   ├── admin/            # Unified admin interface
│   ├── main_site/        # Landing page + signup
│   └── website/          # TP1 (Tech) + TP2 (Construction) templates
├── static/               # Assets + professional styling
├── media/                # Client uploads
└── requirements.txt      # Production dependencies
```

## ✨ **Platform Capabilities**

### **Automated SaaS Features:**
- ✅ Complete signup flow (Business Info → Domain → Template → Live Site)
- ✅ Multi-tenant subdomain system
- ✅ Professional template library (TP1, TP2)  
- ✅ Customer admin dashboard
- ✅ CSRF-protected form handling

### **Professional Services Features:**
- ✅ Custom client website development
- ✅ Integrated admin dashboard management
- ✅ Real-time content management
- ✅ Client project tracking
- ✅ Revenue management system

### **Technical Infrastructure:**
- ✅ Django 5.2.7 with multi-tenant architecture
- ✅ Bootstrap-based responsive templates
- ✅ Production-ready deployment system
- ✅ Zero-downtime migration capabilities
- Dashboard with website statistics
- Content management system
- SEO settings
- Analytics integration
- AI-powered features

### Website Management
- Homepage editor with rich text editing
- Page management system
- Slider and carousel components
- About page configuration
- Contact forms
- Responsive design templates

### AI Features
- Content generation assistance
- Design recommendations
- SEO optimization suggestions

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database**
   - Install PostgreSQL
   - Create database: `justcodeworks_db`
   - Update database settings in `settings.py` if needed

3. **Run Migrations**
   ```bash
   python manage.py migrate_schemas --shared
   python manage.py migrate_schemas
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Create Example Tenant**
   ```bash
   python manage.py shell
   ```
   ```python
   from tenants.models import Tenant, Domain
   from django.contrib.auth.models import User
   
   # Create user
   user = User.objects.create_user('demo', 'demo@example.com', 'demo123')
   
   # Create tenant
   tenant = Tenant.objects.create(
       schema_name='demo',
       name='Demo Website',
       company_name='Demo Company'
   )
   
   # Create domain
   Domain.objects.create(
       domain='demo.localhost:8000',
       tenant=tenant,
       is_primary=True
   )
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Main site: http://localhost:8000
   - Admin: http://localhost:8000/admin/
   - Tenant admin: http://demo.localhost:8000/tenant-admin/
   - Website preview: http://demo.localhost:8000/tenant-admin/preview/

## Development

### Adding New Features

1. **For Shared Features**: Add to `shared/` app
2. **For Tenant Features**: Add to `websites/` app
3. **Update Templates**: Add corresponding templates in `templates/`
4. **Update Sidebar**: Modify `templates/admin/sidebar.html`

### Database Schema

- **Public Schema**: Contains tenant management and shared data
- **Tenant Schemas**: Each tenant has isolated data (websites, pages, etc.)

### Key URLs

- `/admin/` - Django admin
- `/tenant-admin/` - Tenant admin interface
- `/` - Main justcodeworks.eu site

## Deployment

For production deployment:

1. Set `DEBUG = False`
2. Configure proper PostgreSQL database
3. Set up domain/subdomain routing
4. Configure static file serving
5. Set up SSL certificates
6. Configure environment variables

## License

This project is proprietary software for JustCodeWorks.EU platform.