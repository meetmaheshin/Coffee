<template>
  <div class="p-6 h-full flex flex-col">
    <!-- Question Header -->
    <div class="mb-6 flex-shrink-0">
      <div v-if="question.category" class="inline-block px-3 py-1 bg-coffee-100 text-coffee-700 rounded-full text-xs font-semibold mb-3">
        {{ question.category }}
      </div>
      <h2 class="text-2xl md:text-3xl font-bold text-coffee-800 leading-tight">
        {{ question.text }}
      </h2>
    </div>

    <!-- Question Type: Single/Multiple Choice - Grid layout, compact -->
    <div v-if="question.type === 'single_choice' || question.type === 'multiple_choice'" 
         class="flex-1 overflow-y-auto">
      <!-- Display option groups if available -->
      <div v-if="question.optionGroups && question.optionGroups.length > 0">
        <div v-for="(group, groupIndex) in question.optionGroups" :key="groupIndex" class="mb-6">
          <h3 v-if="group.title" class="text-lg font-semibold text-coffee-700 mb-3 border-b border-coffee-200 pb-2">
            {{ group.title }}
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <button
              v-for="option in group.options"
              :key="option"
              @click="handleOptionClick(option)"
              :disabled="isLoading"
              class="bg-gradient-to-br from-white to-coffee-50 rounded-lg px-4 py-3 shadow-md hover:shadow-xl 
                     border-2 border-transparent hover:border-coffee-400
                     transition-all duration-200 cursor-pointer transform hover:scale-105
                     active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed text-left
                     flex items-center justify-between min-h-[60px]"
              :class="{ 'border-coffee-600 bg-coffee-100 ring-2 ring-coffee-500': selectedOptions.includes(option) }"
            >
              <span class="text-sm md:text-base font-semibold text-coffee-800 flex-1">{{ option }}</span>
              <span v-if="selectedOptions.includes(option)" class="text-xl ml-2">✓</span>
            </button>
          </div>
        </div>
      </div>
      <!-- Fallback to flat options display -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 pb-4">
        <button
          v-for="option in question.options"
          :key="option"
          @click="handleOptionClick(option)"
          :disabled="isLoading"
          class="bg-gradient-to-br from-white to-coffee-50 rounded-lg px-4 py-3 shadow-md hover:shadow-xl 
                 border-2 border-transparent hover:border-coffee-400
                 transition-all duration-200 cursor-pointer transform hover:scale-105
                 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed text-left
                 flex items-center justify-between min-h-[60px]"
          :class="{ 'border-coffee-600 bg-coffee-100 ring-2 ring-coffee-500': selectedOptions.includes(option) }"
        >
          <span class="text-sm md:text-base font-semibold text-coffee-800 flex-1">{{ option }}</span>
          <span v-if="selectedOptions.includes(option)" class="text-xl ml-2">✓</span>
        </button>
      </div>

      <!-- Confirm button for multiple choice -->
      <div v-if="question.type === 'multiple_choice' && selectedOptions.length > 0" 
           class="sticky bottom-0 bg-white pt-4 border-t border-coffee-200">
        <button
          @click="handleConfirmMultiple"
          :disabled="isLoading"
          class="btn-primary w-full text-lg py-3"
        >
          ✓ Confirm {{ selectedOptions.length }} Selection{{ selectedOptions.length > 1 ? 's' : '' }}
        </button>
      </div>
    </div>

    <!-- Question Type: Rating -->
    <div v-else-if="question.type === 'rating'" class="flex-1 flex flex-col justify-center py-4">
      <div class="flex justify-between items-center mb-3">
        <span class="text-xs md:text-sm text-coffee-600 font-medium">Low</span>
        <span class="text-xs md:text-sm text-coffee-600 font-medium">High</span>
      </div>
      
      <div class="grid grid-cols-5 sm:grid-cols-10 gap-2">
        <button
          v-for="rating in question.options"
          :key="rating"
          @click="emit('select-option', rating)"
          :disabled="isLoading"
          class="aspect-square rounded-lg md:rounded-xl text-base md:text-xl font-bold transition-all duration-300
                 border-2 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
          :class="[
            parseInt(rating) <= 3 ? 'border-red-300 hover:bg-red-100 text-red-700' :
            parseInt(rating) <= 7 ? 'border-yellow-300 hover:bg-yellow-100 text-yellow-700' :
            'border-green-300 hover:bg-green-100 text-green-700'
          ]"
        >
          {{ rating }}
        </button>
      </div>
    </div>

    <!-- Question Type: Open/Text Input -->
    <div v-else-if="question.type === 'open'" class="space-y-4">
      <textarea
        v-model="textInput"
        @keyup.ctrl.enter="handleTextSubmit"
        placeholder="Type your answer here... (Ctrl+Enter to submit)"
        rows="4"
        class="w-full px-4 py-3 rounded-xl border-2 border-coffee-200 focus:border-coffee-500 
               focus:ring-2 focus:ring-coffee-300 focus:outline-none transition-all resize-none"
      ></textarea>
      
      <button
        @click="handleTextSubmit"
        :disabled="isLoading || !textInput.trim()"
        class="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Submit Answer
      </button>
      
      <p class="text-sm text-coffee-500 text-center">
        Or use the voice button to speak your answer →
      </p>
    </div>

    <!-- Hint Text -->
    <div class="mt-6 p-4 bg-coffee-50 rounded-xl">
      <p class="text-sm text-coffee-600 text-center">
        💡 <strong>Pro tip:</strong> 
        {{ question.type === 'open' ? 'You can type or speak your answer' :
           question.type === 'rating' ? 'Click a number or say "I rate it 8"' :
           question.type === 'multiple_choice' ? 'Select multiple options then confirm' :
           'Click an option or speak your choice' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  question: {
    type: Object,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select-option', 'text-input'])

const selectedOptions = ref([])
const textInput = ref('')
const autoSubmitTimer = ref(null)

// Reset selections when question changes
watch(() => props.question.id, () => {
  selectedOptions.value = []
  textInput.value = ''
  if (autoSubmitTimer.value) {
    clearTimeout(autoSubmitTimer.value)
    autoSubmitTimer.value = null
  }
})

// Auto-submit multiple choice after 2 seconds of no changes
watch(selectedOptions, () => {
  if (props.question.type === 'multiple_choice' && selectedOptions.value.length > 0) {
    if (autoSubmitTimer.value) {
      clearTimeout(autoSubmitTimer.value)
    }
    autoSubmitTimer.value = setTimeout(() => {
      handleConfirmMultiple()
    }, 2000)
  }
}, { deep: true })

const handleOptionClick = (option) => {
  if (props.question.type === 'single_choice') {
    // Auto-advance immediately for single choice
    emit('select-option', option)
  } else if (props.question.type === 'multiple_choice') {
    const index = selectedOptions.value.indexOf(option)
    if (index > -1) {
      selectedOptions.value.splice(index, 1)
    } else {
      selectedOptions.value.push(option)
    }
  }
}

const handleConfirmMultiple = () => {
  if (selectedOptions.value.length > 0) {
    emit('select-option', selectedOptions.value.join(', '))
  }
}

const handleTextSubmit = () => {
  if (textInput.value.trim()) {
    emit('text-input', textInput.value.trim())
    textInput.value = ''
  }
}
</script>
