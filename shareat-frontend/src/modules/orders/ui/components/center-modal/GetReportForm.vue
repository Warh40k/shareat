<template>
  <CenterModalContentWrapper>
    <template #default>
      <v-combobox
          color="main-color"
          v-model="select"
          :items="items"
          label="Тип отчета"
          outlined
          dense
        ></v-combobox>
        <v-btn small color="main-color" right class="white--text text" @click="onSubmit">
                Заказать
              </v-btn>
    </template>
  </CenterModalContentWrapper>
</template>

<script>
import { mapMutations } from 'vuex';
import ALERT_TYPES from '@/modules/alert/constants/alert-types';
import { CreateReport } from '../../../repositories/order-repository';

export default {
  name: 'GetReportForm',

  data() {
    return {
      items: [
          { value: 'sales', text: "Продажи"},
          { value: 'inventory', text: "Инвентаризация"},
          { value: 'active_orders', text: "Активные заказы"},
        ],
      select: null
    }
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),


    async onSubmit() {
      try {
        var report = {
          id: 0,
          type: this.items.find(item => item === this.select).value,
          key: "",
          date: new Date(),
          author_id: "2",
        }
        this.ADD_LOADER();
        await CreateReport(report);
        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Отчет успешно заказан! Вы можете увидеть и скачать его на вкладке "Отчеты"' });
        this.$emit('success');
      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      } finally {
        this.REMOVE_LOADER();
      }
    },
    cancel() {
      this.$emit('cancel');
    },
  },
};
</script>
