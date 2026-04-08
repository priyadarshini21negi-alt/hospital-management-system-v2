<template>
  <div class="container mt-5 pt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">HMS V2 Login</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleLogin">
              
              <div class="mb-3">
                <label for="email" class="form-label">Email Address</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="email" 
                  v-model="email" 
                  required 
                  placeholder="xyz@mail.com"
                >
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password" 
                  v-model="password" 
                  required
                >
              </div>

              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
          </div>
          <div class="card-footer text-center">
            <small>Don't have an account? <router-link to="/register">Register here</router-link></small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import apiClient from '@/axios'; 

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      error: null,
      isLoading: false 
    }
  },
  methods: {
    async handleLogin() {
      this.error = null;
      if (!this.email || !this.password) {
        this.error = "Please fill in all fields";
        return;
      }

      this.isLoading = true;

      try {
        // 1. Get the Token using Axios (Much cleaner syntax!)
        const response = await apiClient.post('/login?include_auth_token', {
          email: this.email, 
          password: this.password
        });

        // Axios automatically parses JSON, so response.data is ready to use
        const token = response.data.response.user.authentication_token;
        
        // 2. Save token to Browser Storage immediately
        // (This makes the interceptor active for the next request)
        localStorage.setItem('auth_token', token);

        // 3. Fetch User Role using Axios
        
        const userResponse = await apiClient.get('/api/user_info');
        const userData = userResponse.data;

        // Save role and email
        localStorage.setItem('user_role', userData.roles[0]);
        localStorage.setItem('user_email', userData.email);

        // 4. Role-Based Redirection!
        if (userData.roles.includes('admin')) {
          this.$router.push('/admin-dashboard');
        } else if (userData.roles.includes('patient')) {
          this.$router.push('/patient-dashboard');
        } else if (userData.roles.includes('doctor')) {
          this.$router.push('/doctor-dashboard');
        }

      } catch (err) {
        console.error(err);
        // Axios wraps errors. A 400/401 from Flask means bad credentials.
        if (err.response && (err.response.status === 400 || err.response.status === 401)) {
          this.error = "Invalid Email or Password";
        } else {
          this.error = "Could not connect to server. Is Flask running?";
        }
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>
