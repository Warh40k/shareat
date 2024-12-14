<template>
  <v-container color style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col cols="12">
        <v-row>
          <template v-if="roleId == 2">
            <v-col cols="12" sm="9">
              <v-btn small tile depressed color="main-color" class="white--text mr-2" @click="showCreateProduct = true">
                Добавить
                <v-icon right dark> mdi-plus </v-icon>
              </v-btn>
            </v-col>
          </template>
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
        <ProductCard :card-data="car" @deleted="deleteProduct" @updated="updateProduct" />
      </v-col>
    </v-row>
    <SidebarModal v-model="showCreateProduct" title="Создание продукта">
      <CreateProductForm v-if="showCreateProduct" @success="createProduct" @cancel="showCreateProduct = false" />
    </SidebarModal>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex';
import store from '@/store';
import ALERT_TYPES from '@/modules/alert/constants/alert-types';
import ProductCard from '../components/ProductCard.vue';
import CreateProductForm from '../components/product/sidebar-modal/CreateProductForm.vue';
import { GetAllProducts } from '../../repositories/catalog-repository';

export default {
  name: 'ProductsView',

  components: {
    ProductCard,
    CreateProductForm,
  },
  data() {
    return {
      showCreateProduct: false,

      carsList: [],

      // carsList: [
      //   {
      //     id: 1,
      //     title: 'Toyota Supra A80',
      //     description:
      //       'The Toyota Supra (Japanese: トヨタ・スープラ, Hepburn: Toyota Sūpura) is a sports car and grand tourer manufactured by the Toyota Motor Corporation beginning in 1978. The name "supra" is derived from the Latin prefix, meaning "above", "to surpass" or "go beyond"',
      //     price: '10000',
      //     image:
      //       'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Black_1997_Toyota_Supra_Limited_Edition_6_Speed_Twin_Turbo_with_Targa_Top.png/1920px-Black_1997_Toyota_Supra_Limited_Edition_6_Speed_Twin_Turbo_with_Targa_Top.png',
      //   },
      //   {
      //     id: 2,
      //     title: 'LADA Granta Sport',
      //     description:
      //       'Из особенностей версии: 16-дюймовые литые диски, низкопрофильные шины «Yokohama», передние и задние тормозные диски увеличенного диаметра, уменьшенный на 20 мм дорожный просвет и газонаполненные амортизаторы.',
      //     price: '10000000',
      //     image: 'https://upload.wikimedia.org/wikipedia/commons/1/11/Lada_Granta_2018_facelift.jpg',
      //   },
      //   {
      //     id: 3,
      //     title: 'Red Bull RB7',
      //     description:
      //       'Гоночный автомобиль с открытыми колёсами команды Red Bull Racing, разработанный и построенный под руководством Эдриана Ньюи для участия в гонках Формулы-1 сезона 2011 Формулы-1. За рулём этого автомобиля Себастьян Феттель выиграл свой второй титул Чемпиона мира.',
      //     price: '100',
      //     image:
      //       'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Sebastian_Vettel_2011_Malaysia_FP1_1.jpg/1200px-Sebastian_Vettel_2011_Malaysia_FP1_1.jpg',
      //   },
      // ],
    };
  },

  computed: {
    roleId() {
      const userData = store.getters['auth/GET_USER_DATA'];

      const roleId = userData ? userData.role_id : -1;

      return roleId;
    },
  },

  created() {
    this.fetchProducts();
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),
    async fetchProducts() {
      try {
        this.ADD_LOADER();

        const result = await GetAllProducts();

        this.carsList = result.map((car) => ({
          id: car.id,
          title: car.title,
          description: car.description,
          price: car.price_per_day,

          // TODO: сделать красивее
          image: 'http://localhost:8000/api/catalog/getPhoto/' + car.photos[0],
        }));
      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      } finally {
        this.REMOVE_LOADER();
      }
    },

    deleteProduct() {
      this.fetchProducts();
    },

    updateProduct() {
      this.fetchProducts();
    },

    createProduct() {
      this.showCreateProduct = false;
      this.fetchProducts();
    },
  },
};
</script>

<style></style>
