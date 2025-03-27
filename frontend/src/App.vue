<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Header from './components/Header.vue'
</script>

<template>
  <Header />
  <div class="container">
    <RouterView />
  </div>
</template>

<style>
/* Any App-specific styles can go here */
</style> 