import Vue from 'vue';
import VueRouter from 'vue-router';
import loadLayout from '@/core/middleware/layout-middleware';
import checkProtection from '@/core/middleware/route-protection-middleware';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'main',
    redirect: {
      name: 'home',
    },
  },
  {
    path: '/home',
    name: 'home',
    component: () => import(/* webpackChunkName: "home" */ '@/modules/home/ui/views/HomeView.vue'),
    meta: {
      isProtected: true,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '@/modules/auth/ui/views/LoginView.vue'),
    meta: {
      layout: 'EmptyLayout',
    },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "login" */ '@/modules/register/ui/views/RegisterView.vue'),
    meta: {
      layout: 'EmptyLayout',
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach(async (to, from, next) => {
  await loadLayout(to);

  if (to.meta.isProtected) {
    await checkProtection(to, from, next);
  } else {
    next();
  }
});

export default router;
