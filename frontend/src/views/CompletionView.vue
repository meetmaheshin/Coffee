<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="max-w-4xl w-full">
      
      <!-- Success Animation -->
      <div class="text-center mb-8 animate-fade-in">
        <div class="inline-block text-8xl mb-6 animate-bounce-slow">
          🎉
        </div>
        <h1 class="text-5xl font-display font-bold text-coffee-700 mb-4">
          Feedback Complete!
        </h1>
        <p class="text-xl text-coffee-600">
          Thank you for your valuable insights
        </p>
      </div>

      <!-- Summary Card -->
      <div v-if="report" class="bg-white rounded-3xl shadow-2xl p-8 mb-6 animate-slide-in">
        <h2 class="text-2xl font-bold text-coffee-800 mb-6 text-center">
          Session Summary
        </h2>

        <div class="grid grid-cols-2 gap-4 mb-6">
          <div class="p-4 bg-coffee-50 rounded-xl">
            <p class="text-sm text-coffee-600 mb-1">Tester</p>
            <p class="text-lg font-semibold text-coffee-800">
              {{ report.tester_name || 'Anonymous' }}
            </p>
          </div>
          <div class="p-4 bg-coffee-50 rounded-xl">
            <p class="text-sm text-coffee-600 mb-1">Coffee Sample</p>
            <p class="text-lg font-semibold text-coffee-800">
              {{ report.coffee_sample || 'Not specified' }}
            </p>
          </div>
          <div class="p-4 bg-coffee-50 rounded-xl">
            <p class="text-sm text-coffee-600 mb-1">Questions Answered</p>
            <p class="text-lg font-semibold text-coffee-800">
              {{ report.total_answers }}
            </p>
          </div>
          <div class="p-4 bg-coffee-50 rounded-xl">
            <p class="text-sm text-coffee-600 mb-1">Duration</p>
            <p class="text-lg font-semibold text-coffee-800">
              {{ duration }}
            </p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center mt-8">
          <button
            @click="handleViewReport"
            class="btn-primary"
          >
            📄 View Full Report
          </button>
          <button
            @click="handleDownloadCSV"
            :disabled="isDownloading"
            class="btn-primary"
          >
            {{ isDownloading ? '⏳ Exporting...' : '📥 Download CSV' }}
          </button>
          <button
            @click="handleNewSession"
            class="btn-secondary"
          >
            ☕ Start New Session
          </button>
        </div>
        
        <!-- Download Success Message -->
        <div v-if="downloadSuccess" class="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-xl text-center animate-fade-in">
          ✅ CSV exported successfully! Check the <code class="bg-green-200 px-2 py-1 rounded">backend/exports</code> folder.
        </div>
      </div>

      <!-- Report Details (Expandable) -->
      <div v-if="showDetails && report" class="bg-white rounded-3xl shadow-2xl p-8 animate-fade-in">
        <h3 class="text-xl font-bold text-coffee-800 mb-4">
          Detailed Responses
        </h3>
        
        <div class="space-y-4 max-h-96 overflow-y-auto">
          <div
            v-for="(answer, index) in report.answers"
            :key="index"
            class="p-4 bg-coffee-50 rounded-xl"
          >
            <p class="text-sm text-coffee-600 mb-1">
              Question {{ index + 1 }}
            </p>
            <p class="text-base font-medium text-coffee-800">
              {{ answer.answer }}
            </p>
            <div class="flex items-center gap-3 mt-2 text-xs text-coffee-500">
              <span class="px-2 py-1 bg-white rounded-full">
                {{ answer.type }}
              </span>
              <span v-if="answer.confidence">
                {{ Math.round(answer.confidence * 100) }}% confidence
              </span>
            </div>
          </div>
        </div>

        <button
          @click="showDetails = false"
          class="mt-6 w-full btn-secondary"
        >
          Hide Details
        </button>
      </div>

      <!-- Show Details Button -->
      <div v-else-if="report" class="text-center">
        <button
          @click="showDetails = true"
          class="text-coffee-600 hover:text-coffee-700 underline"
        >
          Show detailed responses
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center">
        <svg class="animate-spin h-12 w-12 text-coffee-600 mx-auto mb-4" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-lg text-coffee-600">Generating report...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFeedbackStore } from '@/stores/feedback'
import confetti from 'canvas-confetti'

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
})

const router = useRouter()
const feedbackStore = useFeedbackStore()

const report = ref(null)
const isLoading = ref(true)
const showDetails = ref(false)
const isDownloading = ref(false)
const downloadSuccess = ref(false)

const duration = computed(() => {
  if (!report.value || !report.value.start_time || !report.value.end_time) {
    return 'N/A'
  }
  
  const start = new Date(report.value.start_time)
  const end = new Date(report.value.end_time)
  const diff = Math.floor((end - start) / 1000) // seconds
  
  const minutes = Math.floor(diff / 60)
  const seconds = diff % 60
  
  return `${minutes}m ${seconds}s`
})

onMounted(async () => {
  // Trigger confetti animation
  confetti({
    particleCount: 100,
    spread: 70,
    origin: { y: 0.6 }
  })

  // Load report
  try {
    report.value = await feedbackStore.getReport(parseInt(props.sessionId))
  } catch (error) {
    console.error('Failed to load report:', error)
  } finally {
    isLoading.value = false
  }
})

const handleViewReport = () => {
  showDetails.value = !showDetails.value
}

const handleDownloadCSV = async () => {
  isDownloading.value = true
  downloadSuccess.value = false
  
  try {
    const result = await feedbackStore.exportToCSV(parseInt(props.sessionId))
    downloadSuccess.value = true
    
    // Show success message for 5 seconds
    setTimeout(() => {
      downloadSuccess.value = false
    }, 5000)
  } catch (error) {
    console.error('Failed to export CSV:', error)
    alert('Failed to export CSV. Please try again.')
  } finally {
    isDownloading.value = false
  }
}

const handleNewSession = () => {
  feedbackStore.resetSession()
  router.push({ name: 'home' })
}
</script>
