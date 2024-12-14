<template>
  <v-container color style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col v-if="$route.name == 'catalog'" cols="12">
        <v-row>
          <v-col cols="12">
            <h1 class="text-h6 text-sm-h5 font-weight-bold">Каталог товаров</h1>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <ProductsView />
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12">
        <router-view></router-view>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProductsView from '../views/ProductsView.vue';

export default {
  name: 'CatalogView',

  components: {
    ProductsView,
  },
};
</script>

<style></style>
