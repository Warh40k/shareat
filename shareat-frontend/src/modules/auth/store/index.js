export default {
  namespaced: true,

  state: () => ({
    userData: null,
  }),

  mutations: {
    SET_AUTH_DATA: (state, userData) => {
      state.userData = userData;
    },

    REMOVE_AUTH_DATA: (state) => {
      state.userData = null;
    },
  },

  getters: {
    GET_USER_DATA: (state) => state.userData,
  },
};
