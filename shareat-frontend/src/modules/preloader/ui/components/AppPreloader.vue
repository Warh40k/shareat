<template>
  <v-overlay color="color-gray-8" :value="SHOW_PRELOADER" style="z-index: 1000">
    <v-progress-circular :size="70" :width="6" color="main-color" indeterminate></v-progress-circular>
  </v-overlay>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'AppPreloader',
  computed: {
    ...mapGetters('preloader', ['SHOW_PRELOADER']),
  },
};
</script>
