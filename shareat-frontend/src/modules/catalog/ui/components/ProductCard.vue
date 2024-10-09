<template>
  <router-link :to="{ name: cardData.pathName }">
    <div class="root-card">
      <v-container color class="text-left mx-auto" fluid>
        <v-row>
          <v-col cols="12" lg="8" sm="12">
            <div class="card-title">{{ cardData.title }}</div>
            <div class="card-text description">{{ cardData.description }}</div>
            <div class="card-text">Стоимость: {{ cardData.price }}</div>
          </v-col>
          <v-col cols="12" lg="4" sm="12">
            <div class="card-text">
              <img :src="cardData.image" alt="Изображение автомобиля" />
            </div>
          </v-col>
        </v-row>
      </v-container>
      <div class="card-footer">
        <v-btn small color="main-color" right class="white--text text order-btn ml-3">
          Оформить
          <v-icon right dark>mdi-cart</v-icon>
        </v-btn>
      </div>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'ProductCard',

  props: {
    cardData: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
a {
  text-decoration: none;
}

.root-card {
  width: 100%;
  min-height: 100%;
  padding: 20px;
  background-color: $white;
  cursor: pointer;
  transition: all 0.2s linear;

  position: relative;

  &:hover {
    box-shadow: $hover-effect;
  }
}

.description {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-title {
  color: $black;
  font-weight: bold;
}

.card-text {
  color: $black;
}

img {
  width: 100%;
  height: 100%;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
</style>
