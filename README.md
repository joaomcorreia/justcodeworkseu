# JustCodeWorks.EU - AI Website Builder

A Django multi-tenant application that allows users to create AI-powered websites with ease.

## Project Structure

```
justcodeworkseu/
├── justcodeworks/          # Main Django project
├── shared/                 # Shared apps (public schema)
├── tenants/               # Tenant management
├── websites/              # Tenant website functionality  
├── templates/             # HTML templates
│   ├── admin/            # Admin interface templates
│   ├── main_site/        # Main site templates
│   └── website/          # Tenant website templates
├── static/               # Static files
├── media/                # User uploaded files
└── requirements.txt      # Python dependencies
```

## Features

### Multi-Tenant Architecture
- Each user gets their own isolated website space
- Subdomain-based tenant separation
- Shared admin interface for all tenants

### Admin Interface
- Unified sidebar navigation for all tenant backends
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