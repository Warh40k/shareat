<template>
  <v-card>
    <v-card-title>Баланс</v-card-title>
    <v-card-text>
      <div class="balance mb-5">{{ balance }} руб.</div>
      <div class="d-flex justify-start">
        <v-btn tile class="white--text" color="main-color">
          <v-icon left>mdi-plus</v-icon>
          Пополнить</v-btn
        >
      </div>
    </v-card-text>

    <v-card-title>История операций</v-card-title>
    <v-data-table :headers="headers" :items="operations" class="elevation-1">
      <template #item.amount="{ item }">
        <span :class="{ 'red--text': item.amount < 0, 'green--text': item.amount > 0 }"> {{ item.amount }} руб. </span>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: 'UserBalanceTab',
  props: {
    balance: Number,
    operations: Array,
  },

  data() {
    return {
      headers: [
        { text: 'Дата', value: 'date' },
        { text: 'Описание', value: 'description' },
        { text: 'Сумма', value: 'amount' },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.balance {
  font-size: 30px;
  font-weight: bold;
}
</style>
