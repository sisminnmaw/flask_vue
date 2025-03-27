import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    loading: false,
    error: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.user,
    username: (state) => state.user?.username || 'Guest'
  },
  
  actions: {
    async fetchUser() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/frontend/user')
        this.user = response.data
      } catch (error) {
        this.error = 'Failed to load user data'
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    
    clearUser() {
      this.user = null
    }
  }
}) 