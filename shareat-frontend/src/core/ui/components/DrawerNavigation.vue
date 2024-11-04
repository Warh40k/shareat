<template>
  <v-list style="height: 100%; overflow: auto" nav class="ma-0 pa-0 d-flex flex-column justify-space-between">
    <div>
      <v-list-item title="Открыть/скрыть меню" class="mb-0 pl-4 white--text" @click="$emit('toggle:menu')">
        <v-list-item-icon>
          <v-icon color="color-gray-10">{{ isOpen ? 'mdi-menu' : 'mdi-arrow-left' }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Скрыть</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-for="item in navItems"
        :key="item.title"
        :to="item.link"
        :title="item.title"
        link
        class="mb-0 pl-4 white--text">
        <v-list-item-icon>
          <v-icon color="color-gray-10">{{ item.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </div>
  </v-list>
</template>

<script>

export default {
  name: 'DrawerNavigation',
  props: {
    isOpen: {
      type: Boolean,
    },
    navItems: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped></style>
