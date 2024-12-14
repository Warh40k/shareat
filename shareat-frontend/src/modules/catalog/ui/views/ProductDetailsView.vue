<template>
  <v-container
    v-if="true"
    style="width: auto; max-width: 1224px"
    class="mx-xl-auto mx-lg-16 mx-4 pa-0 mt-5 mt-lg-6 mt-xl-10 mb-10 mb-lg-12 mb-xl-16">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h6 text-sm-h5 font-weight-bold">{{ product.title }}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" lg="6" sm="12">
        <template v-if="product.image">
          <v-img :src="product.image" cover> </v-img>
        </template>
      </v-col>
      <v-col cols="12" lg="6" sm="12">
        <div class="black--text white pa-4 pa-lg-6">
          <div class="mb-4" style="word-wrap: break-word" v-html="product.description"></div>
          <div class="mb-4" style="word-wrap: break-word">Стоимость: {{ product.price }} ₽/день</div>
          <div class="product-btn">
            <template v-if="roleId == 1">
              <v-btn small color="main-color" right class="white--text text" @click="showMakeOrderForm = true">
                Оформить
                <v-icon right dark>mdi-cart</v-icon>
              </v-btn>
            </template>
            <v-btn small class="white--text text" color="background-color" @click="$router.push('/products')"
              >Вернуться</v-btn
            >
          </div>
        </div>
      </v-col>
    </v-row>

    <CenterModal title="Оформление заказа" :is-open="showMakeOrderForm" @close="showMakeOrderForm = false">
      <MakeOrderForm
        v-if="showMakeOrderForm"
        :id="product.id"
        :title="product.title"
        :price="product.price"
        @success="makeOrder"
        @cancel="showMakeOrderForm = false" />
    </CenterModal>
  </v-container>
</template>

<script>
import store from '@/store';
import MakeOrderForm from '@/modules/catalog/ui/components/product/central-modal/MakeOrderForm.vue';

export default {
  name: 'ProductDetailsView',

  components: {
    MakeOrderForm,
  },

  props: {
    product: {
      type: Object,
      required: true,
    },
  },

  computed: {
    roleId() {
      const userData = store.getters['auth/GET_USER_DATA'];
      const roleId = userData ? userData.role_id : -1;
      return roleId;
    },
  },

  data() {
    return {
      showMakeOrderForm: false,
    };
  },
  methods: {
    makeOrder() {
      console.log('makeOrder success emited');
      this.showMakeOrderForm = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.product-btn {
  display: flex;
  justify-content: space-between;
}
</style>
