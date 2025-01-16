<template>
  <div class="root-card">
    <v-container color class="text-left mx-auto" fluid>
      <div>
        <v-row>
          <v-col cols="12">
            <div class="card-title ">Ключ: {{ cardData.key.split("/")[2] }}</div>
            <div class="card-text description">Тип: {{ cardData.type }}</div>
            <div class="card-text">Дата: {{ cardData.date }}</div>
            <div class="card-text">Автор: {{ cardData.author }}</div>
          </v-col>
        </v-row>
      </div>
    </v-container>
    <div class="card-footer">
      <template>
        <v-btn small color="main-color" right class="white--text text order-btn ml-3" @click="downloadReport(cardData.key)">
          Скачать
          <v-icon right dark>mdi-download</v-icon>
        </v-btn>
      </template>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex';
import ALERT_TYPES from '@/modules/alert/constants/alert-types';
import { DownloadReport } from '../../../orders/repositories/order-repository';

export default {
  name: 'ReportCard',


  props: {
    cardData: {
      type: Object,
      required: true,
    },
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),
    async downloadReport(key){
       try {
        this.ADD_LOADER();

        var report = await DownloadReport(key);
        const blob = new Blob([report], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${key.split("/")[2]}.pdf`;
        link.click();
        window.URL.revokeObjectURL(url);

      } catch (error) {
        this.ADD_ALERT({ type: ALERT_TYPES.ERROR, text: error.message });
      } finally {
        this.REMOVE_LOADER();
      }
    }
  },
};
</script>

<style lang="scss" scoped>
a {
  text-decoration: none;
}

.root-card {
  width: 100%;
  min-height: 100%;
  padding: 20px;
  background-color: $white;
  cursor: pointer;
  transition: all 0.2s linear;

  position: relative;

  &:hover {
    box-shadow: $hover-effect;
  }
}

.description {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-title {
  color: $black;
  font-weight: bold;
}

.card-text {
  color: $black;
}

img {
  width: 100%;
  height: 100%;
}

.card-footer {
  display: flex;
  flex-direction: row;
  justify-content: space-between; /* Размещаем элементы по краям */
  align-items: center;
}
</style>
