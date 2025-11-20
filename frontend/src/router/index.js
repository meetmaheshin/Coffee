import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FeedbackView from '../views/FeedbackView.vue'
import CompletionView from '../views/CompletionView.vue'
import QuestionsAdmin from '../admin/QuestionsAdmin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/feedback/:sessionId',
      name: 'feedback',
      component: FeedbackView,
      props: true
    },
    {
      path: '/complete/:sessionId',
      name: 'complete',
      component: CompletionView,
      props: true
    },
    {
      path: '/admin/questions',
      name: 'admin-questions',
      component: QuestionsAdmin
    }
  ]
})

export default router
