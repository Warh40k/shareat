<template>
  <div>
    <v-navigation-drawer
      v-model="openMenu"
      color="main-color"
      app
      :mini-variant="isMobileMode ? false : !GET_MENU_STATUS"
      :width="isMobileMode ? '100%' : 256"
      :permanent="!isMobileMode"
      :temporary="isMobileMode">
      <DrawerNavigation
        :is-open="isMobileMode ? false : !GET_MENU_STATUS"
        :nav-items="navItems"
        @toggle:menu="TOGGLE_MENU" />
    </v-navigation-drawer>

    <v-app-bar elevation="1" height="56" max-height="56" min-height="56" color="white" app>
      <template v-if="isMobileMode">
        <v-app-bar-nav-icon @click="TOGGLE_MENU">
          <v-icon color="primary1">mdi-menu</v-icon>
        </v-app-bar-nav-icon>
      </template>

      <!-- <AppLogo /> -->

      <v-spacer></v-spacer>

      <v-btn tile depressed small class="white--text" color="main-color" @click="logout"> Выйти </v-btn>
    </v-app-bar>

    <v-main>
      <slot />
    </v-main>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import DrawerNavigation from '@/core/ui/components/DrawerNavigation.vue';
import { Logout } from '@/modules/auth/repositories/auth-repository';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';
import SidebarContentWrapper from '@/core/ui/components/shared/sidebar-modal/SidebarContentWrapper.vue';

export default {
  name: 'DefaultLayout',

  components: {
    DrawerNavigation,
    SidebarContentWrapper,
  },

  data() {
    return {
      navItems: [
        {
          title: 'Каталог',
          icon: 'mdi-animation',
          link: '/catalog',
        },
        {
          title: 'Заказы',
          icon: 'mdi-order-bool-descending-variant',
          link: '/orders',
        },
        {
          title: 'Личный кабинет',
          icon: 'mdi-account',
          link: '/profile',
        },
        {
          title: 'Администрирование',
          icon: 'mdi-cog',
          link: '/admin',
        },
      ],
    };
  },

  computed: {
    ...mapGetters(['GET_MENU_STATUS']),

    isMobileMode() {
      return this.$vuetify.breakpoint.width < 768;
    },

    openMenu: {
      get() {
        return this.GET_MENU_STATUS;
      },
      set(value) {
        this.SET_STATUS(value);
      },
    },
  },
  created() {
    if (this.isMobileMode) {
      this.SET_STATUS(false);
    }
  },

  methods: {
    ...mapMutations(['TOGGLE_MENU', 'SET_STATUS']),
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('auth', ['REMOVE_AUTH_DATA']),

    async logout() {
      try {
        await Logout();

        this.REMOVE_AUTH_DATA();

        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Успешный выход' });

        this.$router.push({ name: 'login' });
      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      }
    },
  },
};
</script>

<style lang="scss" scoped></style>
