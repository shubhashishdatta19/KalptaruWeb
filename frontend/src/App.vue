<script setup>
</script>

<template>
  <nav class="flex gap-4 p-4 bg-gray-100">
    <router-link to="/" class="text-blue-600 hover:underline">Home</router-link>
    <router-link to="/admin" class="text-blue-600 hover:underline">Admin</router-link>
  </nav>
  <main class="min-h-screen bg-white">
    <router-view />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
