<template>
  <ValidationObserver ref="change-user-password" v-slot="{ handleSubmit }">
    <SidebarContentWrapper>
      <template #default>
        <v-row no-gutters>
          <v-col cols="12">
            <div class="field-label">Пароль</div>
            <ValidationProvider v-slot="{ errors }" rules="required" vid="newPassword">
              <v-text-field
                type="password"
                v-model="controls.newPassword"
                :error-messages="errors"
                color="main-color"
                dense
                outlined />
            </ValidationProvider>
          </v-col>
          <v-col cols="12">
            <div class="field-label">Подтверждение пароля</div>
            <ValidationProvider v-slot="{ errors }" rules="required|confirmed:newPassword">
              <v-text-field
                type="password"
                v-model="controls.confirmPassword"
                :error-messages="errors"
                color="main-color"
                dense
                outlined />
            </ValidationProvider>
          </v-col>
        </v-row>
      </template>
      <template #footer>
        <v-btn type="button" tile class="mr-2 white--text" color="main-color" @click="handleSubmit(submitForm)">
          Изменить
        </v-btn>
        <v-btn color="pantone-cold-gray" tile outlined @click="cancel"> Отмена </v-btn>
      </template>
    </SidebarContentWrapper>
  </ValidationObserver>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

import { ChangePassword } from '../../../repositories/admin-repository';

export default {
  name: 'ChangeUserPasswordForm',

  props: {
    user: {
      type: Object,
      required: true,
    },
  },

  emits: ['success', 'cancel'],

  data() {
    return {
      controls: {
        newPassword: '',
        confirmPassword: '',
      },
    };
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    async submitForm() {
      try {
        this.ADD_LOADER();

        await ChangePassword({ id: this.user.id, ...this.controls });

        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Пароль пользователя успешно изменен' });

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
