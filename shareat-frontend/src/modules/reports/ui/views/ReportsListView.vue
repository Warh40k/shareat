<template>
  <v-container color style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col cols="12" sm="3">
            <v-text-field
              class="pt-0 mt-0"
              placeholder="Поиск по названию"
              prepend-inner-icon="mdi-magnify"
              color="main-color"
              clearable
              underlined>
            </v-text-field>
          </v-col>
        </v-row>
      </v-col>
      <template v-if="reportList.length == 0">
        <h3>Каталог пуст</h3>
      </template>
      <v-col v-for="report in reportList" :key="report.id" cols="12">
        <ReportCard :card-data="report" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex';
import ALERT_TYPES from '@/modules/alert/constants/alert-types';
import ReportCard from '../components/ReportCard.vue';
import { GetAllReports } from '../../../orders/repositories/order-repository';
export default {
  name: 'ReportsListView',

  components: {
    ReportCard,
  },
  data() {
    return {
      reportList: [],
    };
  },

  created() {
    this.fetchReports();
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),
    async fetchReports() {
      try {
        this.ADD_LOADER();

        const result = await GetAllReports();

        this.reportList = result.map((report) => ({
          id: report.id,
          type: "Активные заказы",
          key: report.key,
          date: new Date(new Date(report.date).setHours(new Date(report.date).getHours() + 3)).toLocaleString(),
          author: "manager@manager.ru",
        }));
      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      } finally {
        this.REMOVE_LOADER();
      }
    },
  },
};
</script>

<style></style>
