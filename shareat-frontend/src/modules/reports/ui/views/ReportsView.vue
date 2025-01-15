<template>
  <v-container color style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col v-if="$route.name == 'reports'" cols="12">
        <v-row>
          <v-col cols="12">
            <h1 class="text-h6 text-sm-h5 font-weight-bold">Заказанные отчеты</h1>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <ReportsListView />
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12">
        <router-view></router-view>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ReportsListView from '../views/ReportsListView.vue';

export default {
  name: 'ReportsView',

  components: {
    ReportsListView,
  },
};
</script>

<style></style>
