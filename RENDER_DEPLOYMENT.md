# Render Deployment Guide for Coffee Feedback App

## 🚀 Quick Deployment Steps

### Prerequisites
- GitHub account with your repo: https://github.com/meetmaheshin/coffie-testing.git
- Render account (free): https://render.com
- OpenAI API key

---

## Step 1: Push Code to GitHub

```bash
cd c:\Users\LENOVO\coffie-test
git add .
git commit -m "Add Render deployment config"
git push origin main
```

---

## Step 2: Deploy Backend on Render

1. **Go to Render Dashboard**: https://dashboard.render.com

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repo: `meetmaheshin/coffie-testing`
   - Click "Connect"

3. **Configure Backend Service**:
   - **Name**: `coffee-feedback-api`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

4. **Add Environment Variables**:
   Click "Add Environment Variable" for each:
   
   | Key | Value |
   |-----|-------|
   | `PYTHON_VERSION` | `3.13.0` |
   | `OPENAI_API_KEY` | `your-actual-openai-api-key` |
   | `DATABASE_URL` | `sqlite+aiosqlite:///./coffee_feedback.db` |
   | `CORS_ORIGINS` | `https://your-frontend-url.onrender.com` (add later) |

5. **Click "Create Web Service"** → Wait 3-5 minutes for deployment

6. **Note your backend URL**: 
   - Will be something like: `https://coffee-feedback-api.onrender.com`

---

## Step 3: Deploy Frontend on Render

1. **Create New Static Site**:
   - Click "New +" → "Static Site"
   - Select same GitHub repo
   - Click "Connect"

2. **Configure Frontend Service**:
   - **Name**: `coffee-feedback-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: 
     ```
     npm install && npm run build
     ```
   - **Publish Directory**: `dist`

3. **Add Environment Variable**:
   
   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | `https://coffee-feedback-api.onrender.com` (your backend URL) |

4. **Click "Create Static Site"** → Wait 2-3 minutes

5. **Note your frontend URL**:
   - Will be something like: `https://coffee-feedback-frontend.onrender.com`

---

## Step 4: Update CORS Settings

1. Go back to **Backend Service** on Render
2. Click "Environment"
3. Update `CORS_ORIGINS` variable:
   ```
   https://coffee-feedback-frontend.onrender.com,http://localhost:5173
   ```
4. Click "Save Changes" → Backend will auto-redeploy

---

## Step 5: Test Your Deployment 🎉

Visit your frontend URL: `https://coffee-feedback-frontend.onrender.com`

**Features to test**:
- ✅ Voice recognition (mic access)
- ✅ Question flow
- ✅ AI matching for misspellings
- ✅ PDF report generation
- ✅ Session listing

---

## 📝 Important Notes

### Free Tier Limitations
- Backend spins down after 15 minutes of inactivity
- First request after idle takes ~30 seconds to wake up
- 750 hours/month free (enough for testing)

### Database Persistence
- SQLite file will persist on Render's free tier
- For production, consider PostgreSQL (Render offers free tier)

### OpenAI Costs
- ~$0.0005 per AI matching request
- Estimate: $1-2 for 100 feedback sessions

### Voice Recognition
- Works in Chrome/Edge (Web Speech API)
- Requires HTTPS (Render provides free SSL)
- User must grant microphone permission

---

## 🔧 Troubleshooting

### Backend won't start
- Check environment variables are set correctly
- Check build logs for Python version issues
- Verify `requirements.txt` has all dependencies

### Frontend can't reach backend
- Check `VITE_API_URL` points to correct backend URL
- Check `CORS_ORIGINS` in backend includes frontend URL
- Check browser console for CORS errors

### AI matching not working
- Verify `OPENAI_API_KEY` is set in backend
- Check OpenAI account has credits
- Check backend logs for API errors

### Voice not working
- Ensure HTTPS (HTTP won't work for microphone)
- Check browser permissions for microphone
- Try Chrome or Edge (best support)

---

## 📧 Share with Customers

Your customer URL will be:
```
https://coffee-feedback-frontend.onrender.com
```

**Instructions for customers**:
1. Open the URL in Chrome or Edge
2. Allow microphone access when prompted
3. Speak clearly for voice recognition
4. AI handles misspellings automatically

---

## 🚀 Next Steps (Optional)

### Custom Domain
1. Buy domain (e.g., godaddy.com)
2. In Render → Settings → Custom Domain
3. Add your domain (e.g., `feedback.yourdomain.com`)
4. Update CORS settings

### Upgrade to Paid Plan
- $7/month per service
- No spin-down delays
- Better performance

### Add PostgreSQL
- Render offers free PostgreSQL (90 days)
- Better for production
- Easier to query/export data

---

## 📊 Monitoring

**Backend logs**: Render Dashboard → Your Service → Logs
**Frontend logs**: Browser Console (F12)
**OpenAI usage**: https://platform.openai.com/usage

---

## 🆘 Support

If deployment fails, check:
1. GitHub repo is public or Render has access
2. All files are committed and pushed
3. Environment variables are set correctly
4. Build logs for specific errors

Good luck! 🎉
