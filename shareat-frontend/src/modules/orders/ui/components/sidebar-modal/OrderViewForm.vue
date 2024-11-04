<template>
  <ValidationObserver ref="update-user">
    <SidebarContentWrapper>
      <template #default>
        <v-row no-gutters>
          <v-col cols="12">
            <div class="field-label my-3">Идентификатор заказа: {{ order.id }}</div>
            <div class="field-label my-3">Название товара: {{ order.productName }}</div>
            <div class="field-label my-3">ФИО клиента: {{ order.clientFullName }}</div>
            <div class="field-label my-3">Статус: {{ statusesList.find((s) => s.id === order.statusId).name }}</div>
            <div class="field-label my-3">Дата начала: {{ new Date(order.startDate).toLocaleDateString() }}</div>
            <div class="field-label my-3">Дата окончания: {{ new Date(order.endDate).toLocaleDateString() }}</div>
            <div class="field-label my-3">Полная стоимость: {{ order.fullPrice }}</div>
            <div class="field-label my-3">TODO: навести красоту и выводить больше информации</div>
          </v-col>
        </v-row>
      </template>
      <template #footer>
        <v-btn color="pantone-cold-gray" tile outlined dense @click="cancel"> Закрыть </v-btn>
      </template>
    </SidebarContentWrapper>
  </ValidationObserver>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  name: 'OrderViewForm',

  props: {
    order: {
      type: Object,
      required: true,
    },
  },

  emits: ['cancel'],

  data() {
    return {
      statusesList: [
        {
          id: 0,
          name: 'Новый',
        },
        {
          id: 1,
          name: 'В аренде',
        },
        {
          id: 2,
          name: 'Возвращен',
        },
        {
          id: 3,
          name: 'Просрочен',
        },
        {
          id: 4,
          name: 'Завершен',
        },
      ],
    };
  },

  created() {},

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    cancel() {
      this.$emit('cancel');
    },
  },
};
</script>
