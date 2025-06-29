# 🚀 Deployment Guide - Emotional Intelligence Mood Tracker

## 🌐 Live Website Deployment Options

### **Option 1: Vercel + Railway (Recommended)**

#### **Frontend Deployment on Vercel**

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub
   - Click "New Project"
   - Import your repository
   - Set root directory to `frontend`
   - Deploy

3. **Configure Environment Variables**
   - Add `REACT_APP_API_URL=https://your-backend-url.railway.app`

#### **Backend Deployment on Railway**

1. **Deploy Backend**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project"
   - Import your repository
   - Set root directory to `backend`

2. **Add Environment Variables**
   ```
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   FLASK_SECRET_KEY=your_secret_key
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Update Google OAuth Redirect URIs**
   - Add your Railway backend URL to Google Console
   - Format: `https://your-app.railway.app/auth/callback`

### **Option 2: Netlify + Render**

#### **Frontend on Netlify**
1. Go to [netlify.com](https://netlify.com)
2. Connect GitHub repository
3. Set build command: `cd frontend && npm run build`
4. Set publish directory: `frontend/build`

#### **Backend on Render**
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set root directory to `backend`
5. Add environment variables

### **Option 3: Full Stack on Railway**

1. **Deploy Both Services**
   - Create two services in Railway
   - Frontend service: root directory `frontend`
   - Backend service: root directory `backend`

2. **Configure Communication**
   - Set `REACT_APP_API_URL` in frontend environment variables
   - Point to your backend service URL

## 🔧 Required Configuration Changes

### **Update Frontend API URL**

In `frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';
```

### **Update Backend CORS**

In `backend/api.py`:
```python
CORS(app, supports_credentials=True, origins=[
    "http://localhost:3000",
    "https://your-frontend-domain.vercel.app",
    "https://your-frontend-domain.netlify.app"
])
```

### **Update Google OAuth Redirect URIs**

In Google Cloud Console, add your production URLs:
- `https://your-backend-domain.railway.app/auth/callback`
- `https://your-backend-domain.render.com/auth/callback`

## 🌍 Domain Setup

### **Custom Domain (Optional)**
1. **Vercel**: Add custom domain in project settings
2. **Railway**: Use Railway's provided domain or add custom domain
3. **Update Google OAuth**: Add custom domain to redirect URIs

### **SSL/HTTPS**
- Vercel: Automatic SSL
- Railway: Automatic SSL
- Netlify: Automatic SSL
- Render: Automatic SSL

## 📊 Database Setup

### **SQLite (Development)**
- Works locally
- Not recommended for production

### **PostgreSQL (Production)**
1. **Railway**: Add PostgreSQL service
2. **Render**: Add PostgreSQL service
3. **Update DATABASE_URL** in environment variables

## 🔍 Testing Your Deployment

### **Health Check**
```bash
curl https://your-backend-domain.railway.app/health
```

### **OAuth Flow**
1. Visit your frontend URL
2. Click "Sign in with Google"
3. Complete OAuth flow
4. Verify redirect works

### **API Testing**
```bash
# Test journal endpoint
curl -X POST https://your-backend-domain.railway.app/journal \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling happy today!"}'
```

## 🚨 Common Issues & Solutions

### **CORS Errors**
- Ensure CORS origins include your frontend domain
- Check that credentials are properly configured

### **OAuth Redirect Errors**
- Verify redirect URI matches exactly in Google Console
- Check that HTTPS is used in production

### **Database Connection Issues**
- Ensure DATABASE_URL is set correctly
- For PostgreSQL, install `psycopg2-binary` in requirements.txt

### **Build Failures**
- Check that all dependencies are in requirements.txt
- Verify Python version compatibility

## 📈 Monitoring & Analytics

### **Vercel Analytics**
- Built-in analytics for frontend
- Performance monitoring

### **Railway Metrics**
- CPU and memory usage
- Request logs

### **Custom Monitoring**
- Add logging to Flask app
- Monitor API response times

## 🔄 Continuous Deployment

### **Automatic Deployments**
- Push to GitHub main branch
- Automatic deployment to Vercel/Railway
- No manual intervention needed

### **Environment Management**
- Use different environment variables for dev/prod
- Keep sensitive data in deployment platform settings

## 💰 Cost Estimation

### **Free Tier Limits**
- **Vercel**: 100GB bandwidth/month
- **Railway**: $5 credit/month
- **Netlify**: 100GB bandwidth/month
- **Render**: 750 hours/month

### **Scaling Up**
- Upgrade plans available on all platforms
- Pay-as-you-go pricing

## 🎯 Final Steps

1. **Test Everything**
   - OAuth login
   - Journal entries
   - Analytics dashboard
   - Data clearing

2. **Update Documentation**
   - Add live URL to README
   - Update setup instructions

3. **Monitor Performance**
   - Check response times
   - Monitor error rates
   - Track user engagement

## 🌟 Your Live Website

Once deployed, your Emotional Intelligence Mood Tracker will be available at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.railway.app`

Share your live URL and start helping people track their emotional well-being! 🎉 