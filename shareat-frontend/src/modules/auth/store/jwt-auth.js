import router from '@/router';

import { Login, Logout } from '../repositories/auth-repository';
import { getRouteFromSessionStorage, removeRouteFromSessionStorage } from '../helpers/auth-session-storage-helper';

const LOGIN_PAGE = '/login';

export default {
  namespaced: true,
  state: () => ({
    jwt: {
      accessToken: null,
      expires: null,
    },
  }),

  mutations: {
    SET_TOKEN: (state, { accessToken, expires }) => {
      const date = new Date(expires);
      const expiresIn = date.getTime();

      state.jwt = {
        accessToken,
        expires: expiresIn,
      };
    },

    REMOVE_TOKEN: (state) => {
      state.jwt = {
        accessToken: null,
        expires: null,
      };
    },
  },

  actions: {
    async LOGIN({ commit, dispatch }, { authData = null }) {
      let tokenData = null;

      tokenData = await Login(authData.login, authData.password);

      commit('SET_TOKEN', tokenData);

      //TODO: dispatch

      router.push(getRouteFromSessionStorage());
    },

    async REVOKE({ commit }) {
      await Logout();

      commit('CLEAR_TOKEN');

      removeRouteFromSessionStorage();

      router.push(LOGIN_PAGE);
    },
  },

  getters: {
    GET_ACCESS_TOKEN: (state) => state.jwt.accessToken,

    IS_ACCESS_TOKEN_VALID: (state) => (dateNow) => {
      if (!state.jwt.accessToken || !state.jwt.expires) return false;

      return dateNow < state.jwt.expires;
    },
  },
};
