<template>
  <ValidationObserver ref="create-product-form" v-slot="{ handleSubmit }">
    <SidebarContentWrapper>
      <template #default>
        <v-row no-gutters>
          <v-col cols="12">
            <div class="field-label">Название</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-text-field
                v-model="controls.title"
                :error-messages="errors"
                dense
                color="primary1"
                outlined
                @change="saveToLocalStorage" />
            </ValidationProvider>
          </v-col>
          <v-col cols="12">
            <div class="field-label">Описание</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-text-field
                v-model="controls.description"
                :error-messages="errors"
                dense
                color="primary1"
                outlined
                @change="saveToLocalStorage" />
            </ValidationProvider>
          </v-col>
          <v-col cols="12">
            <div class="field-label">Стоимость, руб./час</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-text-field
                v-model="controls.price"
                :error-messages="errors"
                dense
                color="primary1"
                outlined
                @change="saveToLocalStorage" />
            </ValidationProvider>
          </v-col>
        </v-row>
      </template>
      <template #footer>
        <v-btn tile type="submit" class="mr-2 white--text" color="main-color" @click="handleSubmit(submitForm)">
          Создать
        </v-btn>
        <v-btn color="pantone-cold-gray" tile outlined @click="cancel"> Отмена </v-btn>
      </template>
    </SidebarContentWrapper>
  </ValidationObserver>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';
import SidebarContentWrapper from '@/core/ui/components/shared/sidebar-modal/SidebarContentWrapper.vue';

export default {
  name: 'CreateProductForm',
  components: {
    SidebarContentWrapper,
  },

  data() {
    return {
      controls: {
        title: '',
        description: '',
        price: '',
      },
    };
  },

  created() {
    if (localStorage.getItem('productData') !== null) {
      this.restoreFromLocalStorage();
    }
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    saveToLocalStorage() {
      const objStr = JSON.stringify(this.controls);
      localStorage.setItem('productData', objStr);
    },

    restoreFromLocalStorage() {
      const objStrFromStorage = localStorage.getItem('productData');
      this.controls = JSON.parse(objStrFromStorage);
    },
    async submitForm() {
      try {
        this.ADD_LOADER();

        //await CreateProduct(this.controls);

        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Продукт успешно создан' });

        localStorage.removeItem('productData');

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
