<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="max-w-4xl w-full">
      <!-- Header -->
      <div class="text-center mb-12 animate-fade-in">
        <h1 class="text-6xl font-display font-bold text-coffee-700 mb-4">
          ☕ Coffee Taster
        </h1>
        <p class="text-2xl text-coffee-600 font-medium">
          Feedback Collection System
        </p>
        <p class="text-lg text-coffee-500 mt-2">
          Voice-enabled tasting experience
        </p>
      </div>

      <!-- Welcome Card -->
      <div class="bg-white rounded-3xl shadow-2xl p-12 mb-8 animate-slide-in">
        <h2 class="text-3xl font-bold text-coffee-800 mb-6 text-center">
          Welcome, Coffee Tester! ☕
        </h2>
        
        <p class="text-lg text-coffee-600 mb-8 text-center leading-relaxed">
          Let's capture your unique coffee tasting experience. You can answer questions 
          using your voice or by clicking options. Ready to begin?
        </p>

        <!-- Input Form -->
        <div class="space-y-6 mb-8">
          <div>
            <label for="tasterName" class="block text-sm font-semibold text-coffee-700 mb-2">
              Your Name (Optional)
            </label>
            <input
              id="tasterName"
              v-model="testerName"
              type="text"
              placeholder="Enter your name"
              class="w-full px-4 py-3 rounded-xl border-2 border-coffee-200 focus:border-coffee-500 
                     focus:ring-2 focus:ring-coffee-300 focus:outline-none transition-all"
            />
          </div>

          <div>
            <label for="coffeeSample" class="block text-sm font-semibold text-coffee-700 mb-2">
              Coffee Sample ID (Optional)
            </label>
            <input
              id="coffeeSample"
              v-model="coffeeSample"
              type="text"
              placeholder="e.g., Sample A, Ethiopia Yirgacheffe"
              class="w-full px-4 py-3 rounded-xl border-2 border-coffee-200 focus:border-coffee-500 
                     focus:ring-2 focus:ring-coffee-300 focus:outline-none transition-all"
            />
          </div>
        </div>

        <!-- Start Button -->
        <div class="flex justify-center">
          <button
            @click="handleStart"
            :disabled="isLoading"
            class="btn-primary text-xl px-12 py-4 disabled:opacity-50 disabled:cursor-not-allowed
                   flex items-center space-x-3"
          >
            <span v-if="!isLoading">🎤 Start Feedback Session</span>
            <span v-else class="flex items-center">
              <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Starting...
            </span>
          </button>
        </div>

        <!-- Browser Support Notice -->
        <div v-if="!isSpeechSupported" class="mt-6 p-4 bg-yellow-50 border-2 border-yellow-300 rounded-xl">
          <div class="flex items-start space-x-3">
            <div class="text-2xl">⚠️</div>
            <div class="flex-1">
              <p class="font-semibold text-yellow-800 mb-2">Speech Recognition Not Available</p>
              <p class="text-sm text-yellow-700 mb-2">
                Your browser doesn't support voice input. For the best experience, please use:
              </p>
              <ul class="text-sm text-yellow-700 list-disc list-inside space-y-1">
                <li><strong>Desktop:</strong> Google Chrome or Microsoft Edge</li>
                <li><strong>Android:</strong> Chrome for Android</li>
                <li><strong>Note:</strong> iOS devices don't support speech recognition</li>
              </ul>
              <p class="text-sm text-yellow-700 mt-2">
                You can still complete the feedback using click/tap options! 👆
              </p>
            </div>
          </div>
        </div>

        <!-- Browser Recommendation -->
        <div v-else class="mt-6 p-4 bg-green-50 border-2 border-green-300 rounded-xl">
          <p class="text-sm text-green-800 text-center flex items-center justify-center space-x-2">
            <span>✅</span>
            <span><strong>Voice Input Ready!</strong> Your browser supports speech recognition.</span>
          </p>
          <p class="text-xs text-green-700 text-center mt-1">
            Click "Allow" when prompted for microphone access.
          </p>
        </div>

        <!-- Features List -->
        <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center p-6 bg-coffee-50 rounded-xl">
            <div class="text-4xl mb-3">🎤</div>
            <h3 class="font-semibold text-coffee-800 mb-2">Voice Input</h3>
            <p class="text-sm text-coffee-600">Speak your answers naturally</p>
          </div>
          <div class="text-center p-6 bg-coffee-50 rounded-xl">
            <div class="text-4xl mb-3">👆</div>
            <h3 class="font-semibold text-coffee-800 mb-2">Click Options</h3>
            <p class="text-sm text-coffee-600">Tap or click to select</p>
          </div>
          <div class="text-center p-6 bg-coffee-50 rounded-xl">
            <div class="text-4xl mb-3">⚡</div>
            <h3 class="font-semibold text-coffee-800 mb-2">Quick & Easy</h3>
            <p class="text-sm text-coffee-600">Complete in under 3 minutes</p>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center text-coffee-500 text-sm">
        <p>Powered by AI Voice Technology • ABCD Coffee Testing</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFeedbackStore } from '@/stores/feedback'

const router = useRouter()
const feedbackStore = useFeedbackStore()

const testerName = ref('')
const coffeeSample = ref('')
const isLoading = ref(false)
const isSpeechSupported = ref(true)

onMounted(() => {
  // Check speech recognition support
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  isSpeechSupported.value = !!SpeechRecognition

  // Reset any previous session
  feedbackStore.resetSession()
})

const handleStart = async () => {
  isLoading.value = true
  
  try {
    // Request microphone permission first
    if (isSpeechSupported.value) {
      try {
        await navigator.mediaDevices.getUserMedia({ audio: true })
      } catch (micError) {
        console.error('Microphone permission denied:', micError)
        alert('Microphone access is required for voice features. Please allow microphone access and try again.')
        isLoading.value = false
        return
      }
    }

    const session = await feedbackStore.startSession(
      testerName.value || null,
      coffeeSample.value || null
    )
    
    // Navigate to feedback view
    router.push({ name: 'feedback', params: { sessionId: session.id } })
  } catch (error) {
    console.error('Failed to start session:', error)
    alert('Failed to start session. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>
