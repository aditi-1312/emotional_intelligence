# 🔐 Google OAuth Setup Guide

This guide will help you set up Google OAuth authentication for your Emotional Intelligence Mood Tracker app.

## 📋 Prerequisites

- A Google account
- Python 3.7+ installed
- Basic understanding of web development

## 🚀 Quick Setup

### 1. Run the Setup Script

```bash
python3 scripts/setup_google_oauth.py
```

This interactive script will guide you through the entire setup process.

### 2. Manual Setup (Alternative)

If you prefer to set up manually, follow these steps:

## 🔧 Step-by-Step Manual Setup

### Step 1: Google Cloud Console Setup

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project**
   - Click on the project dropdown at the top
   - Click "New Project"
   - Name it: "Emotional Intelligence App"
   - Click "Create"

3. **Enable Required APIs**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API"
   - Click "Enable"

### Step 2: Create OAuth Credentials

1. **Navigate to Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"

2. **Configure OAuth Consent Screen**
   - Choose "External" user type
   - Fill in the required information:
     - App name: "Emotional Intelligence App"
     - User support email: Your email
     - Developer contact information: Your email
   - Click "Save and Continue"
   - Skip scopes section, click "Save and Continue"
   - Add test users if needed
   - Click "Save and Continue"

3. **Create OAuth Client ID**
   - Application type: "Web application"
   - Name: "Emotional Intelligence App"
   - Authorized redirect URIs:
     ```
     http://localhost:5001/auth/login/callback
     http://127.0.0.1:5001/auth/login/callback
     ```
   - Click "Create"

4. **Save Your Credentials**
   - Copy the Client ID and Client Secret
   - Keep them secure - you'll need them for the next step

### Step 3: Configure Your App

1. **Create/Update config.env**
   ```bash
   # Copy the template
   cp config.env.example config.env
   ```

2. **Edit config.env**
   ```env
   # Google OAuth Configuration
   GOOGLE_CLIENT_ID=your_actual_client_id_here
   GOOGLE_CLIENT_SECRET=your_actual_client_secret_here
   
   # Flask Configuration
   SECRET_KEY=your_generated_secret_key_here
   FLASK_ENV=development
   
   # OpenAI Configuration (Optional)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Database Configuration
   DATABASE_URL=sqlite:///data_and_models/instance/emotional_intelligence.db
   
   # Server Configuration
   PORT=5001
   HOST=0.0.0.0
   ```

3. **Generate a Secret Key**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output to your `SECRET_KEY` in config.env

## 🔒 Security Best Practices

### Environment Variables
- Never commit `config.env` to version control
- Use environment variables in production
- Keep your Google Client Secret secure

### Production Deployment
- Use HTTPS in production
- Update redirect URIs for your domain
- Set up proper session management
- Use secure cookies

### Regular Maintenance
- Rotate secret keys periodically
- Monitor OAuth usage in Google Cloud Console
- Keep dependencies updated

## 🧪 Testing Your Setup

1. **Start the Backend**
   ```bash
   PORT=5001 python3 backend/api.py
   ```

2. **Start the Frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Test Authentication**
   - Visit http://localhost:3000
   - Click "Sign in with Google"
   - Complete the OAuth flow
   - Verify you're logged in

## 🚨 Troubleshooting

### Common Issues

1. **"redirect_uri_mismatch" Error**
   - Check that your redirect URIs in Google Console match exactly
   - Include both localhost and 127.0.0.1 variants

2. **"invalid_client" Error**
   - Verify your Client ID and Secret are correct
   - Check that you copied them without extra spaces

3. **"access_denied" Error**
   - Make sure you're using the correct Google account
   - Check that the app is not in restricted mode

4. **Session Issues**
   - Clear browser cookies and cache
   - Check that `SECRET_KEY` is set correctly
   - Verify `withCredentials: true` in frontend API calls

### Debug Mode

Enable debug logging in your backend:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Check Logs

Monitor your backend console for detailed error messages and authentication flow logs.

## 📚 Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Google Cloud Console Help](https://cloud.google.com/apis/docs/getting-started)

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review the error logs in your backend console
3. Verify your Google Cloud Console configuration
4. Test with a fresh browser session
5. Check that all dependencies are installed correctly

## ✅ Verification Checklist

- [ ] Google Cloud Console project created
- [ ] Google+ API enabled
- [ ] OAuth 2.0 credentials created
- [ ] Redirect URIs configured correctly
- [ ] config.env file created with credentials
- [ ] SECRET_KEY generated and set
- [ ] Backend starts without errors
- [ ] Frontend connects to backend
- [ ] Google OAuth flow completes successfully
- [ ] User data is stored in database
- [ ] Logout functionality works

Once all items are checked, your Google OAuth setup is complete! 🎉 