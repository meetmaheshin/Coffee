import { ref } from 'vue'
import api from '@/services/api'

export function useElevenLabsTTS() {
  const isSpeaking = ref(false)
  const error = ref(null)
  let audio = null

  // Set your preferred ElevenLabs female voice ID here
  const DEFAULT_FEMALE_VOICE_ID = 'EIsgvJT3rwoPvRFG6c4n'

  const speak = async (text, voice_id = null) => {
    if (!text) return Promise.resolve()
    isSpeaking.value = true
    error.value = null
    return new Promise(async (resolve, reject) => {
      try {
        // Cancel any ongoing audio
        if (audio) {
          audio.pause()
          audio.currentTime = 0
        }
        // Use default female voice if none provided
        const finalVoiceId = voice_id || DEFAULT_FEMALE_VOICE_ID
        const response = await api.post('/api/tts', { text, voice_id: finalVoiceId }, { responseType: 'blob' })
        const blob = response.data
        const url = URL.createObjectURL(blob)
        audio = new Audio(url)
        audio.onended = () => {
          isSpeaking.value = false
          URL.revokeObjectURL(url)
          resolve()
        }
        audio.onerror = (e) => {
          isSpeaking.value = false
          error.value = 'Audio playback error'
          URL.revokeObjectURL(url)
          reject(error.value)
        }
        audio.play()
      } catch (err) {
        isSpeaking.value = false
        error.value = err.message || 'TTS error'
        reject(error.value)
      }
    })
  }

  const cancel = () => {
    if (audio) {
      audio.pause()
      audio.currentTime = 0
      isSpeaking.value = false
    }
  }

  return {
    isSpeaking,
    error,
    speak,
    cancel
  }
}
