<template>
  <v-container style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-tabs v-model="activeTab" color="main-color">
      <v-tab>Информация</v-tab>
      <v-tab>Баланс и история операций</v-tab>
      <v-tab>Мои заказы</v-tab>
    </v-tabs>

    <v-tabs-items v-model="activeTab">
      <v-tab-item>
        <UserInfo :user="user" />
      </v-tab-item>

      <v-tab-item>
        <UserBalance :balance="balance" :operations="operations" />
      </v-tab-item>

      <v-tab-item>
        <UserOrders :orders="orders" />
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import UserInfo from '../components/UserInfoTab.vue';
import UserBalance from '../components/UserBalanceTab.vue';
import UserOrders from '../components/UserOrdersTab.vue';

export default {
  name: 'UserProfileView',

  components: { UserInfo, UserBalance, UserOrders },
  data() {
    return {
      activeTab: 0,
      user: {
        id: 1,
        login: 'ivan',
        fullName: 'Иван Иванов',
        email: 'ivan@example.com',
        roleId: 2,
        phone: '+79991234567',
        address: 'г. Москва, ул. Пушкина, д. 10',
      },
      balance: 10000,
      operations: [
        { id: 1, date: '2024-01-01', amount: -500, description: 'Оплата заказа #123' },
        { id: 2, date: '2024-01-05', amount: 1500, description: 'Пополнение' },
      ],
      orders: [
        { id: 1, date: '2024-01-01', total: 1500, status: 'Доставлено' },
        { id: 2, date: '2024-01-10', total: 2000, status: 'В обработке' },
      ],
    };
  },
};
</script>

<style scoped>
/* Стили если нужны */
</style>
