import { ref, onMounted, onUnmounted } from 'vue'

export function useSpeechRecognition() {
  const isListening = ref(false)
  const transcript = ref('')
  const confidence = ref(0)
  const isSupported = ref(false)
  const error = ref(null)
  
  let recognition = null
  let finalTranscript = ''
  let shouldKeepListening = false  // Flag to control continuous listening

  onMounted(() => {
    // Check if browser supports Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    
    if (SpeechRecognition) {
      isSupported.value = true
      recognition = new SpeechRecognition()
      
      recognition.continuous = true  // Keep listening
      recognition.interimResults = true
      recognition.lang = 'en-US'
      recognition.maxAlternatives = 1

      recognition.onstart = () => {
        isListening.value = true
        transcript.value = ''
        finalTranscript = ''
        error.value = null
      }

      recognition.onresult = (event) => {
        let interimTranscript = ''
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i]
          
          if (result.isFinal) {
            finalTranscript += result[0].transcript + ' '
            confidence.value = result[0].confidence
          } else {
            interimTranscript += result[0].transcript
          }
        }
        
        transcript.value = (finalTranscript + interimTranscript).trim()
      }

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error)
        error.value = event.error
        isListening.value = false
        
        // Auto-retry on certain errors
        if (event.error === 'no-speech' || event.error === 'audio-capture') {
          console.log('Recoverable error, will retry on next start')
          error.value = null  // Clear error so auto-restart works
        } else if (event.error === 'network') {
          console.log('Network error, attempting recovery...')
          setTimeout(() => {
            if (shouldKeepListening) {
              error.value = null
              try {
                recognition.start()
              } catch (e) {
                console.log('Network recovery failed:', e)
              }
            }
          }, 1000)
        }
      }

      recognition.onend = () => {
        console.log('Recognition ended. shouldKeepListening:', shouldKeepListening, 'error:', error.value)
        isListening.value = false
        
        // Auto-restart if we want to keep listening (unless there's an error)
        if (shouldKeepListening && !error.value) {
          console.log('Recognition ended, auto-restarting in 300ms...')
          setTimeout(() => {
            if (shouldKeepListening && !isListening.value && recognition) {
              try {
                console.log('Attempting to restart recognition...')
                finalTranscript = ''  // Clear previous transcript
                recognition.start()
                console.log('Recognition restarted successfully')
              } catch (err) {
                console.log('Auto-restart failed:', err.message)
                // If it fails, try one more time after a longer delay
                if (err.message.includes('already started')) {
                  console.log('Recognition already started, skipping')
                } else {
                  setTimeout(() => {
                    try {
                      recognition.start()
                    } catch (e) {
                      console.error('Second restart attempt failed:', e)
                    }
                  }, 500)
                }
              }
            }
          }, 300)  // Increased delay to 300ms for better reliability
        }
      }
    } else {
      isSupported.value = false
      error.value = 'Speech recognition is not supported in this browser'
    }
  })

  onUnmounted(() => {
    if (recognition) {
      recognition.abort()
    }
  })

  const start = () => {
    console.log('Start called. isListening:', isListening.value, 'recognition exists:', !!recognition)
    if (recognition && !isListening.value) {
      shouldKeepListening = true  // Enable auto-restart
      error.value = null  // Clear any previous errors
      try {
        recognition.start()
        console.log('Recognition started successfully')
      } catch (err) {
        console.error('Error starting recognition:', err)
        // If already started, just set the flag
        if (err.message.includes('already started')) {
          console.log('Recognition already running, setting flags')
          isListening.value = true
          shouldKeepListening = true
        } else {
          error.value = err.message
        }
      }
    } else if (isListening.value) {
      console.log('Already listening, just ensuring flags are set')
      shouldKeepListening = true
    }
  }

  const stop = () => {
    shouldKeepListening = false  // Disable auto-restart
    if (recognition && isListening.value) {
      recognition.stop()
    }
  }

  const reset = () => {
    console.log('Reset called')
    transcript.value = ''
    finalTranscript = ''
    confidence.value = 0
    error.value = null
  }
  
  const forceRestart = () => {
    console.log('Force restart called')
    if (recognition) {
      shouldKeepListening = false
      if (isListening.value) {
        recognition.stop()
      }
      setTimeout(() => {
        shouldKeepListening = true
        finalTranscript = ''
        transcript.value = ''
        try {
          recognition.start()
          console.log('Force restart successful')
        } catch (err) {
          console.error('Force restart failed:', err)
        }
      }, 500)
    }
  }

  return {
    isListening,
    transcript,
    confidence,
    isSupported,
    error,
    start,
    stop,
    reset,
    forceRestart
  }
}

export function useTextToSpeech() {
  const isSpeaking = ref(false)
  const isSupported = ref(false)
  
  let synth = null

  onMounted(() => {
    synth = window.speechSynthesis
    isSupported.value = !!synth
  })

  const speak = (text, options = {}) => {
    if (!synth || !text) return

    // Cancel any ongoing speech
    synth.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = options.lang || 'en-US'
    utterance.rate = options.rate || 0.9
    utterance.pitch = options.pitch || 1
    utterance.volume = options.volume || 1

    utterance.onstart = () => {
      isSpeaking.value = true
    }

    utterance.onend = () => {
      isSpeaking.value = false
    }

    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event)
      isSpeaking.value = false
    }

    synth.speak(utterance)
  }

  const cancel = () => {
    if (synth) {
      synth.cancel()
      isSpeaking.value = false
    }
  }

  return {
    isSpeaking,
    isSupported,
    speak,
    cancel
  }
}
