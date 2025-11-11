# Browser Compatibility Guide

## Web Speech API Compatibility

This application uses the **Web Speech API** for Speech-to-Text (STT) and Text-to-Speech (TTS) functionality. Browser support varies significantly across different platforms.

---

## 🌐 Desktop Browser Support

### ✅ **Fully Supported**
- **Google Chrome** (v33+)
  - STT: ✅ Full support
  - TTS: ✅ Full support
  - Notes: Best overall experience

- **Microsoft Edge** (v79+ Chromium-based)
  - STT: ✅ Full support
  - TTS: ✅ Full support
  - Notes: Same engine as Chrome

- **Opera** (v20+)
  - STT: ✅ Full support
  - TTS: ✅ Full support
  - Notes: Chromium-based

### ⚠️ **Partially Supported**
- **Safari** (macOS 14.1+)
  - STT: ❌ Not supported
  - TTS: ✅ Supported
  - Notes: No speech recognition, only speech synthesis

### ❌ **Not Supported**
- **Mozilla Firefox**
  - STT: ❌ Not supported
  - TTS: ✅ Supported (limited)
  - Notes: Speech recognition not available by default

- **Internet Explorer**
  - STT: ❌ Not supported
  - TTS: ❌ Not supported
  - Notes: Not recommended

---

## 📱 Mobile Browser Support

### ✅ **Android**
- **Chrome for Android** (v25+)
  - STT: ✅ Full support
  - TTS: ✅ Full support
  - Notes: **Recommended browser for mobile**

- **Samsung Internet** (v4+)
  - STT: ✅ Full support
  - TTS: ✅ Full support
  - Notes: Chromium-based, good support

### ⚠️ **iOS/iPadOS**
- **Safari on iOS** (v14.5+)
  - STT: ❌ Not supported
  - TTS: ✅ Supported
  - Notes: Limited functionality on iOS

- **Chrome on iOS**
  - STT: ❌ Not supported
  - TTS: ✅ Supported
  - Notes: Uses Safari engine (WebKit) on iOS

---

## 🔒 Permission Requirements

### Microphone Access
The Web Speech API requires **microphone permission** from the user:

1. **First Access**: Browser will automatically prompt for permission when you click the microphone button
2. **HTTPS Required**: Speech recognition only works on:
   - `https://` websites
   - `localhost` (for development)
3. **Permission States**:
   - ✅ **Granted**: Full STT functionality
   - ❌ **Denied**: STT won't work, user must manually allow in browser settings
   - ⏸️ **Prompt**: User will be asked on first use

### Checking Browser Settings

**Chrome/Edge:**
- Click the lock icon 🔒 in address bar
- Check "Microphone" permission
- Reset if needed

**Safari:**
- Safari → Preferences → Websites → Microphone
- Ensure the site is allowed

---

## 🎯 Recommended Setup

### For Best Experience:
1. **Desktop**: Use **Google Chrome** or **Microsoft Edge**
2. **Android**: Use **Chrome for Android**
3. **iOS**: ⚠️ Voice input not available (Safari limitation)
   - Consider using manual text input as fallback

### For Testing:
- Always use `https://` or `localhost`
- Grant microphone permissions when prompted
- Use a quiet environment for better accuracy

---

## 🛠️ Fallback Options

If your browser doesn't support speech recognition:

1. **Manual Input**: Type answers directly in the text box
2. **Use Supported Browser**: Switch to Chrome/Edge on desktop or Chrome on Android
3. **Desktop Alternative**: Use a desktop computer with Chrome

---

## 📊 Feature Support Summary

| Feature | Chrome/Edge | Safari | Firefox | Chrome Android | Safari iOS |
|---------|-------------|--------|---------|----------------|------------|
| Speech Recognition (STT) | ✅ | ❌ | ❌ | ✅ | ❌ |
| Speech Synthesis (TTS) | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Microphone Access | ✅ | ✅ | ✅ | ✅ | ✅ |
| Overall Rating | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

---

## 🔍 Checking Your Browser

To check if your browser supports the Web Speech API, the application will:
1. Automatically detect support on the home page
2. Show a warning message if STT is not available
3. Provide alternative input methods

### Manual Check:
Open your browser console (F12) and run:
```javascript
// Check Speech Recognition
console.log('Speech Recognition:', 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window)

// Check Speech Synthesis
console.log('Speech Synthesis:', 'speechSynthesis' in window)
```

---

## 📞 Support

If you encounter compatibility issues:
1. Ensure you're using a supported browser (Chrome/Edge recommended)
2. Check that microphone permissions are granted
3. Verify you're accessing via HTTPS or localhost
4. Try restarting your browser
5. Clear browser cache and cookies

---

**Last Updated**: 2024
**Application**: Coffee Tester Feedback Collection System
