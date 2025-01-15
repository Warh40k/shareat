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
    path: '/products',
    name: 'catalog',
    component: () => import(/* webpackChunkName: "catalog" */ '@/modules/catalog/ui/views/CatalogView.vue'),
    meta: {
      isProtected: true,
    },
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import(/* webpackChunkName: "admin" */ '@/modules/admin/ui/views/AdminView.vue'),
    meta: {
      isProtected: true,
    },
  },
  {
    path: '/orders',
    name: 'orders',
    component: () => import(/* webpackChunkName: "orders" */ '@/modules/orders/ui/views/OrdersView.vue'),
    meta: {
      isProtected: true,
    },
  },
  {
    path: '/reports',
    name: 'reports',
    component: () => import(/* webpackChunkName: "orders" */ '@/modules/reports/ui/views/ReportsView.vue'),
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
    path: '/products',
    name: 'products',
    component: () => import(/* webpackChunkName: "cars" */ '@/modules/catalog/ui/views/ProductsView.vue'),
    meta: {
      isProtected: true,
    },
  },
  {
    path: '/products/:id',
    name: 'product-details',
    component: () => import(/* webpackChunkName: "cars" */ '@/modules/catalog/ui/views/ProductDetailsView.vue'),
    meta: {
      isProtected: true,
    },
    props: (route) => ({
      product: route.params.product,
      id: parseInt(route.params.id, 10),
    }),
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import(/* webpackChunkName: "sport" */ '@/modules/user/ui/views/UserProfileView.vue'),
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
