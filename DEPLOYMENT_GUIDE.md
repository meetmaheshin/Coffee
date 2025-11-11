# Deployment Guide - Render.com

## Prerequisites
- GitHub account with your code pushed
- Render.com account (free tier available)
- OpenAI API key

## Step-by-Step Deployment

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy on Render.com

1. Go to https://render.com and sign in with GitHub
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository: `meetmaheshin/coffie-testing`
4. Render will detect `render.yaml` and show 2 services:
   - `coffee-feedback-api` (Backend)
   - `coffee-feedback` (Frontend)

### 3. Configure Environment Variables

**For Backend (coffee-feedback-api):**
- `OPENAI_API_KEY`: Your OpenAI API key (sk-proj-...)
- `DATABASE_URL`: `sqlite+aiosqlite:///./coffee_feedback.db` (auto-set)
- `CORS_ORIGINS`: Will be auto-set to frontend URL

**For Frontend (coffee-feedback):**
- `VITE_API_URL`: Will be auto-set to backend URL

### 4. Deploy
- Click "Apply" to start deployment
- Backend: ~5-10 minutes
- Frontend: ~3-5 minutes

### 5. Get Your URLs
After deployment completes:
- **Frontend**: `https://coffee-feedback.onrender.com`
- **Backend API**: `https://coffee-feedback-api.onrender.com`

### 6. Update CORS (Important!)
After getting your frontend URL:
1. Go to Backend service → Environment
2. Update `CORS_ORIGINS` to match your actual frontend URL
3. Save and redeploy

### 7. Test
- Open your frontend URL
- Start a feedback session
- Test voice input with "Frooti", "Arthi", etc.

## Free Tier Limitations
- Backend sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- 750 hours/month free (more than enough for testing)

## Upgrade to Paid ($7/month per service)
- No sleep
- Faster response
- Better for production use

## Troubleshooting

### Backend won't start
- Check environment variables are set
- Check logs in Render dashboard
- Verify `requirements.txt` is correct

### Frontend shows API errors
- Verify `VITE_API_URL` points to backend URL
- Check CORS settings in backend
- Wait for backend to wake up (if using free tier)

### Voice recognition not working
- HTTPS is required for Web Speech API (Render provides this)
- Check browser console for errors
- Ensure microphone permissions granted

## Your URLs (Update these after deployment)
- Frontend: `https://[your-app-name].onrender.com`
- Backend: `https://[your-api-name].onrender.com`

Share the frontend URL with your customers!
