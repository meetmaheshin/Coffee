import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useFeedbackStore = defineStore('feedback', () => {
  const session = ref(null)
  const currentQuestion = ref(null)
  const answers = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const totalQuestions = ref(15) // Approximate based on question flow

  const progress = computed(() => {
    if (!totalQuestions.value) return 0
    return Math.round((answers.value.length / totalQuestions.value) * 100)
  })

  async function startSession(testerName, coffeeSample) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post('/api/sessions/start', {
        tester_name: testerName,
        coffee_sample: coffeeSample
      })
      
      session.value = response.data
      currentQuestion.value = response.data.current_question
      answers.value = []
      
      return session.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function submitAnswer(questionId, answerText, answerType = 'voice', confidenceScore = null) {
    if (!session.value) {
      throw new Error('No active session')
    }

    isLoading.value = true
    error.value = null

    try {
      const response = await api.post('/api/feedback/answer', {
        session_id: session.value.id,
        question_id: questionId,
        answer_text: answerText,
        answer_type: answerType,
        confidence_score: confidenceScore
      })

      answers.value.push({
        question_id: questionId,
        answer_text: answerText,
        timestamp: new Date().toISOString()
      })

      currentQuestion.value = response.data.next_question

      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function completeSession(notes = '') {
    if (!session.value) {
      throw new Error('No active session')
    }

    isLoading.value = true
    error.value = null

    try {
      const response = await api.post(`/api/sessions/${session.value.id}/complete`, {
        notes
      })

      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function getReport(sessionId) {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.get(`/api/reports/${sessionId}`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function exportToCSV(sessionId) {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.post(`/api/sessions/${sessionId}/export-csv`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function resetSession() {
    session.value = null
    currentQuestion.value = null
    answers.value = []
    error.value = null
  }

  return {
    session,
    currentQuestion,
    answers,
    isLoading,
    error,
    progress,
    startSession,
    submitAnswer,
    completeSession,
    getReport,
    exportToCSV,
    resetSession
  }
})
