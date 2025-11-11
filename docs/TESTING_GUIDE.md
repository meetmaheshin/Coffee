# Quick Testing Guide

## 🚀 Start the Application

### Option 1: Use Start Script (Windows)
```bash
.\start.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access Application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## ✅ Testing the New Features

### 1. Test No Duplicate Questions
**Steps:**
1. Open http://localhost:5173
2. Enter your name and coffee sample on home page
3. Click "Start Feedback Session"
4. **Verify:** First question should be about primary flavor profile (NOT asking name/sample again)

**Expected:** Question flow goes directly to flavor questions without re-asking name/sample.

---

### 2. Test Improved Layout
**Steps:**
1. Start a feedback session
2. Look at primary flavor profile question (8 options)
3. **Verify:**
   - All options visible without scrolling
   - Progress bar fixed at top
   - Voice panel compact at bottom
   - Options use most of screen space

**Expected:** Options fit in viewport, no scrolling needed for flavor profiles.

---

### 3. Test Mobile Responsive (Desktop Browser)
**Steps:**
1. Open Chrome DevTools (F12)
2. Click device toolbar icon (or Ctrl+Shift+M)
3. Select "iPhone 12 Pro" or "Pixel 5"
4. Start a session
5. **Verify:**
   - Layout adapts to narrow screen
   - Voice panel stacks vertically on mobile
   - Text sizes readable
   - Buttons large enough to tap

**Expected:** UI adapts gracefully to mobile viewport.

---

### 4. Test CSV Export
**Steps:**
1. Complete an entire feedback session
2. Reach the completion page
3. Click "Download CSV" button
4. Wait for "CSV exported successfully" message
5. Check `backend/exports/` folder
6. Open the CSV file

**Expected:**
- Button shows "⏳ Exporting..." while processing
- Success message appears
- CSV file created with timestamp in filename
- CSV contains: session info, all answers, timestamps

**CSV Format:**
```csv
Session ID,Tester Name,Coffee Sample,Question ID,Answer,Answer Type,Confidence,Timestamp
1,John Doe,Sample A,flavor_main,Fruity,voice,0.95,2024-01-15T10:30:00
```

---

### 5. Test Microphone Permission
**Steps:**
1. Open in Chrome or Edge (fresh browser session or incognito)
2. Start a feedback session
3. Click the microphone button 🎤
4. **Verify:** Browser shows permission prompt
5. Click "Allow"
6. Speak an answer clearly

**Test Permission Denied:**
1. Click microphone button
2. Click "Block" in permission prompt
3. **Verify:** Error message appears with instructions
4. Message should say: "Microphone Permission Denied" with guidance

**Expected:**
- Browser automatically prompts for permission
- Clear error if permission denied
- Instructions shown to fix permission issue

---

### 6. Test Browser Compatibility Warning
**Steps:**
1. Open home page in Chrome: http://localhost:5173
2. **Verify:** Green message: "✅ Voice Input Ready!"
3. Open same page in Firefox (if available)
4. **Verify:** Yellow warning about speech recognition not supported

**Expected:**
- Chrome/Edge: Shows green success message
- Firefox/Safari: Shows yellow warning
- Lists recommended browsers

---

### 7. Test Voice Recognition
**Steps (Chrome/Edge only):**
1. Start a feedback session
2. Wait for first question
3. Click microphone button
4. Say an answer clearly (e.g., "Fruity and sweet")
5. **Verify:**
   - Transcript appears in real-time
   - Confidence % shown
   - ✓ button appears
6. Click ✓ to submit

**Test with Multiple Choice:**
1. Reach "primary flavor profile" question
2. Click an option (e.g., "Fruity")
3. Click "Confirm 1 Selections"

**Expected:**
- Voice input works smoothly
- Transcript shows what you said
- Can also select by clicking options

---

### 8. Test No Auto-TTS (Text-to-Speech)
**Steps:**
1. Start a feedback session
2. Listen carefully when questions appear
3. **Verify:** Questions are NOT read aloud automatically

**Expected:** Questions show visually but don't speak automatically (as requested by user).

---

## 🔍 What to Look For

### Layout Issues
- [ ] Progress bar stays at top (doesn't scroll away)
- [ ] Question text and options visible without scrolling
- [ ] Voice panel stays at bottom
- [ ] No excessive white space
- [ ] Responsive on mobile sizes (320px - 768px)

### Voice Features
- [ ] Microphone button prompts for permission
- [ ] Transcript appears while speaking
- [ ] Confidence score shows
- [ ] Error messages clear and helpful
- [ ] ✓ and ↻ buttons appear after speaking

### CSV Export
- [ ] Button works on completion page
- [ ] File appears in backend/exports/
- [ ] CSV has all data correctly formatted
- [ ] Success message shows file location

### Browser Compatibility
- [ ] Warning shows in unsupported browsers
- [ ] Success message in supported browsers
- [ ] Fallback to click options works

---

## 🐛 Common Issues & Solutions

### Issue: Microphone not working
**Solution:**
1. Check browser: Use Chrome or Edge (Firefox doesn't support STT)
2. Check permissions: Click lock icon 🔒 in address bar, allow microphone
3. Check HTTPS: Should work on localhost
4. Check microphone: Test in system settings

### Issue: CSV not exporting
**Solution:**
1. Check backend is running (http://localhost:8000)
2. Check console for errors (F12)
3. Verify `backend/exports/` folder exists
4. Check file permissions (write access needed)

### Issue: Layout still has scrolling
**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard reload (Ctrl+Shift+R)
3. Check browser zoom is 100%
4. Try smaller screen resolution

### Issue: Options not showing
**Solution:**
1. Check console for errors (F12)
2. Verify backend loaded questions from CSV
3. Check network tab for API responses
4. Restart backend server

---

## 📊 Test Results Checklist

After testing, verify:

### Core Functionality
- [x] Backend starts without errors
- [x] Frontend builds without errors
- [ ] Home page loads correctly
- [ ] Can start a session
- [ ] Questions appear in correct order
- [ ] Can answer with voice
- [ ] Can answer by clicking
- [ ] Progress bar updates
- [ ] Can complete session
- [ ] Completion page shows summary

### New Features (This Session)
- [ ] Name/sample not asked twice ✅
- [ ] Auto-TTS disabled ✅
- [ ] Layout uses full screen ✅
- [ ] Options don't require scrolling ✅
- [ ] Mobile responsive ✅
- [ ] CSV export works ✅
- [ ] Mic permission handled ✅
- [ ] Browser warnings show ✅

### Cross-Browser
- [ ] Chrome desktop (full support)
- [ ] Edge desktop (full support)
- [ ] Safari desktop (warning shown)
- [ ] Firefox (warning shown)
- [ ] Chrome Android (full support - if available)
- [ ] Safari iOS (warning shown - if available)

---

## 📸 Screenshots to Take

For documentation:
1. Home page with browser compatibility message
2. Feedback view showing new layout (progress, question, voice panel)
3. Primary flavor options fitting in viewport
4. Voice panel with transcript
5. Completion page with CSV button
6. CSV export success message
7. Open CSV file showing data
8. Mobile view (responsive layout)

---

## 🎯 Success Criteria

The improvements are successful if:
- ✅ No duplicate questions
- ✅ All options visible without scrolling (on standard laptop screen)
- ✅ Voice panel compact at bottom
- ✅ CSV exports correctly
- ✅ Browser warnings show appropriately
- ✅ Mobile layout adapts properly
- ✅ Error messages clear and helpful

---

**Happy Testing! ☕🎉**

If you find any issues, note:
- What you did (steps to reproduce)
- What happened (actual result)
- What you expected (expected result)
- Browser and OS version
- Any console errors (F12)
