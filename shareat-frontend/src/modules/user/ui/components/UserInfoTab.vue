<template>
  <v-card>
    <v-card-title>Информация о пользователе</v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title><b>Логин:</b> {{ user.login }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title><b>ФИО:</b> {{ user.fullName }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title><b>Email:</b> {{ user.email }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <template v-if="user.roleId === 2">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><b>Телефон:</b> {{ user.phone }}</v-list-item-title>
              <v-list-item-subtitle></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><b>Адрес:</b> {{ user.address }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>

        <!-- Админ и менеджеры -->
        <template v-if="user.roleId != 2">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><b>Место работы:</b> {{ user.departament }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>

        <v-list-item>
          <v-list-item-content>
            <div class="d-flex justify-start">
              <v-btn tile class="white--text" color="background-color" @click="clickChangePasswordBtn(user)"
                >Сменить пароль</v-btn
              >
            </div>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
    <SidebarModal v-model="showChangePassword" title="Изменение пароля пользователя">
      <ChangeUserPasswordForm
        v-if="showChangePassword"
        :user="user"
        @success="changeUserPassword"
        @cancel="showChangePassword = false" />
    </SidebarModal>
  </v-card>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';
import ChangeUserPasswordForm from '../../../admin/ui/components/sidebar-modal/ChangeUserPasswordForm.vue';

export default {
  name: 'UserInfoTab',
  components: {
    ChangeUserPasswordForm,
  },

  props: {
    user: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      showChangePassword: false,
    };
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),
    clickChangePasswordBtn(user) {
      this.currentUser = user;
      this.showChangePassword = true;
    },

    changeUserPassword() {
      this.currentUser = null;
      this.showChangePassword = false;
    },
  },
};
</script>
