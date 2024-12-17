import { createRouter, createWebHistory } from 'vue-router';
import LatestVideo from '@/components/LatestVideo.vue'; 

const routes = [
  {
    path: '/',
    redirect: '/today/api/videos/latest',
  },
  {
    path: '/today/api/videos/latest',
    component: LatestVideo, 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
