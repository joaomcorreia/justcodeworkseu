#!/bin/bash

# Production Deployment Script for JustCodeWorks.EU
# Run this script on your server to deploy the application

echo "🚀 Starting JustCodeWorks.EU deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

# Install Node.js for any frontend tools (optional)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Create application user (optional but recommended)
echo "👤 Creating application user..."
sudo useradd -m -s /bin/bash justcodeworks || true
sudo usermod -aG sudo justcodeworks || true

# Switch to app directory
cd /var/www/justcodeworks || cd /home/justcodeworks

# Clone or update repository
echo "📥 Setting up application code..."
if [ ! -d "justcodeworkseu" ]; then
    git clone https://github.com/joaomcorreia/justcodeworkseu.git
else
    cd justcodeworkseu
    git pull origin main
    cd ..
fi

cd justcodeworkseu

# Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn whitenoise psycopg2-binary

# Set up environment variables
echo "⚙️ Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your production values!"
    echo "⚠️  Don't forget to set SECRET_KEY, DATABASE credentials, etc."
fi

# Create logs directory
mkdir -p logs

# Set up PostgreSQL database
echo "🗄️ Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE justcodeworks_prod;" || true
sudo -u postgres psql -c "CREATE USER justcodeworks WITH ENCRYPTED PASSWORD 'your_password_here';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE justcodeworks_prod TO justcodeworks;" || true
sudo -u postgres psql -c "ALTER USER justcodeworks CREATEDB;" || true

echo "⚠️  Remember to update database password in .env file!"

# Run migrations
echo "🔄 Running database migrations..."
python manage.py collectstatic --noinput --settings=justcodeworks.settings_prod
python manage.py migrate_schemas --shared --settings=justcodeworks.settings_prod
python manage.py migrate_schemas --settings=justcodeworks.settings_prod

# Create superuser (non-interactive)
echo "👑 Create superuser account..."
echo "⚠️  Creating superuser with default credentials. Change password after deployment!"
python manage.py shell --settings=justcodeworks.settings_prod << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@justcodeworks.eu', 'admin123456')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF

# Set up Gunicorn service
echo "🔧 Setting up Gunicorn service..."
sudo tee /etc/systemd/system/justcodeworks.service > /dev/null <<EOF
[Unit]
Description=JustCodeWorks.EU Django Application
After=network.target

[Service]
User=justcodeworks
Group=www-data
WorkingDirectory=/var/www/justcodeworks/justcodeworkseu
Environment="PATH=/var/www/justcodeworks/justcodeworkseu/.venv/bin"
ExecStart=/var/www/justcodeworks/justcodeworkseu/.venv/bin/gunicorn --workers 3 --bind unix:/var/www/justcodeworks/justcodeworkseu/justcodeworks.sock justcodeworks.wsgi:application --settings=justcodeworks.settings_prod
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Set up Nginx configuration
echo "🌐 Setting up Nginx..."
sudo tee /etc/nginx/sites-available/justcodeworks > /dev/null <<EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com *.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/justcodeworks/justcodeworkseu;
    }
    
    location /media/ {
        root /var/www/justcodeworks/justcodeworkseu;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/justcodeworks/justcodeworkseu/justcodeworks.sock;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/justcodeworks /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start and enable services
echo "▶️ Starting services..."
sudo systemctl daemon-reload
sudo systemctl start justcodeworks
sudo systemctl enable justcodeworks
sudo systemctl enable nginx

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R justcodeworks:www-data /var/www/justcodeworks
sudo chmod -R 755 /var/www/justcodeworks

echo "✅ Deployment complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Edit .env file with your production values"
echo "2. Update Nginx configuration with your domain"
echo "3. Set up SSL certificates (Let's Encrypt recommended)"
echo "4. Configure DNS to point to your server"
echo "5. Test the application at your domain"
echo ""
echo "🌐 URLs:"
echo "   Main site: http://yourdomain.com/"
echo "   Admin: http://yourdomain.com/admin5689/"
echo "   Tenant Admin: http://yourdomain.com/tenant-admin/"
echo ""
echo "📝 Important files:"
echo "   Application: /var/www/justcodeworks/justcodeworkseu/"
echo "   Nginx config: /etc/nginx/sites-available/justcodeworks"
echo "   Service: /etc/systemd/system/justcodeworks.service"
echo "   Logs: /var/www/justcodeworks/justcodeworkseu/logs/"