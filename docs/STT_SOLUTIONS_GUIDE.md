# Speech-to-Text (STT) Solutions Guide

## Current Issue: Web Speech API Reliability

### Why Current Implementation Has Issues:
1. **Browser-Dependent** - Web Speech API (Chrome) uses Google's STT, which can be unstable
2. **Internet Dependent** - Requires constant internet connection
3. **Inconsistent Results** - Sometimes mic "hangs" or doesn't restart properly
4. **Limited Control** - Can't control quality, timeouts, or error handling deeply
5. **No Offline Support** - Stops working without internet

---

## Production-Grade STT Solutions for USA

### 🥇 **RECOMMENDED: OpenAI Whisper API** (Best for Your Use Case)

**Why Best for Coffee Tasting App:**
- ✅ **Extremely Accurate** - Industry-leading accuracy (95%+)
- ✅ **Works with Accents** - Handles diverse US accents (Southern, Midwest, etc.)
- ✅ **Technical Terms** - Understands coffee terminology (fruity, cocoa, earthy, etc.)
- ✅ **Real-Time** - Low latency (500ms - 1s response time)
- ✅ **Affordable** - $0.006 per minute (~$0.36/hour)
- ✅ **Easy Integration** - Simple REST API

**Pricing Example:**
- 5-minute session = $0.03
- 100 sessions/day = $3/day = $90/month
- Very affordable for production use

**Implementation:**
```javascript
// Backend endpoint (FastAPI)
import openai

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile):
    transcript = await openai.Audio.atranscribe(
        model="whisper-1",
        file=audio.file,
        language="en"
    )
    return {"text": transcript.text}

// Frontend (capture audio and send)
const mediaRecorder = new MediaRecorder(stream)
const audioChunks = []

mediaRecorder.ondataavailable = (e) => {
    audioChunks.push(e.data)
}

mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
    const formData = new FormData()
    formData.append('audio', audioBlob)
    
    const response = await fetch('/api/transcribe', {
        method: 'POST',
        body: formData
    })
    const { text } = await response.json()
}
```

**Pros:**
- Most accurate for natural speech
- Handles background noise well
- Works with various audio qualities
- Can be used for future AI features

**Cons:**
- Requires backend processing
- Small cost per minute
- Needs OpenAI API key

---

### 🥈 **Option 2: Google Cloud Speech-to-Text**

**Best for:** Enterprise-level accuracy and scalability

**Features:**
- Real-time streaming recognition
- Custom vocabulary (add coffee terms)
- Speaker diarization (multiple speakers)
- Profanity filtering

**Pricing:**
- Standard: $0.006/15 seconds = $0.024/minute
- Enhanced: $0.009/15 seconds = $0.036/minute
- Free tier: 60 minutes/month

**Implementation:**
```javascript
// Backend (Python)
from google.cloud import speech_v1

client = speech_v1.SpeechClient()

config = speech_v1.RecognitionConfig(
    encoding=speech_v1.RecognitionConfig.AudioEncoding.WEBM_OPUS,
    sample_rate_hertz=48000,
    language_code="en-US",
    enable_automatic_punctuation=True,
    model="latest_long",  # Best for conversations
    use_enhanced=True,  # Better accuracy
    # Add coffee-specific vocabulary
    speech_contexts=[{
        "phrases": ["fruity", "cocoa", "earthy", "nutty", "floral"],
        "boost": 20
    }]
)

response = client.recognize(config=config, audio=audio)
```

**Pros:**
- Excellent accuracy
- Custom vocabulary for coffee terms
- Real-time streaming
- Scales to enterprise level

**Cons:**
- More expensive than Whisper
- Requires Google Cloud account
- More complex setup

---

### 🥉 **Option 3: Azure Speech Services**

**Best for:** Microsoft ecosystem integration

**Features:**
- Custom Speech models
- Real-time transcription
- Conversation transcription
- Custom pronunciation

**Pricing:**
- Standard: $1 per audio hour
- Free tier: 5 audio hours/month

**Pros:**
- Good accuracy
- Integration with Azure ecosystem
- Custom models possible
- Free tier generous

**Cons:**
- More expensive for high volume
- Requires Azure account

---

### 💰 **Option 4: AssemblyAI** (Cost-Effective Alternative)

**Best for:** Budget-conscious with good accuracy

**Pricing:**
- $0.00025 per second = $0.015/minute = $0.90/hour
- Cheaper than OpenAI for high volume

**Features:**
- Real-time transcription
- Speaker labels
- Content moderation
- Custom vocabulary

**Implementation:**
```javascript
// Very simple REST API
const response = await fetch('https://api.assemblyai.com/v2/transcript', {
    method: 'POST',
    headers: {
        'authorization': API_KEY,
        'content-type': 'application/json'
    },
    body: JSON.stringify({
        audio_url: audioUrl,
        language_code: 'en_us'
    })
})
```

---

### 🆓 **Option 5: Mozilla DeepSpeech** (Open Source - Offline)

**Best for:** Privacy-focused, offline use

**Features:**
- Completely offline
- No API costs
- Full privacy
- Fast on modern hardware

**Requirements:**
- Run model on backend server
- ~2GB model size
- GPU recommended for real-time

**Pros:**
- Zero ongoing costs
- Complete privacy
- Works offline
- No API limits

**Cons:**
- Lower accuracy than commercial (85-90%)
- Requires powerful server
- More development work
- Harder to maintain

---

## Comparison Table

| Solution | Accuracy | Cost (per hour) | Latency | Setup | Best For |
|----------|----------|-----------------|---------|-------|----------|
| **OpenAI Whisper** | 95%+ | $0.36 | 500ms-1s | Easy | ⭐ Recommended |
| Google Cloud STT | 95%+ | $1.44 | <500ms | Medium | Enterprise |
| Azure Speech | 93%+ | $1.00 | <500ms | Medium | Azure users |
| AssemblyAI | 92%+ | $0.90 | 1-2s | Easy | Budget |
| DeepSpeech | 85-90% | $0 | 200ms | Hard | Privacy/Offline |
| Web Speech API | 85-95% | $0 | 500ms | Very Easy | Testing only |

---

## 🎯 My Recommendation for Your Coffee App

### Immediate (MVP/Testing):
**Keep Web Speech API** - It's free and good enough for testing

**Fix Current Issues:**
1. Add audio buffering to prevent mic hang
2. Implement better error recovery
3. Add connection monitoring
4. Show clear status indicators (we already did this ✅)

### Production (When Launching in USA):
**Use OpenAI Whisper API** 

**Reasons:**
1. **Best Accuracy** - Critical for understanding coffee terminology
2. **Cost-Effective** - At ~100 sessions/day, only $90/month
3. **Easy Migration** - Just add backend endpoint, minimal frontend changes
4. **Future AI Ready** - Can use same API key for AI analysis later
5. **US Optimized** - Trained on diverse US accents

**ROI Calculation:**
- Cost: $90/month for 100 sessions/day
- Per session: $0.03
- Value: Accurate data = better insights = happy customers
- **Worth it!**

---

## Implementation Roadmap

### Phase 1: Fix Current Issues (This Week)
- ✅ Add mic status indicators (Done!)
- ✅ Chat history view (Done!)
- ⏳ Add audio quality monitoring
- ⏳ Implement reconnection logic
- ⏳ Add error recovery

### Phase 2: Prepare for Production (Before Launch)
- Set up OpenAI account
- Create backend `/api/transcribe` endpoint
- Replace Web Speech API with audio recording
- Send audio chunks to Whisper API
- Handle responses in real-time

### Phase 3: Future AI Enhancement
- Use Whisper transcripts for AI analysis
- Implement GPT-4 for intelligent parsing
- Auto-categorize answers ("dark chocolate" → Cocoa > Dark Chocolate)
- Natural language understanding ("I taste some chocolate notes" → selects Cocoa)

---

## Code Example: Fixing Current Web Speech API Issues

### Better Error Recovery
```javascript
// In useSpeech.js
let reconnectAttempts = 0
const MAX_RECONNECT_ATTEMPTS = 3

recognition.onerror = (event) => {
  console.error('Speech recognition error:', event.error)
  error.value = event.error
  
  // Auto-reconnect on network errors
  if (event.error === 'network' && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
    console.log(`Reconnecting... Attempt ${reconnectAttempts + 1}`)
    reconnectAttempts++
    setTimeout(() => {
      if (shouldKeepListening && recognition) {
        recognition.start()
      }
    }, 1000 * reconnectAttempts) // Exponential backoff
  } else {
    isListening.value = false
    reconnectAttempts = 0
  }
}

recognition.onstart = () => {
  reconnectAttempts = 0  // Reset on successful start
  isListening.value = true
  // ... rest of code
}
```

### Connection Monitoring
```javascript
// Add to VoicePanel.vue
const isOnline = ref(navigator.onLine)

window.addEventListener('online', () => {
  isOnline.value = true
  // Auto-restart mic if it was on
  if (shouldKeepListening && !isListening.value) {
    start()
  }
})

window.addEventListener('offline', () => {
  isOnline.value = false
  error.value = 'network'
})
```

---

## Next Steps

1. **Test current implementation** with mic fixes
2. **Decide on production STT** (I recommend Whisper)
3. **Budget approval** ($90-100/month for production STT)
4. **Development timeline** (2-3 days to integrate Whisper)
5. **Testing phase** (1 week with real users)

## Questions to Consider

- What's your monthly budget for cloud services?
- How many daily sessions do you expect?
- Is offline capability required?
- Do you need real-time transcription or batch processing is OK?
- Will you add AI features in future?

Let me know your priorities and I can help implement the best solution! 🚀
