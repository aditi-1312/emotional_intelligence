# 🚀 Deployment Guide

This guide will help you deploy the Emotional Intelligence Mood Tracker to various platforms.

## 📋 Prerequisites

Before deploying, ensure you have:

- Python 3.8+ installed
- Node.js 14+ installed
- Git installed
- Required API keys (OpenAI for AI insights)

## 🔧 Local Development Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd emotional_intelligence
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp config.env.example config.env
# Edit config.env with your API keys

# Initialize database (optional - will be created automatically)
python -c "from api import app; app.app_context().push()"
```

### 3. Frontend Setup

```bash
# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### 4. Start Development Servers

```bash
# Terminal 1: Start backend
PORT=5001 python3 api.py

# Terminal 2: Start frontend
cd frontend
npm start
```

## 🌐 Production Deployment

### Option 1: Traditional Server Deployment

#### Backend Deployment

1. **Prepare the server**:
```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip nginx

# Create application directory
sudo mkdir -p /var/www/emotional-intelligence
sudo chown $USER:$USER /var/www/emotional-intelligence
```

2. **Deploy the application**:
```bash
# Copy files to server
scp -r . user@your-server:/var/www/emotional-intelligence/

# SSH into server
ssh user@your-server
cd /var/www/emotional-intelligence

# Install dependencies
pip3 install -r requirements.txt
pip3 install gunicorn

# Set environment variables
export FLASK_ENV=production
export PORT=5001
```

3. **Create systemd service**:
```bash
sudo nano /etc/systemd/system/emotional-intelligence.service
```

Add the following content:
```ini
[Unit]
Description=Emotional Intelligence API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/emotional-intelligence
Environment="PATH=/var/www/emotional-intelligence/venv/bin"
ExecStart=/var/www/emotional-intelligence/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5001 api:app
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Start the service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable emotional-intelligence
sudo systemctl start emotional-intelligence
```

#### Frontend Deployment

1. **Build the frontend**:
```bash
cd frontend
npm run build
```

2. **Configure Nginx**:
```bash
sudo nano /etc/nginx/sites-available/emotional-intelligence
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/emotional-intelligence/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:5001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **Enable the site**:
```bash
sudo ln -s /etc/nginx/sites-available/emotional-intelligence /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Docker Deployment

1. **Build and run with Docker Compose**:
```bash
# Build and start services
docker-compose up --build -d

# View logs
docker-compose logs -f
```

2. **Update frontend API URL**:
Edit `frontend/src/services/api.ts` to point to your production API URL.

### Option 3: Cloud Platform Deployment

#### Heroku Deployment

1. **Create Heroku app**:
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create your-app-name
```

2. **Configure environment variables**:
```bash
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set FLASK_ENV=production
```

3. **Deploy backend**:
```bash
# Add Heroku buildpack for Python
heroku buildpacks:add heroku/python

# Deploy
git push heroku main
```

4. **Deploy frontend**:
```bash
# Add Heroku buildpack for Node.js
heroku buildpacks:add heroku/nodejs

# Build frontend
cd frontend
npm run build
cd ..

# Deploy
git add .
git commit -m "Add frontend build"
git push heroku main
```

#### Vercel Deployment (Frontend)

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Deploy frontend**:
```bash
cd frontend
vercel
```

3. **Configure environment variables** in Vercel dashboard:
- `REACT_APP_API_URL`: Your backend API URL

#### Railway Deployment

1. **Connect your GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard
3. **Deploy automatically** on push to main branch

## 🔐 Security Configuration

### 1. Environment Variables

Create a `.env` file for production:
```env
FLASK_ENV=production
FLASK_SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=sqlite:///instance/emotional_intelligence.db
CORS_ORIGINS=https://your-domain.com
```

### 2. SSL/HTTPS Setup

#### Let's Encrypt (Free SSL):
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Database Security

For production, consider using PostgreSQL:
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb emotional_intelligence
sudo -u postgres createuser emotional_user

# Update DATABASE_URL
DATABASE_URL=postgresql://emotional_user:password@localhost/emotional_intelligence
```

## 📊 Monitoring and Logging

### 1. Application Logs

Configure logging in `api.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/emotional_intelligence.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Emotional Intelligence startup')
```

### 2. Health Checks

The API includes health check endpoints:
```bash
# Health check
curl https://your-domain.com/health

# API status
curl https://your-domain.com/api/health
```

### 3. Performance Monitoring

Consider adding monitoring tools:
- **Prometheus + Grafana**: For metrics and visualization
- **Sentry**: For error tracking
- **Uptime Robot**: For uptime monitoring

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Deploy to server
      run: |
        # Add your deployment commands here
        echo "Deploying to production..."
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
# Find process using port
sudo lsof -i :5001

# Kill process
sudo kill -9 <PID>
```

2. **Database connection issues**:
```bash
# Check database file permissions
ls -la instance/
chmod 644 instance/emotional_intelligence.db
```

3. **CORS errors**:
```bash
# Update CORS configuration in api.py
CORS(app, origins=['https://your-domain.com'])
```

4. **Frontend build issues**:
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Performance Optimization

1. **Enable Gzip compression** in Nginx:
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

2. **Add caching headers**:
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **Database optimization**:
```sql
-- Add indexes for better performance
CREATE INDEX idx_journal_user_date ON journal(user_id, created_at);
CREATE INDEX idx_journal_emotion ON journal(dominant_emotion);
```

## 📞 Support

For deployment issues:
1. Check the logs: `docker-compose logs` or `journalctl -u emotional-intelligence`
2. Verify environment variables are set correctly
3. Ensure all dependencies are installed
4. Check firewall and network configuration

## 🔄 Updates and Maintenance

### Regular Maintenance Tasks

1. **Update dependencies**:
```bash
# Python dependencies
pip install --upgrade -r requirements.txt

# Node.js dependencies
cd frontend
npm update
```

2. **Database backups**:
```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp instance/emotional_intelligence.db backups/backup_$DATE.db
```

3. **Log rotation**:
```bash
# Configure logrotate
sudo nano /etc/logrotate.d/emotional-intelligence
```

Add:
```
/var/www/emotional-intelligence/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
```

---

**Happy Deploying! 🚀** 