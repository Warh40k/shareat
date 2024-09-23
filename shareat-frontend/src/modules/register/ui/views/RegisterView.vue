<template>
  <v-container fluid>
    <ValidationObserver ref="login-form" v-slot="{ handleSubmit }">
      <v-row align="center" style="height: 100vh">
        <v-col cols="12" class="d-flex justify-center">
          <v-card class="rounded-lg">
            <v-sheet class="pa-7" width="600" color="white">
              <v-row class="mb-2">
                <v-col cols="12" class="text-center">
                  <h1>Регистрация</h1>
                </v-col>
              </v-row>

              <v-row no-gutters>
                <v-col cols="12">
                  <ValidationProvider v-slot="{ errors }" rules="required">
                    <v-text-field
                      v-model="controls.fullName"
                      :error-messages="errors"
                      outlined
                      color="main-color"
                      label="Имя" />
                  </ValidationProvider>
                </v-col>

                <v-col cols="12">
                  <ValidationProvider v-slot="{ errors }" rules="required">
                    <v-text-field
                      v-model="controls.login"
                      :error-messages="errors"
                      outlined
                      color="main-color"
                      label="Логин"
                      autocomplete="new-password" />
                  </ValidationProvider>
                </v-col>

                <v-col cols="12">
                  <ValidationProvider v-slot="{ errors }" rules="required">
                    <v-text-field
                      v-model="controls.email"
                      :error-messages="errors"
                      outlined
                      color="main-color"
                      label="Email"
                      autocomplete="new-password" />
                  </ValidationProvider>
                </v-col>

                <v-col cols="12">
                  <ValidationProvider v-slot="{ errors }" rules="required" vid="password">
                    <v-text-field
                      v-model="controls.password"
                      :error-messages="errors"
                      outlined
                      color="main-color"
                      :type="showPassword ? 'text' : 'password'"
                      :append-icon="showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
                      label="Пароль"
                      autocomplete="new-password"
                      @click:append="() => (showPassword = !showPassword)" />
                  </ValidationProvider>
                </v-col>

                <v-col cols="12">
                  <ValidationProvider v-slot="{ errors }" rules="required|confirmed:password">
                    <v-text-field
                      v-model="controls.passwordAgain"
                      :error-messages="errors"
                      outlined
                      color="main-color"
                      :type="showPasswordAgain ? 'text' : 'password'"
                      :append-icon="showPasswordAgain ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
                      label="Подтверждение пароля"
                      @click:append="() => (showPasswordAgain = !showPasswordAgain)" />
                  </ValidationProvider>
                </v-col>
              </v-row>

              <v-row no-gutters>
                <v-col cols="12" class="d-flex justify-center">
                  <div>
                    <v-btn
                      depressed
                      tile
                      class="white--text"
                      color="background-color"
                      @click="handleSubmit(onSubmitRegister)">
                      Зарегистрироваться
                    </v-btn>
                    <v-btn depressed tile class="white--text mx-5" color="background-color" :to="'/login'">
                      Назад
                    </v-btn>
                  </div>
                </v-col>
              </v-row>
            </v-sheet>
          </v-card>
        </v-col>
      </v-row>
    </ValidationObserver>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';
import { Register } from '../../repositories/register-repository';

export default {
  name: 'RegisterView',

  data() {
    return {
      showPassword: false,
      showPasswordAgain: false,

      controls: {
        fullName: null,
        login: null,
        password: null,
        passwordAgain: null,
        email: null,
      },
    };
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),
    ...mapMutations('auth', ['SET_AUTH_DATA']),

    async onSubmitRegister() {
      try {
        this.ADD_LOADER();

        const user = await Register({
          fullName: this.controls.fullName,
          login: this.controls.login,
          password: this.controls.password,
          email: this.controls.email,
        });

        this.SET_AUTH_DATA(user);

        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Успешная регистрация' });
        this.$router.push({ name: 'login' });
      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      } finally {
        this.REMOVE_LOADER();
      }
    },
  },
};
</script>

<style lang="scss" scoped></style>
