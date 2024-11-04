<template>
  <v-container style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col cols="12">
            <h1 class="text-h6 text-sm-h5 font-weight-bold">Управление пользователями</h1>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="9">
            <v-btn small tile depressed color="main-color" class="white--text mr-2" @click="showCreateUser = true">
              Добавить
              <v-icon right dark> mdi-plus </v-icon>
            </v-btn>
          </v-col>
          <v-col cols="12" sm="3">
            <v-text-field
              class="pt-0 mt-0"
              placeholder="Поиск по логину и ФИО"
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
            <template v-if="!userList.length">
              <p>Записи отсутствуют</p>
            </template>
            <template v-else>
              <v-simple-table>
                <template #default>
                  <thead>
                    <tr>
                      <th class="text-left">Логин</th>
                      <th class="text-left">ФИО</th>
                      <th class="text-left">Почта</th>
                      <th class="text-left">Роль</th>
                      <th class="text-left">Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="user in userList" :key="user.id">
                      <td>{{ user.login }}</td>
                      <td>{{ user.fullName }}</td>
                      <td>{{ user.email }}</td>
                      <td>{{ user.roleId == 0 ? 'Администратор' : user.roleId == 1 ? 'Пользователь' : 'Менеджер' }}</td>
                      <td>
                        <v-btn v-ripple="false" title="Изменить" plain small icon @click="clickUpdateUserBtn(user)">
                          <v-icon>mdi-18px mdi-pencil-outline</v-icon>
                        </v-btn>
                        <v-btn
                          v-ripple="false"
                          title="Изменить пароль"
                          plain
                          small
                          icon
                          @click="clickChangePasswordBtn(user)">
                          <v-icon>mdi-18px mdi-shield-edit-outline</v-icon>
                        </v-btn>

                        <v-btn title="Удалить" small icon @click="clickDeleteUserBtn(user)">
                          <v-icon>mdi-18px mdi-delete-outline</v-icon>
                        </v-btn>
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

    <SidebarModal v-model="showCreateUser" title="Создание пользователя">
      <CreateUserForm v-if="showCreateUser" @success="createUser" @cancel="showCreateUser = false" />
    </SidebarModal>

    <SidebarModal v-model="showUpdateUser" title="Изменение данных пользователя">
      <UpdateUserForm
        v-if="showUpdateUser"
        :user="currentUser"
        @success="updateUser"
        @cancel="showUpdateUser = false" />
    </SidebarModal>

    <SidebarModal v-model="showChangePassword" title="Изменение пароля пользователя">
      <ChangeUserPasswordForm
        v-if="showChangePassword"
        :user="currentUser"
        @success="changeUserPassword"
        @cancel="showChangePassword = false" />
    </SidebarModal>

    <CenterModal title="Удаление пользователя" :is-open="showDeleteUser" @close="showDeleteUser = false">
      <DeleteUserForm
        v-if="showDeleteUser"
        :id="currentUser.id"
        @success="deleteUser"
        @cancel="showDeleteUser = false" />
    </CenterModal>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

import CreateUserForm from '../components/sidebar-modal/CreateUserForm.vue';
import UpdateUserForm from '../components/sidebar-modal/UpdateUserForm.vue';
import ChangeUserPasswordForm from '../components/sidebar-modal/ChangeUserPasswordForm.vue';
import DeleteUserForm from '../components/center-modal/DeleteUserForm.vue';

export default {
  name: 'AdminView',

  components: {
    CreateUserForm,
    UpdateUserForm,
    ChangeUserPasswordForm,
    DeleteUserForm,
  },

  data() {
    return {
      showCreateUser: false,
      showUpdateUser: false,
      showChangePassword: false,
      showChangeStatus: false,
      showDeleteUser: false,

      userList: [
        {
          id: 1,
          login: 'admin',
          fullName: 'Иванов Иван Иванович',
          email: 'admin@example.com',
          roleId: 0,
        },
        {
          id: 2,
          login: 'user',
          fullName: 'Петров Петр Петрович',
          email: 'user@example.com',
          roleId: 1,
        },
        {
          id: 3,
          login: 'company',
          fullName: 'Сидоров Сидор Сидорович',
          email: 'company@example.com',
          roleId: 2,
        },
      ],
      currentUser: null,

      searchTimeoutId: null,
    };
  },

  created() {
    //this.fetchUsers();
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    async fetchUsers() {
      try {
        this.ADD_LOADER();

        //const result = await GetAllUsers();

        this.userList = result.data;
      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      } finally {
        this.REMOVE_LOADER();
      }
    },

    createUser() {
      //this.fetchUsers();
      this.showCreateUser = false;
    },

    clickUpdateUserBtn(user) {
      this.currentUser = user;
      this.showUpdateUser = true;
    },

    updateUser() {
      this.showUpdateUser = false;
      this.currentUser = null;
      //this.fetchUsers();
    },

    clickChangePasswordBtn(user) {
      this.currentUser = user;
      this.showChangePassword = true;
    },

    changeUserPassword() {
      this.currentUser = null;
      this.showChangePassword = false;
    },

    clickDeleteUserBtn(user) {
      this.currentUser = user;
      this.showDeleteUser = true;
    },

    deleteUser() {
      this.showDeleteUser = false;
      this.currentUser = null;
      //this.fetchUsers();
    },

    searchInput() {
      if (this.searchTimeoutId) {
        clearTimeout(this.searchTimeoutId);
      }

      this.searchTimeoutId = setTimeout(() => {
        this.fetchUsers();
      }, 400);
    },
  },
};
</script>
