<template>
  <CenterModalContentWrapper>
    <template #default>
      <p class="text-body-1 ma-0">Вы действительно хотите удалить пользователя?</p>
    </template>
    <template #actions>
      <v-btn tile class="white--text" color="error-color" @click="confirm"> Удалить </v-btn>
      <v-btn color="pantone-cold-gray" tile outlined dense @click="cancel"> Отмена </v-btn>
    </template>
  </CenterModalContentWrapper>
</template>

<script>
import { mapMutations } from 'vuex';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

import { DeleteUser } from '../../../repositories/admin-repository';

export default {
  name: 'DeleteUserForm',

  props: {
    id: {
      type: Number,
      required: true,
    },
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    async confirm() {
      try {
        this.ADD_LOADER();
        await DeleteUser(this.id);
        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Пользователь успешно удален' });
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
