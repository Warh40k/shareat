<template>
  <div class="root-card">
    <v-container color class="text-left mx-auto" fluid>
      <router-link :to="{ name: `product-details`, params: { id: cardData.id, product: cardData } }">
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
      </router-link>
    </v-container>
    <div class="card-footer">
      <v-btn small color="main-color" right class="white--text text order-btn ml-3">
        Оформить
        <v-icon right dark>mdi-cart</v-icon>
      </v-btn>

    <template v-if="roleId == 2">
      <v-menu offset-y bottom>
        <template #activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item @click="updateCard(cardData)">
            <v-icon>mdi-pencil</v-icon>
            <v-list-item-title class="px-3">Редактировать</v-list-item-title>
          </v-list-item>
          <v-list-item @click="deleteCard(cardData.id)">
            <v-icon>mdi-delete</v-icon>
            <v-list-item-title class="px-3">Удалить</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
    </div>

    <SidebarModal v-model="showUpdateProduct" title="Изменение продукта">
      <UpdateProductForm v-if="showUpdateProduct" @success="updateProduct" @cancel="showUpdateProduct = false"
      :product="cardData"/>
    </SidebarModal>

    <CenterModal title="Удаление продукта" :is-open="showDeleteProduct" @close="showDeleteProduct = false">
      <DeleteProductForm
        v-if="showDeleteProduct"
        :id="cardData.id"
        :title="cardData.title"
        @success="deleteProduct"
        @cancel="showDeleteProduct = false" />
    </CenterModal>
  </div>
</template>

<script>
import store from '@/store';
import DeleteProductForm from '@/modules/catalog/ui/components/product/central-modal/DeleteProductForm.vue';
import UpdateProductForm from '@/modules/catalog/ui/components/product/sidebar-modal/UpdateProductForm.vue';

export default {
  name: 'ProductCard',

  components: {
    DeleteProductForm,
    UpdateProductForm
  },

  props: {
    cardData: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      showDeleteProduct: false,
      showUpdateProduct: false,

    };
  },

  computed: {
    roleId() {
      const userData = store.getters['auth/GET_USER_DATA'];
      const roleId = userData ? userData.role_id : -1;
      return roleId;
    }
  },

  methods: {
    updateCard(data) {
      this.cardData = data;
      this.showUpdateProduct = true;
    },

    deleteCard(id) {
      console.log('Удалить карточку с id:', id);
      this.showDeleteProduct = true;
    },

    deleteProduct(){
      console.log('delete success emited');
      this.showDeleteProduct = false;

    },
    updateProduct(){
      console.log('update success emited');
      this.showUpdateProduct = false;

    }
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
  flex-direction: row-reverse;
  justify-content: space-between; /* Размещаем элементы по краям */
  align-items: center;
}
</style>
