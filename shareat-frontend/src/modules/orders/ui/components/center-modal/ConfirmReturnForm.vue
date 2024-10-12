<template>
  <CenterModalContentWrapper>
    <template #default>
      <p class="text-body-1 ma-0">
        Вы подтверждаете возврат заказа № {{ id }} на {{ productName }} от {{ clientName }}?
      </p>
    </template>
    <template #actions>
      <v-btn tile class="white--text" color="error-color" @click="confirm"> Подтвердить </v-btn>
      <v-btn tile class="white--text" color="background-color" @click="cancel"> Отмена </v-btn>
    </template>
  </CenterModalContentWrapper>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

export default {
  name: 'ConfirmReturnForm',

  props: {
    id: {
      type: Number,
      required: true,
    },
    productName: {
      type: String,
      required: true,
    },
    clientName: {
      type: String,
      required: true,
    },
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    async confirm() {
      try {
        this.ADD_LOADER();
        //await ConfirmReturnOrder(this.id);
        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Возврат заказа подтвержден' });
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
