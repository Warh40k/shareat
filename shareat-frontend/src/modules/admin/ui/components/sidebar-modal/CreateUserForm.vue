<template>
  <ValidationObserver ref="create-user" v-slot="{ handleSubmit }">
    <SidebarContentWrapper>
      <template #default>
        <v-row no-gutters>
          <v-col cols="12">
            <div class="field-label">Логин</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-text-field v-model="controls.login" :error-messages="errors" color="main-color" outlined dense />
            </ValidationProvider>
          </v-col>
          <v-col cols="12">
            <div class="field-label">Пароль</div>
            <ValidationProvider v-slot="{ errors }" rules="required" vid="password">
              <v-text-field
                type="password"
                v-model="controls.password"
                :error-messages="errors"
                color="main-color"
                outlined
                dense />
            </ValidationProvider>
          </v-col>
          <v-col cols="12">
            <div class="field-label">Подтверждение пароля</div>
            <ValidationProvider v-slot="{ errors }" rules="required|confirmed:password">
              <v-text-field
                type="password"
                v-model="controls.confirmPassword"
                :error-messages="errors"
                color="main-color"
                outlined
                dense />
            </ValidationProvider>
          </v-col>
          <v-col cols="12">
            <div class="field-label">ФИО</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-text-field v-model="controls.fullName" :error-messages="errors" color="main-color" outlined dense />
            </ValidationProvider>
          </v-col>
          <v-col cols="12">
            <div class="field-label">Почта</div>
            <ValidationProvider v-slot="{ errors }" rules="required|email">
              <v-text-field v-model="controls.email" :error-messages="errors" color="main-color" outlined dense />
            </ValidationProvider>
          </v-col>
          <v-col cols="12">
            <div class="field-label">Роль</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-autocomplete
                v-model="controls.roleId"
                :items="roles"
                item-text="name"
                item-value="id"
                :error-messages="errors"
                dense
                color="main-color"
                outlined
                :menu-props="{ bottom: true, offsetY: true }" />
            </ValidationProvider>
          </v-col>
        </v-row>
      </template>
      <template #footer>
        <v-btn type="button" tile class="mr-2 white--text" color="main-color" @click="handleSubmit(submitForm)">
          Создать
        </v-btn>
        <v-btn color="pantone-cold-gray" tile outlined dense @click="cancel"> Отмена </v-btn>
      </template>
    </SidebarContentWrapper>
  </ValidationObserver>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

import { CreateUser } from '../../../repositories/admin-repository';

export default {
  name: 'CreateUserForm',

  emits: ['success', 'cancel'],

  data() {
    return {
      roles: [
        {
          id: 0,
          name: 'Администратор',
        },
        {
          id: 1,
          name: 'Пользователь',
        },
        {
          id: 2,
          name: 'Менеджер',
        },
      ],

      controls: {
        login: '',
        password: '',
        confirmPassword: '',
        fullName: '',
        email: '',
        roleId: 1,
      },
    };
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    async submitForm() {
      try {
        this.ADD_LOADER();

        await CreateUser(this.controls);

        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Пользователь успешно создан' });

        this.$emit('success');
      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      } finally {
        this.REMOVE_LOADER();
      }
    },

    cancel() {
      this.$emit('cancel');
    },
  },
};
</script>
