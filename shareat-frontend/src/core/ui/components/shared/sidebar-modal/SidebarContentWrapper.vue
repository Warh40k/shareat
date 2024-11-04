<template>
  <div class="modal-content-wrapper">
    <div class="modal-content">
      <slot> </slot>
    </div>
    <div v-if="$slots.footer" class="modal-footer">
      <slot name="footer"> </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SidebarContentWrapper',
};
</script>

<style lang="scss" scoped>
@import './styles/modal-variables';

.modal-content-wrapper {
  height: 100%;
}

.modal-content {
  height: calc(100% - $header-height - $footer-height);
  padding: $section-paddings;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  height: $footer-height;
  align-items: center;
  justify-content: flex-start;
  padding: $section-paddings;
  box-shadow: inset 0 -1px 3px 1px rgb(0 0 0 / 10%);
}

@media (width <= $mobile-breakpoint) {
  .modal-content {
    padding: $section-paddings-mobile;
  }

  .modal-footer {
    justify-content: center;
    padding: $section-paddings-mobile;
  }
}
</style>
