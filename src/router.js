import { createRouter, createWebHistory } from 'vue-router'
import ProjectsView from './views/ProjectsView.vue'
import ItemDetailView from './views/ItemDetailView.vue'
import UserPanelView from './views/UserPanelView.vue'
import LoginView from './views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Projects',
      component: ProjectsView
    },
    {
      path: '/item/:id',
      name: 'ItemDetail',
      component: ItemDetailView
    },
    {
      path: '/user-panel',
      name: 'UserPanel',
      component: UserPanelView
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    }
  ],
})

export default router
