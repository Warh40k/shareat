<template>
  <CenterModalContentWrapper>
    <template #default>
      <p class="text-body-1 ma-0">
        В связи с тем, что клиент {{ order.clientFullName }} не вернул заказ №{{ order.id }} на
        {{ order.productName }} до {{ order.endDate }} назначен штраф в размере undefined руб. в сутки.
      </p>
      <p class="text-body-1 ma-0">Просрочка: {{ getDelay() }}</p>
    </template>
  </CenterModalContentWrapper>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  name: 'CheckFineForm',

  props: {
    order: {
      type: Object,
      required: true,
    },
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    getDelay() {
      const now = new Date();
      const delay = new Date(this.order.endDate).getTime() - now.getTime();
      const number = Math.ceil(delay / (1000 * 60 * 60 * 24));

      if (number > 10 && [11, 12, 13, 14].includes(number % 100)) return `${number} дней`;
      const lastNum = number % 10;

      if ([2, 3, 4].includes(lastNum)) return `${number} дня`;
      if ([5, 6, 7, 8, 9, 0].includes(lastNum)) return `${number} дней`;
      return `${number}день`;
    },

    cancel() {
      this.$emit('cancel');
    },
  },
};
</script>
