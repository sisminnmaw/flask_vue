<script setup>
</script>

<template>
  <div class="home">
    <h1>Welcome to Flask-Vue Application</h1>
    <div class="card">
      <h2>Features</h2>
      <ul>
        <li>API Services for backend operations</li>
        <li>API Services for frontend interfaces</li>
        <li>Automated batch processes with email alerts</li>
        <li>Modern Vue 3 frontend with Composition API</li>
      </ul>
    </div>
    <div class="card">
      <h2>Getting Started</h2>
      <p>
        Explore the application using the navigation menu above. The Dashboard section shows data from the backend API.
      </p>
      <RouterLink to="/dashboard" class="btn">View Dashboard</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.home h1 {
  margin-bottom: 2rem;
  text-align: center;
}

.home ul {
  padding-left: 1.5rem;
  margin: 1rem 0;
}

.home p {
  margin-bottom: 1.5rem;
}
</style> 