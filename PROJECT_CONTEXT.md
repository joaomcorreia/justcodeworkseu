# JustCodeWorks.EU - Project Context & Documentation

## Project Overview
**Multi-tenant SaaS platform for AI-powered website creation with integrated business services**

### Core Architecture
- **Framework**: Django 5.2.7 with django-tenants 3.9.0
- **Database**: PostgreSQL with multi-tenant schemas
- **Deployment**: Ubuntu server with Nginx + Gunicorn
- **Repository**: https://github.com/joaomcorreia/justcodeworkseu

### Business Model

#### Main Platform (justcodeworks.eu)
1. **Type 1 Websites**: Users sign up and build AI-generated websites
   - User registration → Company details → Domain selection → Payment → Auto-deployment
   - Recurring revenue: $30-200/month per customer
   
2. **Type 2 Websites**: Custom client websites (manually built)
   - White-label solution with centralized management
   - Shared admin dashboards with custom sidebar
   - Updates pushed from main dashboard to all client sites

#### Additional Revenue Streams
- Domain registration markup
- Print materials reselling (via APIs: Printful, Vistaprint, Gooten)
- Premium services (SEO, custom design)

### Technical Implementation

#### Multi-Tenant Structure
```
justcodeworks.eu (Public Schema)
├── Master admin dashboard
├── Global templates & sidebar
├── Tenant management
└── Centralized updates

client1.com, client2.com, etc. (Tenant Schemas)
├── Shared admin interface
├── Client-specific data
├── Receives global updates
└── Custom domain mapping
```

#### Current Status (October 2025)
- ✅ Django project structure complete
- ✅ Multi-tenant configuration ready
- ✅ Admin interface with custom sidebar
- ✅ GitHub repository up to date
- 🔄 **NEXT**: Clean deployment to production server

### Server Configuration

#### Hostinger Ubuntu Server
- **IP**: 46.202.152.237
- **Domain**: justcodeworks.eu
- **User**: justcodeworks / www-data
- **Database**: PostgreSQL (justcodeworks_db, user: justcodeworks, pass: justcodeworks123)

#### Required Services
- Nginx (reverse proxy + SSL)
- Gunicorn (WSGI server)
- PostgreSQL (database)
- Systemd service (justcodeworks.service)

### Deployment Plan

#### Phase 1: Foundation (Target: 45 minutes)
1. Clean slate server setup
2. Fresh GitHub clone
3. Python environment & dependencies
4. Database configuration & migrations
5. Nginx + SSL configuration
6. Systemd service setup

#### Phase 2: Client Sites (20 minutes each)
1. Add domains to tenant configuration
2. DNS setup
3. SSL certificates
4. Test & verify

#### Phase 3: Automation Features
- User registration system
- Automatic domain registration
- Payment integration (Stripe)
- AI website generation
- Print API integration

### Related Projects

#### EU Directory Project
- **Type**: Django-based business directory
- **Features**: AI-generated simple websites (mostly single page)
- **Target**: European businesses
- **Architecture**: Similar multi-tenant approach

### Key Files & Locations

#### Django Settings
- `justcodeworks/settings.py` - Main configuration
- `justcodeworks/settings_prod.py` - Production settings
- `justcodeworks/settings_dev.py` - Development settings
- `justcodeworks/urls.py` - URL routing (uses /admin/)

#### Templates
- `templates/admin/base_with_sidebar.html` - Shared admin layout
- `templates/admin/sidebar.html` - Global sidebar for all tenants
- `templates/main_site/` - Landing page templates

#### Apps
- `tenants/` - Tenant management
- `websites/` - Website builder functionality
- `shared/` - Shared utilities

### Development Workflow

#### Local Development
```bash
cd c:\projects\justcodeworkseu
.venv\Scripts\activate
python manage.py runserver --settings=justcodeworks.settings_dev
```

#### Production Deployment
```bash
cd /var/www/justcodeworks/justcodeworkseu
git pull origin main
sudo systemctl restart justcodeworks
sudo systemctl reload nginx
```

### Common Issues & Solutions

#### Database Connection
- Ensure PostgreSQL user has proper permissions
- Check DATABASES configuration in settings
- Verify database exists: `sudo -u postgres psql -l`

#### Multi-Tenant Setup
- Run migrations: `python manage.py migrate`
- Setup schemas: `python manage.py migrate_schemas --shared`
- Create domains in admin panel

#### Nginx Configuration
- Site configs in `/etc/nginx/sites-available/`
- Enable with symlink to `/etc/nginx/sites-enabled/`
- Test config: `sudo nginx -t`

### Future Development Priorities

1. **User Registration System**
   - Signup flow with company details
   - Domain selection interface
   - Payment integration

2. **AI Website Builder**
   - Template system
   - Content generation
   - Customization tools

3. **Print Services Integration**
   - API connections to print providers
   - Product catalog in tenant dashboards
   - Order management system

4. **Analytics & Monitoring**
   - Google Analytics integration
   - Performance tracking
   - Revenue dashboards

### Contact & Repository
- **GitHub**: https://github.com/joaomcorreia/justcodeworkseu
- **Owner**: joaomcorreia
- **Current Branch**: main

---
*Last Updated: October 4, 2025*
*This file should be shared with any developers working on the project*