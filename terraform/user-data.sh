#!/bin/bash
set -e

# Install Docker and dependencies
dnf update -y
dnf install -y docker git docker-compose-plugin curl
systemctl start docker
systemctl enable docker

# Add ec2-user to docker group
usermod -aG docker ec2-user

# Install Python and pip
dnf install -y python3 python3-pip python3-devel gcc

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Create application directory
mkdir -p /var/www/web-crawler
chown -R ec2-user:ec2-user /var/www/web-crawler

# Clone repository (if public) or use SSH key from Secrets Manager
cd /var/www/web-crawler
git clone https://github.com/naveensaini9521/web-crawler.git . || echo "Repository already exists"

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || pip install flask gunicorn pymysql cryptography

# Create .env file
cat > /var/www/web-crawler/.env << 'EOF'
FLASK_APP=app.py
FLASK_ENV=production
MYSQL_HOST=${DB_HOST}
MYSQL_USERNAME=${DB_USERNAME}
MYSQL_PASSWORD=${DB_PASSWORD}
MYSQL_DATABASE=${DB_NAME}
SECRET_KEY=${SECRET_KEY}
DEBUG=False
EOF

# Set ownership
chown -R ec2-user:ec2-user /var/www/web-crawler

# Create systemd service
cat > /etc/systemd/system/web-crawler.service << 'EOF'
[Unit]
Description=Web Crawler Application
After=network.target docker.service
Requires=docker.service

[Service]
Type=notify
User=ec2-user
Group=ec2-user
WorkingDirectory=/var/www/web-crawler
Environment="PATH=/var/www/web-crawler/venv/bin"
ExecStart=/var/www/web-crawler/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:${APP_PORT} app:app
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable web-crawler
systemctl start web-crawler

# Configure Nginx
dnf install -y nginx
cat > /etc/nginx/conf.d/web-crawler.conf << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:${APP_PORT};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/web-crawler/static;
        expires 30d;
    }

    location /media {
        alias /var/www/web-crawler/media;
        expires 30d;
    }
}
EOF

systemctl enable nginx
systemctl start nginx

echo "Application deployed successfully!"