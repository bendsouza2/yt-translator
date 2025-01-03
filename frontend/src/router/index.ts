import { createRouter, createWebHistory } from 'vue-router';
import LatestVideo from '@/components/LatestVideo.vue'; 
import UploadTimer from '@/components/UploadTimer.vue';

const routes = [
  {
    path: '/',
    redirect: '/today/videos/latest',
  },
  {
    path: '/today/videos/latest',
    component: LatestVideo, 
  },
  {
    path: '/today/videos/next',
    component: UploadTimer
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
