# JustCodeWorks.EU - Project Context & Documentation

## Project Overview
**Multi-tenant SaaS platform for AI-powered website creation with integrated business services**

### **Current Business Context (October 2025)**
- **Government Business Grant Application**: Demo needed for upcoming government agency interviews
- **Launch Timeline**: December 2025 - January 2026 (8-10 weeks)
- **Immediate Priority**: Working demo to showcase business model and technical capability
- **Customer Base**: Initially 2-3 manual clients with basic editing needs (no self-serve yet)
- **MVP Focus**: Demonstrate multi-tenant architecture and admin management capabilities

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
- ✅ Comprehensive security requirements documented
- 🔄 **NEXT**: Deploy working demo for government business grant interviews

#### Demo Requirements (Government Grant Application)
- **Immediate Goal**: Working demo within 1-2 days for agency interviews
- **Showcase Features**: Multi-tenant admin, client website management, scalable architecture
- **Client Management**: Static admin pages with basic content editing (prices, contacts, images)
- **Security Level**: Basic but visible security measures (SSL, privacy policy, secure admin)
- **Future Vision**: Full automation and AI features (for business plan presentation)

#### Security Implementation Status
- 🔄 **Phase 1**: Secure foundation deployment (in progress)
- ⏳ **Phase 2**: 2FA and monitoring setup (planned)
- ⏳ **Phase 3**: Full GDPR compliance tools (planned)
- ⏳ **Phase 4**: Advanced security features (planned)

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

### Security & Trust Messaging

#### **Public Security Commitments**
- **EU GDPR Compliant**: Full compliance with European data protection regulations
- **Enterprise-Grade Security**: Bank-level encryption and security measures  
- **Zero Data Sharing**: Your data is never sold, shared, or used for advertising
- **Transparent Privacy**: Clear, understandable privacy policies in plain language
- **Regular Security Audits**: Independent third-party security assessments
- **Data Sovereignty**: EU data stays in EU servers (data residency compliance)

#### **Trust Indicators to Display**
- 🔒 **SSL Certificate Badge** (visible on all pages)
- 🛡️ **GDPR Compliance Seal** (official certification)  
- ⚡ **99.9% Uptime Guarantee** (with SLA)
- 🔐 **SOC 2 Type II** (security audit certification - future goal)
- 🏆 **ISO 27001** (information security standard - future goal)
- 📊 **Transparent Security Report** (annual public security summary)

#### **User-Facing Security Features**
- Two-factor authentication available for all accounts
- Real-time security notifications for suspicious activity
- Automatic security updates with zero downtime
- Encrypted backups with instant recovery options
- Personal data export tools (GDPR right to portability)
- One-click data deletion (GDPR right to be forgotten)

#### **Marketing Messages**
- *"Built with privacy by design - your data is protected from day one"*
- *"EU-based, EU-compliant - your data never leaves European servers"*  
- *"Enterprise security for everyone - no matter your business size"*
- *"Transparent security - see exactly how we protect your information"*
- *"Privacy-first platform - we make money from subscriptions, not your data"*

### Related Projects

#### EU Directory Project
- **Type**: Django-based business directory
- **Features**: AI-generated simple websites (mostly single page)
- **Target**: European businesses
- **Architecture**: Similar multi-tenant approach
- **Security**: Same enterprise-grade security standards

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

### Security & Compliance Requirements

#### **EU/GDPR Compliance (Mandatory)**
- Data Protection Officer (DPO) contact information
- Privacy Policy & Cookie Consent system
- Right to be forgotten (automated data deletion)
- Data breach notification system (72h requirement)
- Explicit consent management for data processing
- Data encryption at rest & in transit
- Regular compliance audits and documentation

#### **Multi-Tenant Security Architecture**
- Tenant data isolation (strict schema separation)
- Cross-tenant data leakage prevention
- Per-tenant security headers and CSP policies
- Rate limiting and DDoS protection per tenant
- Comprehensive audit logging for all tenant actions
- Tenant-specific backup and recovery procedures

#### **Authentication & Access Control**
- **2FA mandatory** for all admin accounts (TOTP/Google Authenticator)
- Strong password policies (12+ characters, complexity requirements)
- Session management (secure cookies, timeout policies)
- Role-based permissions (tenant admin vs global admin vs user)
- API key management with rotation capabilities
- OAuth2 integration for third-party services

#### **Infrastructure Security**
- SSL/TLS certificates with auto-renewal (Let's Encrypt)
- Web Application Firewall (WAF) configuration
- SSH key authentication only (password login disabled)
- Automated security updates (unattended-upgrades)
- Encrypted off-site backups with rotation
- Network segmentation and access control

#### **Application Security**
- Django security middleware (XSS, CSRF, clickjacking protection)
- SQL injection prevention (Django ORM exclusively)
- Input validation and sanitization for all user data
- Secure file upload handling with virus scanning
- Environment variable secrets management
- Content Security Policy (CSP) headers
- Regular dependency vulnerability scanning

#### **Monitoring & Incident Response**
- Intrusion detection system (fail2ban + custom rules)
- Centralized logging with log retention policies
- External uptime and performance monitoring
- Automated security scanning and vulnerability assessments
- Incident response plan with breach notification procedures
- Regular penetration testing schedule

### Future Development Priorities

#### **Phase 1: Demo MVP (Days 1-3)**
1. **Working Demo Deployment**
   - Basic secure deployment (SSL, firewall)
   - Multi-tenant admin dashboard working
   - 3 client websites live and manageable
   - Content editing capabilities (prices, contacts, images, forms)
   - Professional appearance for government presentation

#### **Phase 2: Government Presentation Prep (Days 4-7)**
1. **Demo Polish & Documentation**
   - Business plan technical documentation
   - Revenue model demonstration
   - Scalability presentation materials
   - Security and compliance overview
   - Client onboarding process demo

#### **Phase 3: Pre-Launch Development (Weeks 2-8)**
1. **User Registration System**
   - Signup flow with company details
   - Domain selection interface
   - Payment integration with PCI compliance
   - 2FA implementation for all users

2. **Multi-Tenant Management**
   - Automated tenant provisioning
   - Tenant-specific feature toggles
   - Billing and subscription management
   - Audit logging and compliance reporting

#### **Phase 3: AI & Automation (Month 2)**
1. **AI Website Builder**
   - Template system with security validation
   - Content generation with content filtering
   - Customization tools with input sanitization
   - Performance optimization

2. **Integration Services**
   - Print API connections with secure authentication
   - Payment gateway integrations
   - Analytics and tracking (GDPR-compliant)
   - Third-party service management

#### **Phase 4: Advanced Features (Month 3+)**
1. **Advanced Security & Compliance**
   - Advanced threat detection
   - Compliance automation tools
   - Security audit dashboards
   - Automated incident response

2. **Business Intelligence**
   - Revenue analytics and forecasting
   - Customer behavior analysis (privacy-compliant)
   - Performance optimization recommendations
   - Competitive analysis tools

### Contact & Repository
- **GitHub**: https://github.com/joaomcorreia/justcodeworkseu
- **Owner**: joaomcorreia
- **Current Branch**: main

---
*Last Updated: October 4, 2025*
*This file should be shared with any developers working on the project*