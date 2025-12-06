import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Projects',
      component: () => import('./views/ProjectsView.vue')
    },
    {
      path: '/item/:id',
      name: 'ItemDetail',
      component: () => import('./views/ItemDetailView.vue')
    },
    {
      path: '/user-panel',
      name: 'UserPanel',
      component: () => import('./views/UserPanelView.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('./views/LoginView.vue')
    }
  ],
})

export default router
