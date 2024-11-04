<template>
  <v-app>
    <AppLayout>
      <router-view />
    </AppLayout>
    <AppPreloader />
    <AppAlert />
  </v-app>
</template>

<script>
import AppLayout from '@/core/ui/layouts/AppLayout.vue';
import AppPreloader from '@/modules/preloader/ui/components/AppPreloader.vue';
import AppAlert from '@/modules/alert/ui/components/AppAlert.vue';

export default {
  name: 'App',

  components: {
    AppLayout,
    AppPreloader,
    AppAlert,
  },
};
</script>
