import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: '',
    component: () => import('@/views/Login.vue'),
    meta: {
      not_login: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      not_login: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: {
      not_login: true
    }
  },
  {
    path: '/forum',
    name: 'Forum',
    component: () => import('@/views/Forum')
  },
  {
    path: '/forum/:board_num',
    name: 'Board',
    component: () => import('@/views/Board')
  },
  {
    path: '/forum/:board_num/:topic_num',
    name: 'Topic',
    component: () => import('@/views/Topic')
  },
  {
    path: '/refresh',
    name: 'Refresh',
    component: () => import('@/components/Refresh.vue')
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/components/NotFound.vue')
  },
  {
    path: '*',
    redirect: { name: 'NotFound' }
  }
];

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
});

export default router;
