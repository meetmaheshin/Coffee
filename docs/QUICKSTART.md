# Coffee Tester Feedback Collection App - Quick Start Guide

## Installation & Setup

### Option 1: Automatic Setup (Windows)

Simply double-click `setup.bat` and it will:
- Create Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Create environment files

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## Running the Application

### Option 1: Automatic Start (Windows)

Double-click `start.bat` to launch both backend and frontend servers automatically.

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access Points

- **Frontend App**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/redoc

## Features to Test

1. **Voice Input**
   - Click the microphone button
   - Speak clearly
   - Watch real-time transcription

2. **Click/Tap Input**
   - Click any option card
   - Select ratings by clicking numbers
   - Type text answers

3. **Keyboard Shortcuts**
   - `Space` - Toggle microphone
   - `Enter` - Submit answer
   - `Esc` - Reset/clear
   - `Ctrl+Enter` - Submit text input

4. **Progress Tracking**
   - Watch the progress bar at the top
   - See completion percentage

5. **Completion Celebration**
   - Complete all questions
   - Enjoy the confetti animation
   - View your detailed report

## Browser Compatibility

**Best Experience:**
- Chrome 25+
- Edge 79+
- Safari 14.1+

**Note:** Voice features require microphone permissions and HTTPS in production.

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Check if port 8000 is available
- Verify virtual environment is activated

**Frontend won't start:**
- Ensure Node.js 18+ is installed
- Try `npm install` again
- Check if port 5173 is available

**Voice not working:**
- Use Chrome, Edge, or Safari
- Grant microphone permissions
- Check browser console for errors

## Next Steps

1. Start a feedback session
2. Answer questions using voice or click
3. Complete the session
4. View your report
5. Start a new session to test different coffee samples

Enjoy your coffee tasting experience! ☕
