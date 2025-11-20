<template>
  <div class="bg-gradient-to-br from-coffee-700 to-coffee-900 rounded-2xl shadow-2xl flex flex-col h-full text-white overflow-hidden">
    
    <!-- Chat History Display -->
    <div class="flex-1 overflow-y-auto p-6 space-y-3">
      <!-- Welcome Message (shows once on load) -->
      <div v-if="showWelcome" class="bg-green-500 bg-opacity-20 backdrop-blur rounded-xl p-4 animate-fade-in">
        <div class="flex items-start gap-3">
          <div class="text-2xl">👋</div>
          <div class="flex-1">
            <p class="text-xs font-bold text-green-100 mb-1">Welcome to Coffee Tasting!</p>
            <p class="text-xs text-green-200 leading-relaxed">
              I'll guide you through the tasting process. Speak naturally or select options.
            </p>
          </div>
        </div>
      </div>

      <!-- Chat Messages History -->
      <div v-for="(message, index) in chatHistory" :key="index" class="animate-fade-in">
        
        <!-- AI Question Message -->
        <div v-if="message.type === 'question'" class="bg-white bg-opacity-10 backdrop-blur rounded-xl p-4 mb-3">
          <div class="flex items-start gap-3">
            <div class="text-2xl flex-shrink-0">🤖</div>
            <div class="flex-1 min-w-0">
              <p class="text-xs font-semibold text-coffee-200 mb-1">AI Assistant</p>
              <p class="text-sm md:text-base font-medium leading-relaxed break-words">
                {{ message.text }}
              </p>
              <p class="text-xs text-coffee-400 mt-1">
                {{ formatTime(message.timestamp) }}
              </p>
            </div>
            <button
              @click="speak(message.text)"
              class="text-coffee-200 hover:text-white transition-colors p-1 flex-shrink-0"
              title="Read aloud"
            >
              🔊
            </button>
          </div>
        </div>

        <!-- User Answer Message -->
        <div v-if="message.type === 'answer'" class="bg-coffee-800 bg-opacity-50 rounded-xl p-4 mb-3 ml-8">
          <div class="flex items-start gap-3">
            <div class="text-2xl flex-shrink-0">👤</div>
            <div class="flex-1 min-w-0">
              <p class="text-xs font-semibold text-coffee-200 mb-1">You</p>
              <p class="text-sm md:text-base leading-relaxed break-words">
                {{ message.text }}
              </p>
              <div class="flex items-center gap-2 mt-1">
                <span v-if="message.confidence > 0" class="text-xs text-green-400">
                  ✓ {{ Math.round(message.confidence * 100) }}%
                </span>
                <span class="text-xs text-coffee-400">
                  {{ formatTime(message.timestamp) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Current Input Area (Live Transcript) -->
      <div v-if="isListening || transcript" class="bg-blue-500 bg-opacity-20 backdrop-blur rounded-xl p-4 border-2 border-blue-400 border-opacity-50">
        <div class="flex items-start gap-3">
          <div class="text-2xl flex-shrink-0">👤</div>
          <div class="flex-1 min-w-0">
            <p class="text-xs font-semibold text-blue-200 mb-1">Speaking now...</p>
            
            <!-- Live transcript -->
            <p v-if="transcript" class="text-sm md:text-base leading-relaxed break-words animate-pulse">
              {{ transcript }}
            </p>
            
            <!-- Listening indicator -->
            <p v-else-if="isListening" class="text-sm text-blue-300 italic animate-pulse">
              Listening for your voice...
            </p>
            
            <!-- Confidence -->
            <span v-if="confidence > 0" class="text-xs text-green-300 mt-1 block">
              Confidence: {{ Math.round(confidence * 100) }}%
            </span>
          </div>
        </div>
      </div>

      <!-- Scroll anchor -->
      <div ref="chatBottom"></div>
    </div>

    <!-- Control Panel at Bottom -->
    <div class="border-t border-white border-opacity-20 p-4">
      <div class="flex items-center gap-3">
        
        <!-- Microphone Button -->
        <div class="relative">
          <!-- Animated Waves -->
          <div v-if="isListening" class="absolute inset-0">
            <div class="wave-animation" style="animation-delay: 0s;"></div>
            <div class="wave-animation" style="animation-delay: 0.5s;"></div>
          </div>

          <!-- Main Microphone Button -->
          <button
            @click="toggleListening"
            :disabled="isSubmitting || !isSpeechSupported"
            class="w-16 h-16 rounded-full shadow-xl flex items-center justify-center cursor-pointer
                   transition-all duration-300 hover:scale-110 active:scale-95 relative z-10"
            :class="{
              'bg-gradient-to-br from-green-400 to-green-600 ring-4 ring-green-300 ring-opacity-50': isListening,
              'bg-gradient-to-br from-red-400 to-red-600': !isListening
            }"
          >
            <!-- Microphone Icon -->
            <svg
              v-if="!isListening"
              class="w-8 h-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
              />
            </svg>
            
            <!-- Stop Icon when listening -->
            <svg
              v-else
              class="w-8 h-8 text-white animate-pulse"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <rect x="6" y="6" width="12" height="12" rx="2" />
            </svg>
          </button>
        </div>

        <!-- Mic Status Indicator -->
        <div class="flex-1 text-center">
          <div class="flex items-center justify-center gap-2">
            <!-- Status Icon -->
            <div class="w-3 h-3 rounded-full border-2" :class="{
              'bg-green-400 border-green-500 animate-pulse shadow-lg shadow-green-500/50': isListening,
              'bg-red-400 border-red-500': !isListening
            }"></div>
            
            <!-- Status Text -->
            <p class="text-sm font-bold" :class="{
              'text-green-300': isListening,
              'text-red-300': !isListening
            }">
              {{ isListening ? '🎤 MIC ACTIVE' : '🔇 MIC DISABLED' }}
            </p>
          </div>
          <p class="text-xs text-coffee-300 mt-1">
            Click mic to {{ isListening ? 'disable' : 'enable' }} • Stays on until you disable
          </p>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-2">
          <!-- Restart Mic Button (if mic seems stuck) -->
          <button
            v-if="!isListening && isSpeechSupported"
            @click="forceRestart"
            :disabled="isSubmitting"
            class="bg-orange-500 hover:bg-orange-600 text-white px-3 py-2 rounded-lg
                   text-sm font-semibold shadow-lg transition-all
                   disabled:opacity-50 disabled:cursor-not-allowed"
            title="Restart microphone"
          >
            🔄 Restart Mic
          </button>
          
          <!-- Clear Transcript Button -->
          <button
            v-if="transcript"
            @click="reset"
            :disabled="isSubmitting"
            class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-2 rounded-lg
                   text-sm font-semibold shadow-lg transition-all
                   disabled:opacity-50 disabled:cursor-not-allowed"
            title="Clear transcript"
          >
            🗑️ Clear
          </button>
        </div>
      </div>
    </div>

    <!-- Browser Support Warning -->
    <div v-if="!isSpeechSupported" class="mt-4 p-4 bg-yellow-500 bg-opacity-20 rounded-xl">
      <p class="text-sm text-yellow-200 text-center">
        ⚠️ Voice recognition not supported in this browser. Please use Chrome, Edge, or Safari.
      </p>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="mt-4 p-3 md:p-4 bg-red-500 bg-opacity-20 rounded-xl">
      <div class="flex items-start space-x-2">
        <span class="text-lg">🚫</span>
        <div class="flex-1">
          <p class="text-sm font-semibold text-red-100 mb-1">
            {{ getErrorTitle(error) }}
          </p>
          <p class="text-xs text-red-200">
            {{ getErrorMessage(error) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useElevenLabsTTS } from '@/composables/useElevenLabsTTS'
import { useSpeechRecognition } from '@/composables/useSpeech'

const props = defineProps({
  question: {
    type: Object,
    required: true
  },
  isSubmitting: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['voice-answer'])

const showWelcome = ref(true)
const autoSubmitTimer = ref(null)
const chatHistory = ref([])  // Store chat messages as array
const chatBottom = ref(null)  // Reference to scroll anchor

const {
  isListening,
  transcript,
  confidence,
  isSupported: isSpeechSupported,
  error,
  start,
  stop,
  reset,
  forceRestart
} = useSpeechRecognition()

const { isSpeaking, speak, cancel, error: ttsError } = useElevenLabsTTS()

// Format timestamp for chat messages
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { 
    hour: 'numeric', 
    minute: '2-digit',
    hour12: true 
  })
}

// Auto-scroll to bottom when new messages added
const scrollToBottom = () => {
  setTimeout(() => {
    if (chatBottom.value) {
      chatBottom.value.scrollIntoView({ behavior: 'smooth', block: 'end' })
    }
  }, 100)
}

// Hide welcome message after 5 seconds
setTimeout(() => {
  showWelcome.value = false
}, 5000)

// Watch for question changes - add to chat history and speak
let isFirstLoad = true
let preloadAudio = null
// Helper to preload TTS audio for a given text
const preloadTTS = async (text, voice_id = null) => {
  try {
    // Use the same API as speak, but don't play, just fetch and cache
    await api.post('/api/tts', { text, voice_id: voice_id || 'EIsgvJT3rwoPvRFG6c4n' }, { responseType: 'blob' })
  } catch (e) {
    // Ignore errors for preloading
  }
}

watch(() => props.question, async (newQuestion, oldQuestion) => {
  if (newQuestion && newQuestion.text) {
    console.log('Question changed:', oldQuestion?.id, '->', newQuestion.id)
    cancel()
    // Clear any pending auto-submit
    if (autoSubmitTimer.value) {
      clearTimeout(autoSubmitTimer.value)
      autoSubmitTimer.value = null
    }
    // Add question to chat history
    if (oldQuestion && oldQuestion.id !== newQuestion.id) {
      chatHistory.value.push({
        type: 'question',
        text: newQuestion.text,
        timestamp: new Date()
      })
      scrollToBottom()
    } else if (!oldQuestion) {
      // Initial question
      chatHistory.value.push({
        type: 'question',
        text: newQuestion.text,
        timestamp: new Date()
      })
      scrollToBottom()
    }
    // Only auto-speak and restart for question changes (not initial load)
    const isQuestionChange = oldQuestion && oldQuestion.id !== newQuestion.id
    if (isQuestionChange) {
      setTimeout(async () => {
        await speak(newQuestion.text)
        // Always restart mic after TTS
        if (isSpeechSupported.value) {
          start()
        }
        // Preload next question's TTS if available
        if (props.nextQuestion && props.nextQuestion.text) {
          preloadTTS(props.nextQuestion.text)
        }
      }, 800)
    }
    isFirstLoad = false
  }
}, { immediate: true })

// Watch transcript for auto-submit after silence (turn detection)
watch(transcript, (newTranscript) => {
  if (newTranscript && newTranscript.trim().length > 0) {
    // Clear existing timer
    if (autoSubmitTimer.value) {
      clearTimeout(autoSubmitTimer.value)
    }
    
    // Set new timer - auto-submit after 2 seconds of silence
    autoSubmitTimer.value = setTimeout(() => {
      if (newTranscript.trim().length > 0 && !props.isSubmitting) {
        handleSubmit()
      }
    }, 2000)
  }
})

// Manually speak the question
const speakQuestion = () => {
  if (props.question && props.question.text) {
    speak(props.question.text)
  }
}

// Keyboard shortcuts
const handleKeyDown = (e) => {
  if (e.code === 'Space' && !props.isSubmitting) {
    e.preventDefault()
    toggleListening()
  } else if (e.code === 'Enter' && transcript.value && !isListening.value && !props.isSubmitting) {
    e.preventDefault()
    handleSubmit()
  } else if (e.code === 'Escape' && !props.isSubmitting) {
    e.preventDefault()
    handleReset()
  }
}


onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  // Listen for start-mic event from parent
  window.addEventListener('start-mic', () => {
    if (!isListening.value && isSpeechSupported.value) {
      start()
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  cancel()
})

const toggleListening = () => {
  if (isListening.value) {
    stop()
  } else {
    start()
  }
}

const handleSubmit = () => {
  if (transcript.value && !props.isSubmitting) {
    // Add user's answer to chat history
    chatHistory.value.push({
      type: 'answer',
      text: transcript.value,
      confidence: confidence.value,
      timestamp: new Date()
    })
    
    emit('voice-answer', transcript.value, confidence.value)
    
    // Clear current transcript for next answer
    reset()
    
    // Scroll to bottom to show new message
    scrollToBottom()
  }
}

const handleReset = () => {
  reset()
  // Don't stop mic - keep it active
}

const getErrorTitle = (errorType) => {
  const titles = {
    'not-allowed': 'Microphone Permission Denied',
    'no-speech': 'No Speech Detected',
    'audio-capture': 'Microphone Not Available',
    'network': 'Network Error',
    'aborted': 'Recognition Aborted'
  }
  return titles[errorType] || 'Voice Recognition Error'
}

const getErrorMessage = (errorType) => {
  const messages = {
    'not-allowed': 'Please allow microphone access in your browser settings and reload the page.',
    'no-speech': 'No speech was detected. Please try again and speak clearly.',
    'audio-capture': 'No microphone found. Please connect a microphone and try again.',
    'network': 'Network connection issue. Please check your internet connection.',
    'aborted': 'Recognition was stopped. Click the microphone to try again.'
  }
  return messages[errorType] || 'An error occurred. Please try again or use click options.'
}
</script>
