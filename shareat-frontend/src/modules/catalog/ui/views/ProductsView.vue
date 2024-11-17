<template>
  <v-container color style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col cols="12" sm="9">
            <v-btn small tile depressed color="main-color" class="white--text mr-2" @click="showCreateProduct = true">
              Добавить
              <v-icon right dark> mdi-plus </v-icon>
            </v-btn>
          </v-col>
          <v-col cols="12" sm="3">
            <v-text-field
              class="pt-0 mt-0"
              placeholder="Поиск по названию"
              prepend-inner-icon="mdi-magnify"
              color="main-color"
              clearable
              underlined>
            </v-text-field>
          </v-col>
        </v-row>
      </v-col>

      <v-col v-for="car in carsList" :key="car.id" cols="12">
        <ProductCard :card-data="car" />
      </v-col>
    </v-row>
    <SidebarModal v-model="showCreateProduct" title="Создание продукта">
      <CreateProductForm v-if="showCreateProduct" @success="createProduct" @cancel="showCreateProduct = false" />
    </SidebarModal>
  </v-container>
</template>

<script>
import ProductCard from '../components/ProductCard.vue';
import CreateProductForm from '../components/product/sidebar-modal/CreateProductForm.vue';

export default {
  name: 'ProductsCategoryView',

  components: {
    ProductCard,
    CreateProductForm,
  },
  data() {
    return {
      showCreateProduct: false,
      carsList: [
        {
          id: 1,
          title: 'Toyota Supra A80',
          description:
            'The Toyota Supra (Japanese: トヨタ・スープラ, Hepburn: Toyota Sūpura) is a sports car and grand tourer manufactured by the Toyota Motor Corporation beginning in 1978. The name "supra" is derived from the Latin prefix, meaning "above", "to surpass" or "go beyond"',
          price: '10 000',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Black_1997_Toyota_Supra_Limited_Edition_6_Speed_Twin_Turbo_with_Targa_Top.png/1920px-Black_1997_Toyota_Supra_Limited_Edition_6_Speed_Twin_Turbo_with_Targa_Top.png',
        },
        {
          id: 2,
          title: 'LADA Granta Sport',
          description:
            'Из особенностей версии: 16-дюймовые литые диски, низкопрофильные шины «Yokohama», передние и задние тормозные диски увеличенного диаметра, уменьшенный на 20 мм дорожный просвет и газонаполненные амортизаторы.',
          price: '10 000 000',
          image: 'https://upload.wikimedia.org/wikipedia/commons/1/11/Lada_Granta_2018_facelift.jpg',
        },
        {
          id: 3,
          title: 'Red Bull RB7',
          description:
            'Гоночный автомобиль с открытыми колёсами команды Red Bull Racing, разработанный и построенный под руководством Эдриана Ньюи для участия в гонках Формулы-1 сезона 2011 Формулы-1. За рулём этого автомобиля Себастьян Феттель выиграл свой второй титул Чемпиона мира.',
          price: '100',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Sebastian_Vettel_2011_Malaysia_FP1_1.jpg/1200px-Sebastian_Vettel_2011_Malaysia_FP1_1.jpg',
        },
      ],
    };
  },

  methods: {
    createProduct() {
      this.showCreateProduct = true;
    },
  },
};
</script>

<style></style>
