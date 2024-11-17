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
          <div class="mb-4" style="word-wrap: break-word">Стоимость: {{ product.price }} ₽/час</div>
          <div class="product-btn">
            <v-btn small color="main-color" right class="white--text text">
              Оформить
              <v-icon right dark>mdi-cart</v-icon>
            </v-btn>
             <v-btn small class="white--text text" color="background-color" @click="$router.push('/products')"
              >Вернуться</v-btn>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ProductDetailsView',

  props: {
    product: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      links: [
        {
          text: 'Каталог',
          disabled: false,
          href: '/products',
        }
      ]
    }
  },
};
</script>

<style lang="scss" scoped>
.product-btn {
  display: flex;
  justify-content: space-between;
}
</style>
