# 🚀 Quick Deployment Checklist

## Before You Start ✅
- GitHub repo: https://github.com/omkarreddy652/medvault-backend.git
- Located in: `C:\Users\99230\Documents\medvault-backend`

## 📋 Step-by-Step Checklist

### 1. PostgreSQL Database (5 minutes)
- [ ] Go to [render.com](https://render.com) → New + → PostgreSQL
- [ ] Name: `medvault-database` | Region: Singapore | Plan: Free
- [ ] **COPY the Internal Database URL** (starts with `postgresql://`)

### 2. Web Service (10 minutes)  
- [ ] New + → Web Service → Connect `medvault-backend` repo
- [ ] Name: `medvault-backend` | Region: Singapore
- [ ] Build Command: `./build.sh`
- [ ] Start Command: `gunicorn backend.wsgi:application`

### 3. Environment Variables (5 minutes)
Add these 10 variables:

```
SECRET_KEY = [generate new secret key]
DEBUG = False
ALLOWED_HOSTS = medvault-backend.onrender.com,localhost
DATABASE_URL = [paste Internal Database URL from step 1]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = https://your-frontend.vercel.app
CLOUDFLARE_R2_ACCOUNT_ID = Y71fc1946284d5bf2ff3e0ae69270f2e5
CLOUDFLARE_R2_ACCESS_KEY_ID = 030c1ce2e4afda6ab9deb5b0ab3bccb2
CLOUDFLARE_R2_SECRET_ACCESS_KEY = 185535bde135f982ab741c99515edd8325e10be2e431fff3688c5ab485c8f515
CLOUDFLARE_R2_BUCKET_NAME = medvault-secure-files
```

### 4. Deploy & Test (5 minutes)
- [ ] Click "Create Web Service"
- [ ] Watch logs for "Your service is live 🎉"
- [ ] Test: Visit `https://medvault-backend.onrender.com/api/`

### 5. Update Frontend (2 minutes)
- [ ] Vercel → Settings → Environment Variables
- [ ] Update `VITE_API_BASE_URL` = `https://medvault-backend.onrender.com`
- [ ] Redeploy frontend

## 🎯 Total Time: ~25 minutes

## 🔗 Key URLs
- **Render Dashboard**: https://dashboard.render.com
- **Your Backend**: https://medvault-backend.onrender.com
- **GitHub Repo**: https://github.com/omkarreddy652/medvault-backend.git

## 🆘 Quick Fixes
- **Build fails**: Check `requirements.txt` has all packages
- **Can't connect to DB**: Use Internal Database URL, not External
- **CORS errors**: Update `CORS_ALLOWED_ORIGINS` with exact frontend URL
- **Frontend errors**: Update `VITE_API_BASE_URL` in Vercel and redeploy

## 🎉 Success Indicators
- ✅ Render logs show "Your service is live"
- ✅ API responds at `/api/` endpoint  
- ✅ Frontend can register/login users
- ✅ No CORS errors in browser console

Ready to deploy! 🚀