<template>
  <div class="admin-questions-flex">
    <div class="questions-list">
      <h2>Published Questions</h2>
      <div v-if="questions.length === 0" class="empty-list">No questions yet.</div>
      <ul>
        <li v-for="q in questions" :key="q.id" :class="{selected: selectedId === q.id}" @click="selectQuestion(q)">
          <div class="q-title">{{ q.text }}</div>
          <div class="q-id">ID: {{ q.id }}</div>
        </li>
      </ul>
      <button class="delete-all-btn" @click="deleteAllQuestions">Delete All Questions</button>
    </div>
    <div class="question-form">
      <h2>{{ editMode ? 'Edit Question' : 'Add New Question' }}</h2>
      <form @submit.prevent="saveQuestion">
        <div class="form-row">
          <label>Question Text</label>
          <input v-model="form.text" placeholder="Enter question text" required />
        </div>
        <div class="form-row">
          <label>Question ID</label>
          <input v-model="form.id" placeholder="Unique ID" required :disabled="editMode" />
        </div>
        <div class="form-row">
          <label>Question Type</label>
          <select v-model="form.type" required>
            <option value="">Select type</option>
            <option value="single_choice">Single Choice</option>
            <option value="multiple_choice">Multiple Choice</option>
            <option value="rating">Rating</option>
            <option value="open">Open Text</option>
            <option value="intro">Intro</option>
          </select>
        </div>
        <div class="form-row">
          <label>Category</label>
          <input v-model="form.category" placeholder="e.g. Flavor" />
        </div>
        <div class="form-row">
          <label>Order Index</label>
          <input v-model.number="form.order_index" type="number" placeholder="0" />
        </div>
        <div class="option-groups">
          <div v-for="(group, gIdx) in form.optionGroups" :key="gIdx" class="option-group">
            <div class="form-row">
              <label>Option Group Title</label>
              <input v-model="group.title" placeholder="e.g. Flavor Intensity" required />
              <button type="button" class="remove-group-btn" @click="removeOptionGroup(gIdx)">Remove Group</button>
            </div>
            <div class="form-row">
              <label>Options (comma separated)</label>
              <textarea v-model="group.optionsRaw" rows="3" placeholder="e.g. Weak, Mild, Pleasant, Prominent, Strong, Overbearing, Medium" class="options-textarea"></textarea>
            </div>
          </div>
          <button type="button" class="add-group-btn" @click="addOptionGroup">Add Option Group</button>
        </div>
        <div class="form-actions">
          <button type="submit">{{ editMode ? 'Update' : 'Add' }}</button>
          <button type="button" @click="resetForm">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const questions = ref([])
const loading = ref(false)
const error = ref('')
const editMode = ref(false)
const selectedId = ref(null)
const form = ref({
  id: '',
  text: '',
  type: '',
  category: '',
  order_index: 0,
  optionGroups: [] // [{ title: '', optionsRaw: '' }]
})

function blankForm() {
  return { 
    id: '', 
    text: '', 
    type: '', 
    category: '',
    order_index: 0,
    optionGroups: [] 
  }
}

async function fetchQuestions() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get('/api/admin/questions')
    questions.value = (res.data || []).map(q => ({
      ...q,
      optionGroups: q.optionGroups || []
    }))
  } catch (e) {
    error.value = e.message || 'Failed to load questions.'
  } finally {
    loading.value = false
  }
}

function selectQuestion(q) {
  selectedId.value = q.id
  editMode.value = true
  form.value = {
    id: q.id,
    text: q.text,
    type: q.type || '',
    category: q.category || '',
    order_index: q.order_index || 0,
    optionGroups: (q.optionGroups || []).map(group => ({
      title: group.title || '',
      optionsRaw: (group.options || []).join(', ')
    }))
  }
}

function resetForm() {
  editMode.value = false
  selectedId.value = null
  form.value = blankForm()
}

function addOptionGroup() {
  form.value.optionGroups.push({ title: '', optionsRaw: '' })
}
function removeOptionGroup(idx) {
  form.value.optionGroups.splice(idx, 1)
}
function addOption(gIdx) {
  form.value.optionGroups[gIdx].options.push('')
}
function removeOption(gIdx, oIdx) {
  form.value.optionGroups[gIdx].options.splice(oIdx, 1)
}

async function saveQuestion() {
  loading.value = true
  error.value = ''
  try {
    // Convert optionGroups to the format expected by backend
    const optionGroups = form.value.optionGroups.map(group => ({
      title: group.title,
      options: (group.optionsRaw || '').split(',').map(opt => opt.trim()).filter(Boolean)
    })).filter(group => group.title || group.options.length > 0)
    
    const payload = {
      id: form.value.id,
      text: form.value.text,
      type: form.value.type,
      optionGroups: optionGroups,
      category: form.value.category,
      order_index: form.value.order_index
    }
    if (editMode.value) {
      await axios.put(`/api/admin/questions/${form.value.id}`, payload)
    } else {
      await axios.post('/api/admin/questions', payload)
    }
    await fetchQuestions()
    resetForm()
  } catch (e) {
    error.value = e.message || 'Failed to save question.'
  } finally {
    loading.value = false
  }
}

async function deleteQuestion(id) {
  if (!confirm('Delete this question?')) return
  loading.value = true
  error.value = ''
  try {
    await axios.delete(`/api/admin/questions/${id}`)
    await fetchQuestions()
    resetForm()
  } catch (e) {
    error.value = e.message || 'Failed to delete question.'
  } finally {
    loading.value = false
  }
}

async function deleteAllQuestions() {
  if (!confirm('Delete ALL questions? This cannot be undone.')) return
  loading.value = true
  error.value = ''
  try {
    for (const q of questions.value) {
      await axios.delete(`/api/admin/questions/${q.id}`)
    }
    await fetchQuestions()
    resetForm()
  } catch (e) {
    error.value = e.message || 'Failed to delete all questions.'
  } finally {
    loading.value = false
  }
}

fetchQuestions()
</script>

<style scoped>
.admin-questions-flex {
  display: flex;
  gap: 2rem;
  max-width: 1200px;
  margin: 2rem auto;
  background: #f9f6f2;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px #0001;
}
.questions-list {
  width: 320px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px #0001;
  padding: 1rem;
  min-height: 400px;
}
.questions-list h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}
.questions-list ul {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem 0;
}
.questions-list li {
  padding: 0.7rem 0.5rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  background: #f7f7fa;
  border: 1px solid #eee;
  transition: background 0.2s;
}
.questions-list li.selected {
  background: #e0e7ff;
  border-color: #b3bcf5;
}
.q-title {
  font-weight: 500;
}
.q-id {
  font-size: 0.9em;
  color: #888;
}
.delete-all-btn {
  background: #ffebee;
  color: #b71c1c;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1.2rem;
  margin-top: 1rem;
  cursor: pointer;
}
.empty-list {
  color: #aaa;
  margin-bottom: 1rem;
}
.question-form {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px #0001;
  padding: 2rem 2.5rem;
}
.question-form h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
}
.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.form-row label {
  width: 180px;
  font-weight: 500;
  color: #6f4e37;
}
.form-row input, .form-row select {
  flex: 1;
  padding: 0.4rem 0.7rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.option-groups {
  margin-bottom: 1.5rem;
}
.option-group {
  background: #f7f7fa;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #eee;
}
.add-group-btn, .add-option-btn, .remove-group-btn, .remove-option-btn {
  margin-top: 0.5rem;
  margin-right: 0.5rem;
  background: #e0e7ff;
  border: none;
  border-radius: 5px;
  padding: 0.3rem 0.9rem;
  cursor: pointer;
}
.remove-group-btn, .remove-option-btn {
  background: #ffebee;
  color: #b71c1c;
}
.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.error {
  color: #b71c1c;
  margin-bottom: 1rem;
}
.loading {
  color: #888;
  margin-bottom: 1rem;
}
.options-textarea {
  flex: 1;
  min-width: 0;
  min-height: 60px;
  font-size: 1em;
  padding: 0.5rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-bottom: 0.5rem;
}
</style>
