import Vue from 'vue';
import Vuex from 'vuex';

import preloader from '@/modules/preloader/store';
import alert from '@/modules/alert/store';
import auth from '@/modules/auth/store';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    preloader,
    alert,
    auth,
  },
  state: () => ({
    openMenu: true,
  }),
  mutations: {
    TOGGLE_MENU: (state) => {
      state.openMenu = !state.openMenu;
    },

    SET_STATUS: (state, value) => {
      state.openMenu = value;
    },
  },

  getters: {
    GET_MENU_STATUS: (state) => state.openMenu,
  },
});
