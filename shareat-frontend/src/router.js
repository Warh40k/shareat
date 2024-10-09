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
      name: 'catalog',
    },
  },
  {
    path: '/catalog',
    name: 'catalog',
    component: () => import(/* webpackChunkName: "catalog" */ '@/modules/catalog/ui/views/CatalogView.vue'),
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
    component: () => import(/* webpackChunkName: "register" */ '@/modules/register/ui/views/RegisterView.vue'),
    meta: {
      layout: 'EmptyLayout',
    },
  },

  // каталог
  {
    path: '/category/cars',
    name: 'cars',
    component: () => import(/* webpackChunkName: "cars" */ '@/modules/catalog/ui/views/CarsCategoryView.vue'),
    meta: {
      isProtected: true,
    },
  },
  {
    path: '/computers',
    name: 'computers',
    component: () => import(/* webpackChunkName: "computers" */ '@/modules/catalog/ui/views/ComputersCategoryView.vue'),
    meta: {
      isProtected: true,
    },
  },
  {
    path: '/sport',
    name: 'sport',
    component: () => import(/* webpackChunkName: "sport" */ '@/modules/catalog/ui/views/SportsCategoryView.vue'),
    meta: {
      isProtected: true,
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
