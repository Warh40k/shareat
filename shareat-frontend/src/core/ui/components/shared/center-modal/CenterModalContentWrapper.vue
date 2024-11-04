<template>
  <div>
    <v-card-text class="pa-7 modal-content">
      <slot> </slot>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions v-if="$slots.actions" class="px-7 py-5">
      <slot name="actions"> </slot>
    </v-card-actions>
  </div>
</template>

<script>
export default {
  name: 'CenterModalContentWrapper',
};
</script>

<style lang="scss" scoped>
.modal-content {
  max-height: 700px;
  overflow-y: auto !important;
}

@media (width <= 640px) {
  .modal-content {
    max-height: 500px;
  }
}
</style>
