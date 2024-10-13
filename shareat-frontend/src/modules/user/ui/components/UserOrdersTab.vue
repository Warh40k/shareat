<template>
  <v-card>
    <v-card-title>Мои заказы</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <v-row>
            <v-col cols="12" sm="3">
              <v-text-field
                v-model="searchValue"
                class="pt-0 mt-0"
                placeholder="Поиск по названию товара"
                prepend-inner-icon="mdi-magnify"
                color="main-color"
                clearable
                underlined
                @input="searchInput">
              </v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <template v-if="!orderList.length">
                <p>Записи отсутствуют</p>
              </template>
              <template v-else>
                <v-simple-table>
                  <template #default>
                    <thead>
                      <tr>
                        <th class="text-left">Название</th>
                        <th class="text-left">Статус</th>
                        <th class="text-left">Дата начача</th>
                        <th class="text-left">Дата окончания</th>
                        <th class="text-left">Cтоимость</th>
                        <th class="text-left">Действия</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in orderList" :key="order.id">
                        <td>{{ order.productName }}</td>
                        <td>
                          {{ statusesList.find((s) => s.id === order.statusId).name }}
                        </td>
                        <td>{{ new Date(order.startDate).toLocaleDateString() }}</td>
                        <td>{{ new Date(order.endDate).toLocaleDateString() }}</td>
                        <td>{{ order.fullPrice }}</td>
                        <td class="text-left">
                          <v-btn v-ripple="false" title="Просмотр" plain small icon @click="clickViewOrderBtn(order)">
                            <v-icon>mdi-folder</v-icon>
                          </v-btn>
                          <template v-if="order.statusId === 1">
                            <v-btn
                              v-ripple="false"
                              title="Вернуть"
                              plain
                              small
                              icon
                              @click="clickConfirmReturnBtn(order)">
                              <v-icon color="error-color">mdi-arrow-bottom-left</v-icon>
                            </v-btn>
                          </template>
                          <template v-if="order.statusId === 3">
                            <v-btn
                              v-ripple="false"
                              title="Просмотр штрафа"
                              plain
                              small
                              icon
                              @click="clickCheckFineBtn(order)">
                              <v-icon color="error-color">mdi-cash-multiple</v-icon>
                            </v-btn>
                          </template>
                        </td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </template>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>

    <CenterModal title="Подтверждение возрата" :is-open="showConfirmReturn" @close="showConfirmReturn = false">
      <ConfirmReturnForm
        v-if="showConfirmReturn"
        :id="currentOrder.id"
        :product-name="currentOrder.productName"
        :client-name="currentOrder.clientFullName"
        @success="confirmReturn"
        @cancel="showConfirmReturn = false" />
    </CenterModal>

    <CenterModal title="Просмотр штрафа" :is-open="showCheckFine" @close="showCheckFine = false">
      <CheckFineForm v-if="showCheckFine" :order="currentOrder" @success="checkFine" @cancel="showCheckFine = false" />
    </CenterModal>

    <SidebarModal v-model="showOrder" title="Просмотр заказа">
      <OrderViewForm v-if="showOrder" :order="currentOrder" @cancel="showOrder = false" />
    </SidebarModal>
  </v-card>
</template>

<script>
import ConfirmReturnForm from '../../../orders/ui/components/center-modal/ConfirmReturnForm.vue';
import CheckFineForm from '../../../orders/ui/components/center-modal/CheckFineForm.vue';
import OrderViewForm from '../../../orders/ui/components/sidebar-modal/OrderViewForm.vue';

export default {
  name: 'UserOrdersTab',

  components: { ConfirmReturnForm, CheckFineForm, OrderViewForm },

  props: {
    orders: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      showConfirmReturn: false,
      showCheckFine: false,
      showOrder: false,

      statusesList: [
        {
          id: 0,
          name: 'Новый',
        },
        {
          id: 1,
          name: 'В аренде',
        },
        {
          id: 2,
          name: 'Возвращен',
        },
        {
          id: 3,
          name: 'Просрочен',
        },
        {
          id: 4,
          name: 'Завершен',
        },
      ],

      //TODO: заменить на данные с бэка
      orderList: [
        {
          id: 1,
          productId: 1,
          productName: 'Электросамокат',
          clientId: 1,
          clientFullName: 'Иванов Иван Иванович',
          statusId: 0,
          startDate: '2025-01-01',
          endDate: '2025-02-01',
          fullPrice: 5000,
        },
        {
          id: 2,
          productId: 2,
          productName: 'Планшет Apple IPad',
          clientId: 2,
          clientFullName: 'Петров Петр Петрович',
          statusId: 1,
          startDate: '2025-01-01',
          endDate: '2025-01-15',
          fullPrice: 1200,
        },
        {
          id: 3,
          productId: 1,
          productName: 'Электросамокат',
          clientId: 3,
          clientFullName: 'Сидоров Петр Иванович',
          statusId: 2,
          startDate: '2025-01-01',
          endDate: '2025-01-02',
          fullPrice: 500,
        },
        {
          id: 4,
          productId: 1,
          productName: 'Электросамокат',
          clientId: 3,
          clientFullName: 'Сидоров Петр Иванович',
          statusId: 3,
          startDate: '2024-01-01',
          endDate: '2024-01-02',
          fullPrice: 500,
        },
        {
          id: 5,
          productId: 1,
          productName: 'Электросамокат',
          clientId: 3,
          clientFullName: 'Сидоров Петр Иванович',
          statusId: 4,
          startDate: '2025-01-01',
          endDate: '2025-01-02',
          fullPrice: 500,
        },
      ],
      currentOrder: null,
    };
  },
  methods: {
    clickViewOrderBtn(order) {
      this.currentOrder = order;
      this.showOrder = true;
    },
    clickConfirmReturnBtn(order) {
      this.currentOrder = order;
      this.showConfirmReturn = true;
    },

    //TODO: смена статуса заказа
    confirmReturn() {
      this.showConfirmReturn = false;
      this.currentOrder = null;
    },

    clickCheckFineBtn(order) {
      this.currentOrder = order;
      this.showCheckFine = true;
    },

    checkFine() {
      this.showCheckFine = false;
      this.currentOrder = null;
    },
  },
};
</script>
