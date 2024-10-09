<template>
  <router-link :to="{ name: cardData.pathName }">
    <div class="root-card">
      <span class="card-title"> {{ cardData.title }} </span>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'CategoryRootCard',

  props: {
    cardData: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
a {
  text-decoration: none;
}

.root-card {
  width: 100%;
  height: 200px;
  padding: 20px;
  background-color: $white;
  cursor: pointer;
  transition: all 0.2s linear;

  &:hover {
    box-shadow: $hover-effect;
  }
}

.card-title {
  color: $black;
  font-weight: bold;
}
</style>
