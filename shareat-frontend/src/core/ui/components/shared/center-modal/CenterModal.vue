<template>
  <v-dialog :value="isOpen" persistent :max-width="maxWidth">
    <v-card>
      <v-card-title class="d-flex flex-nowrap justify-space-between">
        <h4 class="text-truncate">
          {{ title }}
        </h4>
        <v-btn
          tile
          class="pa-0"
          elevation="0"
          min-width="40"
          max-width="40"
          min-height="40"
          max-height="40"
          width="40"
          height="40"
          @click="close">
          <v-icon>mdi-plus mdi-rotate-45</v-icon>
        </v-btn>
      </v-card-title>
      <v-divider></v-divider>
      <slot> </slot>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'CenterModal',

  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },

    maxWidth: {
      type: Number,
      default: 600,
    },

    title: {
      type: String,
      required: true,
    },
  },

  methods: {
    close() {
      this.$emit('close');
    },
  },
};
</script>
