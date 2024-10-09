<template>
  <v-container color style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col cols="12">
            <h1 class="text-h6 text-sm-h5 font-weight-bold">Автомобили</h1>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="9">
            <v-btn small tile depressed color="main-color" class="white--text mr-2">
              Добавить
              <v-icon right dark> mdi-plus </v-icon>
            </v-btn>
            <v-btn tile small outlined color="main-color"> Удаленные </v-btn>
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

      <v-col v-for="car in carsList" :key="car.id" cols="12" lg="4" xl="3">
        <ProductCard :card-data="car" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProductCard from '../components/ProductCard.vue';

export default {
  name: 'CarsCategoryView',

  components: {
    ProductCard,
  },
  data() {
    return {
      carsList: [
        {
          id: 1,
          title: 'Toyota Supra A80',
          description:
            'The Toyota Supra (Japanese: トヨタ・スープラ, Hepburn: Toyota Sūpura) is a sports car and grand tourer manufactured by the Toyota Motor Corporation beginning in 1978. The name "supra" is derived from the Latin prefix, meaning "above", "to surpass" or "go beyond"',
          price: '10 000',
          pathName: 'cars',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Black_1997_Toyota_Supra_Limited_Edition_6_Speed_Twin_Turbo_with_Targa_Top.png/275px-Black_1997_Toyota_Supra_Limited_Edition_6_Speed_Twin_Turbo_with_Targa_Top.png',
        },
        {
          id: 2,
          title: 'LADA Granta Sport',
          description:
            'Из особенностей версии: 16-дюймовые литые диски, низкопрофильные шины «Yokohama», передние и задние тормозные диски увеличенного диаметра, уменьшенный на 20 мм дорожный просвет и газонаполненные амортизаторы.',
          price: '10 000 000',
          pathName: 'cars',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Lada_Granta_2018_facelift.jpg/305px-Lada_Granta_2018_facelift.jpg',
        },
        {
          id: 3,
          title: 'Red Bull RB7',
          description:
            'Гоночный автомобиль с открытыми колёсами команды Red Bull Racing, разработанный и построенный под руководством Эдриана Ньюи для участия в гонках Формулы-1 сезона 2011 Формулы-1. За рулём этого автомобиля Себастьян Феттель выиграл свой второй титул Чемпиона мира.',
          price: '100',
          pathName: 'cars',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Sebastian_Vettel_2011_Malaysia_FP1_1.jpg/1200px-Sebastian_Vettel_2011_Malaysia_FP1_1.jpg',
        },
      ],
    };
  },
};
</script>

<style></style>
