# JustCodeWorks.EU - Server Deployment Guide

## 🚀 **Quick Server Setup**

### **1. Prepare Your Server**
```bash
# Upload project to server
scp -r justcodeworkseu/ user@yourserver.com:/var/www/

# SSH into server
ssh user@yourserver.com

# Make deploy script executable
chmod +x /var/www/justcodeworkseu/deploy.sh

# Run deployment (this will install everything)
sudo /var/www/justcodeworkseu/deploy.sh
```

### **2. Configure Environment**
Edit the `.env` file on your server:
```bash
nano /var/www/justcodeworkseu/.env
```

**Required settings:**
```
SECRET_KEY=your-super-secret-key-generate-new-one
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,*.yourdomain.com

DB_NAME=justcodeworks_prod
DB_USER=justcodeworks  
DB_PASSWORD=secure-database-password
DB_HOST=localhost
DB_PORT=5432

SECURE_SSL_REDIRECT=True
```

### **3. Update Domain Configuration**
Edit Nginx config:
```bash
sudo nano /etc/nginx/sites-available/justcodeworks
```

Replace `yourdomain.com` with your actual domain.

### **4. SSL Certificate (Recommended)**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### **5. Test Everything**
```bash
# Check services
sudo systemctl status justcodeworks
sudo systemctl status nginx

# View logs
sudo journalctl -u justcodeworks -f
tail -f /var/www/justcodeworkseu/logs/django.log
```

## 🌐 **URLs After Deployment**

- **Coming Soon Page**: https://yourdomain.com/
- **Admin Panel**: https://yourdomain.com/admin5689/
- **Tenant Admin**: https://yourdomain.com/tenant-admin/

## 📋 **Production Checklist**

### **Before Going Live:**
- [ ] Update `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up database with strong password
- [ ] Configure email settings for notifications
- [ ] Set up SSL certificate
- [ ] Test all admin functionality
- [ ] Create initial tenant/user accounts
- [ ] Test coming soon page for visitors

### **Security:**
- [ ] Admin URL changed to `/admin5689/`
- [ ] Strong database passwords
- [ ] SSL/HTTPS enabled
- [ ] Regular backups scheduled
- [ ] Server firewall configured

### **Monitoring:**
- [ ] Log rotation set up
- [ ] Server monitoring (CPU, RAM, disk)
- [ ] Application uptime monitoring
- [ ] Database backup strategy

## 🔄 **Updates & Maintenance**

### **To Update the Application:**
```bash
cd /var/www/justcodeworkseu
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput --settings=justcodeworks.settings_prod
python manage.py migrate_schemas --settings=justcodeworks.settings_prod
sudo systemctl restart justcodeworks
```

### **Database Backup:**
```bash
# Create backup
pg_dump justcodeworks_prod > backup_$(date +%Y%m%d).sql

# Restore backup
psql justcodeworks_prod < backup_20251002.sql
```

## 🆘 **Troubleshooting**

### **Common Issues:**

**502 Bad Gateway:**
- Check Gunicorn service: `sudo systemctl status justcodeworks`
- Check logs: `sudo journalctl -u justcodeworks -f`

**Static Files Not Loading:**
- Run: `python manage.py collectstatic --settings=justcodeworks.settings_prod`
- Check Nginx permissions

**Database Connection Error:**
- Verify `.env` database settings
- Check PostgreSQL service: `sudo systemctl status postgresql`

**Coming Soon Page Not Showing:**
- Check that users are not authenticated
- Verify URL routing in `urls.py`

## 📞 **Support**

For deployment issues:
1. Check logs: `/var/www/justcodeworkseu/logs/django.log`
2. Check service status: `sudo systemctl status justcodeworks`
3. Check Nginx: `sudo nginx -t`

## 🎯 **Current Features Ready for Production**

✅ Coming soon page with countdown
✅ Secure admin panel at `/admin5689/`
✅ Full tenant admin interface  
✅ Website preview functionality
✅ User authentication system
✅ Database models for multi-tenancy
✅ Responsive design
✅ SEO optimization
✅ Security middleware

Ready to deploy and start testing! 🚀