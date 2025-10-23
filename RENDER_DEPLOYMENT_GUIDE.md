# MedVault Backend - Complete Render Deployment Guide

## 🎯 Prerequisites Checklist ✅
- ✅ Django backend pushed to GitHub: https://github.com/omkarreddy652/medvault-backend.git
- ✅ `build.sh` file created for Render deployment
- ✅ `requirements.txt` with all dependencies
- ✅ Production-ready `settings.py` configured
- ✅ `.gitignore` preventing sensitive files from being uploaded

---

## Step 1: Create PostgreSQL Database on Render

### 1.1 Sign Up / Log In to Render
1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"** or **"Sign In"**
3. Sign up with GitHub (recommended) or email
4. Verify your email if prompted

### 1.2 Create PostgreSQL Database
1. After logging in, you'll see the Render Dashboard
2. Click the **"New +"** button (top right)
3. Select **"PostgreSQL"** from the dropdown menu

### 1.3 Configure Database Settings
Fill in these **exact** settings:

**Basic Information:**
- **Name**: `medvault-database`
- **Database**: `medvault_db` (database name inside PostgreSQL)
- **User**: `medvault_user` (will be auto-generated)
- **Region**: `Singapore` (choose closest to your users)

**Plan:**
- **Plan Type**: ✅ **Free** (perfect for development/testing)
- **PostgreSQL Version**: `15` (latest stable)

### 1.4 Create the Database
1. Click **"Create Database"**
2. Wait 2-3 minutes for setup to complete
3. You'll be redirected to the database dashboard

### 1.5 Get Database Connection URLs ⚠️ IMPORTANT
Once your database is ready, you'll see connection information:

**Copy the "Internal Database URL"** (this is what you need):
```
postgresql://medvault_user:PASSWORD@dpg-xxxxx-internal:5432/medvault_db
```

**Why Internal URL?**
- ✅ Faster connection (stays within Render's network)
- ✅ No external bandwidth usage
- ✅ More secure

**Save this URL** - you'll need it for the Web Service environment variables!

---

## Step 2: Create Web Service

### 2.1 Create New Web Service
1. From Render Dashboard, click **"New +"**
2. Select **"Web Service"**

### 2.2 Connect GitHub Repository
1. Click **"Connect account"** next to GitHub
2. Authorize Render to access your repositories
3. Find and select **"medvault-backend"** from the list
4. Click **"Connect"**

### 2.3 Configure Service Settings
Fill in these **exact** settings:

**Basic Information:**
- **Name**: `medvault-backend`
- **Region**: `Singapore` (same as your database)
- **Branch**: `main`
- **Root Directory**: (leave empty)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn backend.wsgi:application`

**Plan:**
- **Instance Type**: ✅ **Free** (512 MB RAM, shared CPU)

### 2.4 Advanced Settings
**Auto-Deploy**: ✅ **Yes** (automatically deploys when you push to GitHub)

**Don't click "Create Web Service" yet!** - We need to set environment variables first.

---

## Step 3: Configure Environment Variables

### 3.1 Find Environment Section
Before creating the service, scroll down to find the **"Environment Variables"** section.

### 3.2 Add Required Environment Variables
Click **"Add Environment Variable"** for each of these:

#### 🔐 Django Core Variables

**Variable 1: SECRET_KEY**
- **Key**: `SECRET_KEY`
- **Value**: Generate a new secret key by running this command locally:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and paste it here.

**Variable 2: DEBUG**
- **Key**: `DEBUG`  
- **Value**: `False`

**Variable 3: ALLOWED_HOSTS**
- **Key**: `ALLOWED_HOSTS`
- **Value**: `medvault-backend.onrender.com,localhost`
  
*(Replace "medvault-backend" with your actual service name if different)*

#### 🗄️ Database Configuration

**Variable 4: DATABASE_URL**
- **Key**: `DATABASE_URL`
- **Value**: Paste the **Internal Database URL** you copied from Step 1.5
- Example: `postgresql://medvault_user:PASSWORD@dpg-xxxxx-internal:5432/medvault_db`

#### 🌐 CORS Configuration

**Variable 5: CORS_ALLOW_ALL_ORIGINS**
- **Key**: `CORS_ALLOW_ALL_ORIGINS`
- **Value**: `False`

**Variable 6: CORS_ALLOWED_ORIGINS**
- **Key**: `CORS_ALLOWED_ORIGINS`
- **Value**: `https://your-frontend-domain.vercel.app`
  
*(You'll update this later with your actual Vercel URL)*

#### ☁️ Cloudflare R2 Configuration

**Variable 7: CLOUDFLARE_R2_ACCOUNT_ID**
- **Key**: `CLOUDFLARE_R2_ACCOUNT_ID`
- **Value**: `Y71fc1946284d5bf2ff3e0ae69270f2e5`

**Variable 8: CLOUDFLARE_R2_ACCESS_KEY_ID**
- **Key**: `CLOUDFLARE_R2_ACCESS_KEY_ID`
- **Value**: `030c1ce2e4afda6ab9deb5b0ab3bccb2`

**Variable 9: CLOUDFLARE_R2_SECRET_ACCESS_KEY**
- **Key**: `CLOUDFLARE_R2_SECRET_ACCESS_KEY`
- **Value**: `185535bde135f982ab741c99515edd8325e10be2e431fff3688c5ab485c8f515`

**Variable 10: CLOUDFLARE_R2_BUCKET_NAME**
- **Key**: `CLOUDFLARE_R2_BUCKET_NAME`
- **Value**: `medvault-secure-files`

### 3.3 Create the Web Service
After adding all environment variables, click **"Create Web Service"**

---

## Step 4: Monitor Deployment

### 4.1 Watch the Build Process
1. You'll be taken to the service dashboard
2. Click on the **"Logs"** tab to watch deployment
3. The build process will:
   - Install Python dependencies from `requirements.txt`
   - Collect static files
   - Run database migrations

### 4.2 Build Success Indicators
Look for these messages in the logs:
```
✅ "Requirement already satisfied: django..."
✅ "127 static files copied to '/opt/render/project/staticfiles'"
✅ "Operations to perform: Apply all migrations"
✅ "Your service is live 🎉"
```

### 4.3 Common Build Issues & Solutions

**❌ "No module named 'decouple'"**
- Solution: Check that `python-decouple` is in `requirements.txt`

**❌ "relation does not exist"**
- Solution: Database migrations failed. Check DATABASE_URL is correct.

**❌ "Permission denied on build.sh"**
- Solution: The build script isn't executable. This should auto-fix on Render.

### 4.4 Get Your Live URL
Once deployment succeeds, you'll see:
- **Your live backend URL**: `https://medvault-backend.onrender.com`
- Test it by visiting: `https://medvault-backend.onrender.com/api/`

---

## Step 5: Final Step - Update Vercel Frontend

### 5.1 Update Frontend Environment Variable
Now that your backend is live, update your React frontend:

1. Go to [vercel.com](https://vercel.com)
2. Open your frontend project dashboard
3. Go to **Settings** → **Environment Variables**
4. Find `VITE_API_BASE_URL`
5. Update its value to: `https://medvault-backend.onrender.com`
6. **Important**: Remove any trailing slash!

### 5.2 Redeploy Frontend
1. Go to **Deployments** tab in Vercel
2. Click **"Redeploy"** on the latest deployment
3. Or push a new commit to trigger auto-deployment

### 5.3 Update CORS Settings (if needed)
If you have your exact Vercel URL, update the backend CORS:

1. Go back to Render Web Service
2. **Settings** → **Environment Variables**
3. Edit `CORS_ALLOWED_ORIGINS`
4. Set to your exact Vercel URL: `https://your-actual-frontend.vercel.app`
5. Click **"Save Changes"** (this will redeploy automatically)

---

## 🚀 Deployment Complete!

### Your Live Services:
- **Backend API**: `https://medvault-backend.onrender.com`
- **Database**: PostgreSQL on Render (internal connection)
- **Frontend**: Your Vercel URL (updated to point to new backend)

### Test Your Deployment:
1. **API Health Check**: Visit `https://medvault-backend.onrender.com/api/`
2. **Frontend Connection**: Test login/registration on your frontend
3. **Database**: Try creating a new user account

### Important Notes:
- ⏰ **Free tier sleeps after 15 minutes** of inactivity
- 🔄 **Auto-deploys** when you push to GitHub
- 📊 **750 hours/month** usage limit on free tier
- 🔒 **HTTPS enforced** automatically

---

## 🛠️ Troubleshooting

### Backend Not Responding:
1. Check Render logs for errors
2. Verify all environment variables are set
3. Ensure DATABASE_URL uses "internal" connection

### CORS Errors:
1. Update `CORS_ALLOWED_ORIGINS` with exact frontend URL
2. No trailing slashes in URLs
3. Use HTTPS URLs only

### Database Connection Issues:
1. Verify DATABASE_URL is the "Internal" connection string
2. Check PostgreSQL service is running
3. Ensure database and web service are in same region

### Frontend Can't Connect:
1. Update `VITE_API_BASE_URL` in Vercel
2. Redeploy frontend after environment variable change
3. Check network tab for API call URLs

---

## 🎉 Success!

Your MedVault platform is now fully deployed with:
- ✅ Secure Django REST API backend
- ✅ PostgreSQL database  
- ✅ Cloudflare R2 file storage
- ✅ React frontend on Vercel
- ✅ HTTPS encryption
- ✅ Professional deployment setup

Your medical data platform is ready for users! 🏥✨