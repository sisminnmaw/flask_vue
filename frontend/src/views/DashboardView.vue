<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const dashboardData = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await axios.get('/api/frontend/dashboard')
    dashboardData.value = response.data
  } catch (err) {
    error.value = 'Failed to load dashboard data'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    
    <div v-if="loading" class="loading">
      Loading dashboard data...
    </div>
    
    <div v-else-if="error" class="error card">
      {{ error }}
    </div>
    
    <div v-else-if="dashboardData">
      <div class="card stats-section">
        <h2>System Statistics</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-value">{{ dashboardData.stats.users }}</div>
            <div class="stat-label">Users</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ dashboardData.stats.active_sessions }}</div>
            <div class="stat-label">Active Sessions</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ dashboardData.stats.pending_tasks }}</div>
            <div class="stat-label">Pending Tasks</div>
          </div>
        </div>
      </div>
      
      <div class="card activities-section">
        <h2>Recent Activities</h2>
        <ul class="activity-list">
          <li v-for="activity in dashboardData.recent_activities" :key="activity.id" class="activity-item">
            <div class="activity-action">{{ activity.action }}</div>
            <div class="activity-time">{{ new Date(activity.timestamp).toLocaleString() }}</div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard h1 {
  margin-bottom: 2rem;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-style: italic;
}

.error {
  color: var(--color-danger);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--color-primary);
}

.stat-label {
  margin-top: 0.5rem;
  color: var(--color-secondary);
}

.activities-section {
  margin-top: 2rem;
}

.activity-list {
  list-style: none;
  padding: 0;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  color: var(--color-secondary);
  font-size: 0.9rem;
}
</style> 