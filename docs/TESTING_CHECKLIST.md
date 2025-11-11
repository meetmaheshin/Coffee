# Coffee Tester App - Testing Checklist

Use this checklist to verify all features are working correctly.

## ✅ Pre-Test Setup

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Chrome, Edge, or Safari browser (for voice features)
- [ ] Microphone connected and working
- [ ] Browser microphone permissions granted

## 🏠 Home Page Tests

### Visual Tests
- [ ] Page loads without errors
- [ ] Coffee-themed colors visible (browns, creams)
- [ ] Header text displays correctly
- [ ] Welcome card centered and readable
- [ ] Input fields styled properly
- [ ] Start button has gradient effect
- [ ] Feature cards (3 columns) display correctly
- [ ] Responsive layout on mobile/tablet

### Functional Tests
- [ ] Can type in "Your Name" field
- [ ] Can type in "Coffee Sample ID" field
- [ ] Can start session without entering name/sample
- [ ] Can start session with name and sample
- [ ] Start button shows loading state
- [ ] Redirects to feedback page after clicking start
- [ ] Browser support warning shows (if Firefox)

### Keyboard Tests
- [ ] Tab navigation works through inputs
- [ ] Enter key submits form

## 🎤 Feedback Page Tests

### Visual Tests
- [ ] Progress bar visible at top
- [ ] Progress bar shows 0% initially
- [ ] Split-screen layout (Question left, Voice right)
- [ ] Question panel has white background
- [ ] Voice panel has dark gradient background
- [ ] Question text large and readable
- [ ] Category badge displays (if applicable)
- [ ] Microphone button large and centered
- [ ] Option cards styled properly

### Question Type Tests

#### Intro Questions
- [ ] Welcome screen displays
- [ ] "Let's Start" button works
- [ ] Transitions to next question smoothly

#### Single Choice Questions
- [ ] Option cards display vertically
- [ ] Hover effect works on cards
- [ ] Clicking card submits answer immediately
- [ ] Selected state shows briefly
- [ ] Next question loads automatically

#### Multiple Choice Questions
- [ ] Multiple options can be selected
- [ ] Selected options show checkmark
- [ ] "Confirm Selection" button appears
- [ ] Button shows count of selected items
- [ ] Can deselect options
- [ ] Confirms all selected options

#### Rating Questions (1-10)
- [ ] All 10 numbers display in grid
- [ ] Color coding: 1-3 red, 4-7 yellow, 8-10 green
- [ ] Hover effect on each number
- [ ] Clicking number submits immediately
- [ ] Numbers scale on hover

#### Open Text Questions
- [ ] Textarea displays
- [ ] Can type answer
- [ ] Placeholder text shows
- [ ] Submit button appears
- [ ] Button disabled when empty
- [ ] Ctrl+Enter submits
- [ ] Clears after submission

### Voice Interaction Tests

#### Speech Recognition (STT)
- [ ] Microphone button clickable
- [ ] Button changes when listening (pulse effect)
- [ ] Wave animations appear when listening
- [ ] Can click to start recording
- [ ] Can click again to stop recording
- [ ] Transcript appears in real-time
- [ ] Confidence score displays
- [ ] Error handling for no speech detected
- [ ] Works with clear speech
- [ ] Handles background noise reasonably

#### Text-to-Speech (TTS)
- [ ] Question reads aloud automatically
- [ ] Speech clear and understandable
- [ ] Rate/pitch appropriate
- [ ] Can be interrupted by new question
- [ ] Doesn't overlap with user speech

#### Voice Panel Features
- [ ] Submit button appears after speech
- [ ] Reset button works
- [ ] Keyboard shortcuts work (Space, Enter, Esc)
- [ ] Keyboard shortcut hints display
- [ ] Browser support warning (if unsupported)
- [ ] Error messages display properly

### Progress Tracking Tests
- [ ] Progress bar updates after each answer
- [ ] Percentage increases correctly
- [ ] Smooth animation on progress change
- [ ] Reaches 100% at end

### Navigation Tests
- [ ] Can't go back to home during session
- [ ] Completing session redirects to completion page
- [ ] Session persists in store

## 🎉 Completion Page Tests

### Visual Tests
- [ ] Confetti animation plays
- [ ] Success emoji displays large
- [ ] Completion message shows
- [ ] Summary card centered
- [ ] Grid layout for session info
- [ ] Action buttons styled properly

### Functional Tests
- [ ] Report data loads correctly
- [ ] Tester name displays (or "Anonymous")
- [ ] Coffee sample displays (or "Not specified")
- [ ] Answer count correct
- [ ] Duration calculated accurately
- [ ] "View Full Report" button works
- [ ] "Start New Session" button works
- [ ] Detailed responses expand/collapse
- [ ] Can see all answers in detail
- [ ] Confidence scores display
- [ ] Answer types display (voice/click/text)

## 🔧 Backend API Tests

### Health Check
- [ ] GET http://localhost:8000 returns 200
- [ ] Response includes version and status

### API Documentation
- [ ] http://localhost:8000/docs loads Swagger UI
- [ ] All endpoints documented
- [ ] Can test endpoints from Swagger
- [ ] Schemas display correctly

### Session Endpoints
- [ ] POST /api/sessions/start creates session
- [ ] Returns session ID and first question
- [ ] GET /api/sessions lists sessions
- [ ] POST /api/sessions/{id}/complete marks complete

### Feedback Endpoints
- [ ] POST /api/feedback/answer saves answer
- [ ] Returns next question
- [ ] Returns null when done
- [ ] Question ID validation works

### Report Endpoints
- [ ] GET /api/reports/{session_id} returns data
- [ ] Includes all answers
- [ ] Includes session metadata
- [ ] Timestamps formatted correctly

### Question Endpoints
- [ ] GET /api/questions lists all questions
- [ ] Questions ordered correctly
- [ ] GET /api/questions/{id} returns single question
- [ ] Question options parsed correctly

## 🎨 Design & UX Tests

### Colors & Typography
- [ ] Coffee brown theme consistent
- [ ] Text readable (contrast ratio)
- [ ] Font sizes appropriate
- [ ] Headings use Poppins
- [ ] Body uses Inter

### Animations
- [ ] Smooth page transitions
- [ ] Fade-in effects work
- [ ] Slide-in effects work
- [ ] Hover animations smooth
- [ ] Progress bar animates
- [ ] Microphone pulse effect
- [ ] Wave animations
- [ ] Confetti animation

### Responsiveness
- [ ] Works on 1920x1080 (desktop)
- [ ] Works on 1366x768 (laptop)
- [ ] Works on 768x1024 (tablet)
- [ ] Works on 375x667 (mobile)
- [ ] Split layout stacks on mobile
- [ ] Text remains readable
- [ ] Buttons touchable on mobile
- [ ] No horizontal scrolling

### Accessibility
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Color contrast sufficient
- [ ] Error messages clear
- [ ] Loading states announced
- [ ] Labels for form inputs
- [ ] Alt text for icons (if any)

## 🐛 Error Handling Tests

### Frontend Errors
- [ ] Backend offline - shows error message
- [ ] Network timeout - shows error message
- [ ] Invalid response - handles gracefully
- [ ] No microphone - shows warning
- [ ] Speech recognition error - shows message
- [ ] Can retry after error

### Backend Errors
- [ ] Invalid session ID - returns 404
- [ ] Missing required fields - returns 400
- [ ] Database error - returns 500
- [ ] CORS errors handled

## 🚀 Performance Tests

### Load Times
- [ ] Home page loads < 2 seconds
- [ ] Feedback page loads < 2 seconds
- [ ] API responses < 500ms
- [ ] Smooth 60fps animations

### Resource Usage
- [ ] No memory leaks (check DevTools)
- [ ] CPU usage reasonable
- [ ] Network requests optimized
- [ ] Images/assets load efficiently

## 🔒 Security Tests

### Input Validation
- [ ] SQL injection protected (parameterized queries)
- [ ] XSS protected (Vue auto-escapes)
- [ ] CORS configured correctly
- [ ] No sensitive data in console

## 📱 Browser Compatibility Tests

Test in each browser:

### Chrome
- [ ] All features work
- [ ] Voice recognition works
- [ ] TTS works
- [ ] No console errors

### Edge
- [ ] All features work
- [ ] Voice recognition works
- [ ] TTS works
- [ ] No console errors

### Safari
- [ ] All features work
- [ ] Voice recognition works
- [ ] TTS works
- [ ] No console errors

### Firefox
- [ ] Visual features work
- [ ] Click/type input works
- [ ] Voice warning shows
- [ ] Graceful degradation

## 💯 Integration Tests

### Complete User Journey
- [ ] Open home page
- [ ] Enter tester info
- [ ] Start session
- [ ] Answer using voice
- [ ] Answer using click
- [ ] Answer using text
- [ ] Use keyboard shortcuts
- [ ] Complete all questions
- [ ] See confetti
- [ ] View report
- [ ] Start new session
- [ ] Complete second session

### Data Flow
- [ ] Frontend → Backend → Database
- [ ] Session created in DB
- [ ] Answers saved in DB
- [ ] Questions loaded from CSV
- [ ] Report generated from DB data

## 📊 CSV Data Tests

### Flavor.csv Loading
- [ ] CSV parsed correctly on backend start
- [ ] Categories created (Fruity, Floral, etc.)
- [ ] Subcategories created (Lemon, Jasmine, etc.)
- [ ] Questions generated from CSV
- [ ] Options populated correctly

### Question Flow Logic
- [ ] Selecting "Fruity" → shows fruity options
- [ ] Selecting "Floral" → shows floral options
- [ ] After specific flavor → goes to intensity
- [ ] Intensity → Aftertaste → Body → etc.
- [ ] Ends after additional notes

## ✅ Final Checks

- [ ] No console errors
- [ ] No console warnings (major)
- [ ] No broken images
- [ ] No broken links
- [ ] All text readable
- [ ] All buttons clickable
- [ ] All inputs functional
- [ ] All animations smooth
- [ ] Documentation up-to-date
- [ ] README accurate
- [ ] Code commented
- [ ] Git repo clean

## 🎯 Success Criteria

- [ ] ✅ Voice recognition accuracy >85%
- [ ] ✅ Complete session in <3 minutes
- [ ] ✅ Responsive on all devices
- [ ] ✅ Accessible (WCAG 2.1 AA)
- [ ] ✅ Delightful user experience
- [ ] ✅ No critical bugs
- [ ] ✅ Production-ready

---

## Test Results

**Date Tested**: _______________

**Tester Name**: _______________

**Browser Used**: _______________

**Overall Result**: ⭐ PASS / FAIL

**Notes**:
_______________________________________________
_______________________________________________
_______________________________________________

**Critical Issues Found**:
_______________________________________________
_______________________________________________

**Minor Issues Found**:
_______________________________________________
_______________________________________________

**Suggestions**:
_______________________________________________
_______________________________________________
