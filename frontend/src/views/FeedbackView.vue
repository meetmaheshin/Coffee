<template>
  <div class="flex flex-col h-screen overflow-hidden bg-gradient-to-br from-coffee-50 to-coffee-100">
    <!-- Progress Bar - Fixed at top -->
    <div class="bg-white shadow-md p-3 flex-shrink-0 border-b border-coffee-200">
      <div class="max-w-screen-2xl mx-auto px-4">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-semibold text-coffee-700">Progress</span>
          <span class="text-xs font-semibold text-coffee-600">{{ feedbackStore.progress }}%</span>
        </div>
        <div class="w-full bg-coffee-100 rounded-full h-2">
          <div 
            class="progress-bar"
            :style="{ width: feedbackStore.progress + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Welcome Message Before First Question -->


  <!-- Main Content - Side by Side Layout (No wasted space) -->
  <div v-if="feedbackStore.currentQuestion" class="flex-1 overflow-hidden">
      <div class="max-w-screen-2xl mx-auto h-full flex gap-4 p-4">
        <!-- LEFT: Options Panel (65% width) -->
        <div class="flex-[0_0_65%] bg-white rounded-2xl shadow-xl overflow-y-auto">
          <QuestionPanel
            :question="feedbackStore.currentQuestion"
            :is-loading="feedbackStore.isLoading"
            @select-option="handleOptionSelect"
            @text-input="handleTextInput"
          />
        </div>
        <!-- RIGHT: Chat/Voice Panel (35% width) -->
        <div class="flex-[0_0_35%] flex flex-col">
          <VoicePanel
            :question="feedbackStore.currentQuestion"
            :is-submitting="feedbackStore.isLoading"
            @voice-answer="handleVoiceAnswer"
          />
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="feedbackStore.isLoading" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <svg class="animate-spin h-12 w-12 text-coffee-600 mx-auto mb-4" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-lg text-coffee-600">Loading question...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="feedbackStore.error" class="max-w-2xl mx-auto">
      <div class="bg-red-50 border-2 border-red-300 rounded-xl p-6 text-center">
        <p class="text-red-800 mb-4">{{ feedbackStore.error }}</p>
        <button @click="handleRetry" class="btn-primary">
          Retry
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFeedbackStore } from '@/stores/feedback'
import QuestionPanel from '@/components/QuestionPanel.vue'
import VoicePanel from '@/components/VoicePanel.vue'

import { useElevenLabsTTS } from '@/composables/useElevenLabsTTS'

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
})

const router = useRouter()
const feedbackStore = useFeedbackStore()

const { speak: speakTTS } = useElevenLabsTTS()


onMounted(async () => {
  // If no current session, redirect to home
  if (!feedbackStore.session || feedbackStore.session.id !== parseInt(props.sessionId)) {
    router.push({ name: 'home' })
    return
  }
  // Play welcome message via TTS, then first question
  await speakTTS('Welcome to ABC Coffee Testing. You can speak with a representative or select an option from the left side.')
  // Speak the first question if available
  if (feedbackStore.currentQuestion && feedbackStore.currentQuestion.text) {
    await speakTTS(feedbackStore.currentQuestion.text)
    // Start the mic after first question is spoken
    // Use event bus or direct ref to VoicePanel if needed, but here we use window event
    window.dispatchEvent(new CustomEvent('start-mic'))
  }
})

const handleOptionSelect = async (option) => {
  try {
    const result = await feedbackStore.submitAnswer(
      feedbackStore.currentQuestion.id,
      option,
      'click',
      1.0
    )

    // Check if questionnaire is complete
    if (!result.next_question) {
      await feedbackStore.completeSession()
      router.push({ name: 'complete', params: { sessionId: props.sessionId } })
    }
  } catch (error) {
    console.error('Failed to submit answer:', error)
  }
}

const handleTextInput = async (text) => {
  if (!text.trim()) return

  try {
    const result = await feedbackStore.submitAnswer(
      feedbackStore.currentQuestion.id,
      text,
      'text',
      1.0
    )

    // Check if questionnaire is complete
    if (!result.next_question) {
      await feedbackStore.completeSession()
      router.push({ name: 'complete', params: { sessionId: props.sessionId } })
    }
  } catch (error) {
    console.error('Failed to submit answer:', error)
  }
}

const handleVoiceAnswer = async (transcript, confidence) => {
  if (!transcript.trim()) return

  try {
    const result = await feedbackStore.submitAnswer(
      feedbackStore.currentQuestion.id,
      transcript,
      'voice',
      confidence
    )

    // Check if questionnaire is complete
    if (!result.next_question) {
      await feedbackStore.completeSession()
      router.push({ name: 'complete', params: { sessionId: props.sessionId } })
    }
  } catch (error) {
    console.error('Failed to submit answer:', error)
  }
}

const handleRetry = () => {
  router.push({ name: 'home' })
}
</script>
