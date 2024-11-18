<template>
  <ValidationObserver ref="create-product-form" v-slot="{ handleSubmit }">
    <SidebarContentWrapper>
      <template #default>
        <v-row no-gutters>
          <!-- Название -->
          <v-col cols="12">
            <div class="field-label">Название</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-text-field
                v-model="controls.title"
                :error-messages="errors"
                dense
                color="main-color"
                outlined
                @change="saveToLocalStorage" />
            </ValidationProvider>
          </v-col>

          <!-- Описание -->
          <v-col cols="12">
            <div class="field-label">Описание</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-textarea
                v-model="controls.description"
                :error-messages="errors"
                dense
                color="main-color"
                outlined
                @change="saveToLocalStorage" />
            </ValidationProvider>
          </v-col>

          <!-- Стоимость -->
          <v-col cols="12">
            <div class="field-label">Стоимость, руб./час</div>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <v-text-field
                v-model="controls.price"
                type="number"
                :error-messages="errors"
                dense
                color="main-color"
                outlined
                @change="saveToLocalStorage" />
            </ValidationProvider>
          </v-col>

          <!-- Поле для загрузки картинки -->
          <v-col cols="12">
            <div class="field-label">Изображение товара</div>
            <template v-if="!imageName">
              <label class="file-upload">
                <v-icon class="white--text my-2">mdi-plus</v-icon>
                <input type="file" accept="image/png, image/jpeg" @change="onFileChange" />
              </label>
            </template>
            <v-alert v-if="error" class="my-2" color="error-color" type="error" dismissible>
              {{ error }}
            </v-alert>
          </v-col>

          <!-- Превью загруженного изображения -->
          <v-col v-if="imagePreview" cols="12">
            <div class="image-preview">
              <img :src="imagePreview" alt="Предварительный просмотр" class="preview-image" />
              <div class="image-info">
                <p><strong>Название:</strong> {{ imageName }}</p>
                <p><strong>Размер:</strong> {{ imageSize }}</p>
                <p><strong>Объем:</strong> {{ imageVolume }} КБ</p>
              </div>
              <v-btn color="error-color white--text" @click="removeImage">Удалить</v-btn>
            </div>
          </v-col>
        </v-row>
      </template>

      <template #footer>
        <v-btn tile type="submit" class="mr-2 white--text" color="main-color" @click="handleSubmit(submitForm)">
          Создать
        </v-btn>
        <v-btn color="pantone-cold-gray" tile outlined @click="cancel"> Отмена </v-btn>
      </template>
    </SidebarContentWrapper>
  </ValidationObserver>
</template>

<script>
import { mapMutations } from 'vuex';
import SidebarContentWrapper from '@/core/ui/components/shared/sidebar-modal/SidebarContentWrapper.vue';

import ALERT_TYPES from '@/modules/alert/constants/alert-types';

import { CreateProduct } from '../../../../repositories/catalog-repository';

export default {
  name: 'CreateProductForm',
  components: {
    SidebarContentWrapper,
  },

  data() {
    return {
      controls: {
        title: '',
        description: '',
        price: '',
      },
      imagePreview: null,
      imageName: '',
      imageSize: '',
      imageVolume: '',
      imageFile: null,
      error: '',
    };
  },

  methods: {
    ...mapMutations('alert', ['ADD_ALERT']),
    ...mapMutations('preloader', ['ADD_LOADER', 'REMOVE_LOADER']),

    saveToLocalStorage() {
      const objStr = JSON.stringify(this.controls);
      localStorage.setItem('productData', objStr);
    },

    async submitForm() {
      if (!this.imagePreview) {
        this.error = 'Вы не выбрали изображение';
        return;
      }
      try {
        this.ADD_LOADER();

        const formData = new FormData();
        formData.append('title', this.controls.title);
        formData.append('description', this.controls.description);
        formData.append('price_per_day', this.controls.price);
        formData.append('in_rent', false);
        formData.append('is_active', true);
        formData.append('photos', this.imageFile);

        await CreateProduct(formData);
        this.ADD_ALERT({ type: ALERT_TYPES.SUCCESS, text: 'Продукт успешно создан' });

        localStorage.removeItem('productData');
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

    onFileChange(event) {
      const file = event.target.files[0];

      if (file.size > 10 * 1024 * 1024) {
        this.error = 'Размер файла не должен превышать 10 МБ';
        this.removeImage();
        return;
      }

      this.error = '';

      if (file) {
        this.imageFile = file;
        this.imageName = file.name;
        this.imageVolume = (file.size / 1024).toFixed(2);

        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;

          const img = new Image();
          img.src = e.target.result;
          img.onload = () => {
            this.imageSize = `${img.width}x${img.height}`;
          };
        };
        reader.readAsDataURL(file);
      }
    },

    removeImage() {
      this.imagePreview = null;
      this.imageName = '';
      this.imageSize = '';
      this.imageVolume = '';
    },
  },
};
</script>

<style lang="scss" scoped>
.image-preview {
  display: flex;
  align-items: center;
  margin-top: 15px;
}

.preview-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin-right: 15px;
}

.image-info {
  flex-grow: 1;
}

.image-info p {
  margin: 0;
}

.v-btn {
  margin-left: 10px;
}

.file-upload {
  padding: 10px;
  background-color: $main-color; /* Основной цвет кнопки */
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  text-align: center;
  transition: background-color 0.3s ease;
}

.file-upload:hover {
  opacity: 0.8;
}

.file-upload input[type='file'] {
  display: none;
}
</style>
