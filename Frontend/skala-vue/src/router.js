// router.js - components 폴더 사용으로 수정
import { createRouter, createWebHistory } from 'vue-router'
import DisguiseMenu from './components/DisguiseMenu.vue'  // components 폴더로 변경
import DisguisePage from './components/DisguisePage.vue'  // components 폴더로 변경

const routes = [
  {
    path: '/',
    name: 'DisguiseMenu',
    component: DisguiseMenu,
  },
  {
    path: '/disguise',
    name: 'Disguise', 
    component: DisguisePage,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
