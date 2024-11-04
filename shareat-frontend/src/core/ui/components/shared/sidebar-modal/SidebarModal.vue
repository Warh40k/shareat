<template>
  <div>
    <transition name="overlay">
      <div v-if="innerValue" class="modal-overlay"></div>
    </transition>
    <transition name="modal">
      <div v-if="innerValue" class="modal-wrapper">
        <div class="modal-header">
          <span class="modal-title"> {{ title }}</span>
          <button class="modal-close-button" type="button" title="Закрыть" @click="innerValue = false">
            <svg class="button-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
            </svg>
          </button>
        </div>
        <slot> </slot>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'SidebarModal',

  props: {
    value: {
      type: Boolean,
    },

    title: {
      type: String,
      required: true,
    },
  },

  emits: ['input'],

  data() {
    return {
      innerValue: false,
    };
  },

  watch: {
    innerValue(value) {
      document.querySelector('html').style.overflowY = value ? 'hidden' : 'auto';
      this.$emit('input', value);
    },
    value(value) {
      this.innerValue = value;
    },
  },
};
</script>

<style lang="scss" scoped>
@import './styles/modal-variables';

.modal-overlay {
  position: fixed;
  z-index: 99;
  width: 100%;
  height: 100%;
  background-color: rgb(0 0 0 / 50%);
  inset: 0;
}

.modal-wrapper {
  position: fixed;
  z-index: 100;
  top: 0;
  right: 0;
  overflow: hidden;
  width: 100%;
  max-width: $mobile-breakpoint;
  height: 100%;
  background-color: white;
}

.modal-header {
  display: flex;
  height: $header-height;
  align-items: center;
  justify-content: space-between;
  padding: $section-paddings;
}

.modal-title {
  overflow: hidden;
  margin-right: 10px;
  font-size: 22px;
  font-weight: bold;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.modal-close-button {
  display: flex;
  width: 36px;
  min-width: 36px;
  height: 36px;
  min-height: 36px;
  align-items: center;
  justify-content: center;
  background-color: rgb(225 225 225 / 50%);
  transition: all 0.2s ease;

  &:hover {
    background-color: rgb(225 225 225 / 90%);
  }
}

.button-icon {
  width: 20px;
  height: 20px;
}

.overlay-enter-active,
.overlay-leave-active {
  transition: all 0.2s ease;
}

.overlay-enter,
.overlay-leave-to {
  opacity: 0;
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.2s ease;
}

.modal-enter,
.modal-leave-to {
  transform: translateX(100%);
}

@media (width <= $mobile-breakpoint) {
  .modal-header {
    padding: $section-paddings-mobile;
  }

  .modal-enter-active,
  .modal-leave-active {
    transition: all 0.2s ease;
  }

  .modal-enter,
  .modal-leave-to {
    transform: translateY(100%);
  }
}
</style>
