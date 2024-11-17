<template>
  <CenterModalContentWrapper>
    <template #default>
      <h2 class="mb-2">Заказ на {{ title }}</h2>
      <v-row no-gutters>
          <!-- Дата окончания аренды -->
          <v-col cols="12" class="text-center">
            <div class="field-label mb-3">Дата окончания аренды:</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-date-picker
                v-model="controls.endDate"
                :error-messages="errors"
                dense
                color="main-color"
                outlined
                :min="new Date().toISOString().split('T')[0]"
                />
            </ValidationProvider>
          </v-col>
        </v-row>
        <h2 class="mb-2">Стоимость: {{ getPrice }}</h2>

    </template>
    <template #actions>
      <v-btn tile class="white--text" color="main-color" @click="onSubmit"> Оформить заказ </v-btn>
      <v-btn tile color="pantone-cold-gray" outlined @click="cancel"> Отмена </v-btn>
    </template>
  </CenterModalContentWrapper>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

export default {
  name: 'MakeOrderForm',
  data() {
    return {
      controls: {
        endDate: new Date().toISOString().split('T')[0],
      }
    }
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },

    price: {
      type: String,
      required: true,
    },
  },

  computed: {
    getPrice() {
        const price = Number(this.price);
        const endDate = new Date(this.controls.endDate);
        const today = new Date();
        const diffInDays = Math.ceil((endDate - today) / (1000 * 60 * 60 * 24)) + 1;

        return price * diffInDays;
      }
  },

  watch: {
    'controls.endDate'(newValue) {
      this.getPrice = this.calculatePrice(newValue);
    }
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    calculatePrice(endDate) {
      const price = Number(this.price);
      const days = new Date(endDate).getDate();

      return price * days;
    },

    async onSubmit() {
      try {
        this.ADD_LOADER();
        //await DeleteProduct(this.id);
        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Заказ успешно создан! Вы можете увидеть его в личном кабинете во вкладке "Мои заказы"' });
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
