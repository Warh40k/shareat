<template>
  <v-container style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col cols="12">
            <h1 class="text-h6 text-sm-h5 font-weight-bold">Управление заказами</h1>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="9">
            <v-btn small color="main-color" right class="white--text text" @click="showGetReport = true">
                Заказать отчет
                <v-icon right dark>mdi-note-text-outline</v-icon>
              </v-btn>
          </v-col>
          <v-col cols="12" sm="3">
            <v-text-field
              v-model="searchValue"
              class="pt-0 mt-0"
              placeholder="Поиск по названию товара"
              prepend-inner-icon="mdi-magnify"
              color="primary1"
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
                      <th class="text-left">Идентификатор</th>
                      <th class="text-left">Название</th>
                      <th class="text-left">ФИО клиента</th>
                      <th class="text-left">Статус</th>
                      <th class="text-left">Дата начача</th>
                      <th class="text-left">Дата окончания</th>
                      <th class="text-left">Общая стоимость</th>
                      <th class="text-left">Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="order in orderList" :key="order.id">
                      <td>{{ order.id }}</td>
                      <td>{{ order.productName }}</td>
                      <td>{{ order.clientFullName }}</td>
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
                        <template v-if="order.statusId === 0">
                          <v-btn
                            v-ripple="false"
                            title="Подтвердить"
                            plain
                            small
                            icon
                            @click="clickConfirmOrderBtn(order)">
                            <v-icon color="success-color">mdi-check</v-icon>
                          </v-btn>
                        </template>
                        <template v-if="order.statusId === 2">
                          <v-btn
                            v-ripple="false"
                            title="Подтвердить возврат"
                            plain
                            small
                            icon
                            @click="clickConfirmReturnBtn(order)">
                            <v-icon color="warning-color">mdi-arrow-bottom-left</v-icon>
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

    <CenterModal title="Подтверждение заказа" :is-open="showConfirmOrder" @close="showConfirmOrder = false">
      <ConfirmOrderForm
        v-if="showConfirmOrder"
        :id="currentOrder.id"
        :product-name="currentOrder.productName"
        :client-name="currentOrder.clientFullName"
        @success="confirmOrder"
        @cancel="showConfirmOrder = false" />
    </CenterModal>

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

    <CenterModal title="Заказ отчета" :is-open="showGetReport" @close="showGetReport = false">
      <GetReportForm v-if="showGetReport" @success="getReport" @cancel="showGetReport = false" />
    </CenterModal>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

import ConfirmOrderForm from '../components/center-modal/ConfirmOrderForm.vue';
import ConfirmReturnForm from '../components/center-modal/ConfirmReturnForm.vue';
import CheckFineForm from '../components/center-modal/CheckFineForm.vue';
import GetReportForm from '../components/center-modal/GetReportForm.vue';
import OrderViewForm from '../components/sidebar-modal/OrderViewForm.vue';

export default {
  name: 'OrdersView',

  components: { ConfirmOrderForm, ConfirmReturnForm, CheckFineForm, OrderViewForm, GetReportForm },

  data() {
    return {
      showOrder: false,
      showConfirmOrder: false,
      showConfirmReturn: false,
      showCheckFine: false,
      showGetReport: false,

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
          startDate: '2025-01-01',
          endDate: '2025-01-02',
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

      searchTimeoutId: null,
      searchValue: '',
    };
  },

  created() {
    //this.fetchOrders();
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    async fetchOrders() {
      try {
        this.ADD_LOADER();

        //const result = await GetAllOrders();

        this.orderList = result.data;
      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      } finally {
        this.REMOVE_LOADER();
      }
    },

    clickViewOrderBtn(order) {
      this.currentOrder = order;
      this.showOrder = true;
    },

    clickConfirmOrderBtn(order) {
      this.currentOrder = order;
      this.showConfirmOrder = true;
    },

    //TODO: смена статуса заказа
    confirmOrder() {
      this.currentOrder = null;
      this.showConfirmOrder = false;
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

    clickGetReportBtn() {
      this.showGetReport = true;
    },

    getReport() {
      this.showGetReport = false;
    },

    searchInput() {
      if (this.searchTimeoutId) {
        clearTimeout(this.searchTimeoutId);
      }

      this.searchTimeoutId = setTimeout(() => {
        this.orderList = this.orderList.filter((o) => o.productName.includes(this.searchValue));
        //TODO: поиск
      }, 400);
    },
  },
};
</script>
