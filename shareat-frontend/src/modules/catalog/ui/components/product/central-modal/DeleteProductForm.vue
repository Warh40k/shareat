<template>
  <CenterModalContentWrapper>
    <template #default>
      <p class="text-body-1 ma-0">Вы действительно хотите удалить продукт {{ title }}?</p>
    </template>
    <template #actions>
      <v-btn tile class="white--text" color="error-color" @click="onSubmit"> Удалить </v-btn>
      <v-btn tile color="pantone-cold-gray" outlined @click="cancel"> Отмена </v-btn>
    </template>
  </CenterModalContentWrapper>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

export default {
  name: 'DeleteProductForm',

  props: {
    id: {
      type: Number,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    async onSubmit() {
      try {
        this.ADD_LOADER();
        //await DeleteProduct(this.id);
        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Продукт успешно удален' });
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
