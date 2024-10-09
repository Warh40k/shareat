<template>
  <v-container color style="max-width: 1400px" class="text-left pa-5 mx-auto" fluid>
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col cols="12">
            <h1 class="text-h6 text-sm-h5 font-weight-bold">Спортивный инвентарь</h1>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="9">
            <v-btn small tile depressed color="main-color" class="white--text mr-2">
              Добавить
              <v-icon right dark> mdi-plus </v-icon>
            </v-btn>
            <v-btn tile small outlined color="main-color"> Удаленные </v-btn>
          </v-col>
          <v-col cols="12" sm="3">
            <v-text-field
              class="pt-0 mt-0"
              placeholder="Поиск по названию"
              prepend-inner-icon="mdi-magnify"
              color="main-color"
              clearable
              underlined>
            </v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {};
</script>

<style></style>
