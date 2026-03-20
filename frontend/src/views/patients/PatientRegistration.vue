<template>
  <div class="container mt-5  pt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header bg-success text-white">
            <h3 class="mb-0">Patient Registration</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleRegister">
              
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" class="form-control" v-model="name" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Phone Number</label>
                <input type="text" class="form-control" v-model="number" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Email Address</label>
                <input type="email" class="form-control" v-model="email" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" v-model="password" required>
              </div>

              <div v-if="error" class="alert alert-danger">{{ error }}</div>

              <button type="submit" class="btn btn-success w-100">Register</button>
            </form>
          </div>
          <div class="card-footer text-center">
            <small>Already have an account? <router-link to="/login">Login here</router-link></small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientRegister',
  data() {
    return {
      name: '',
      number: '',
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async handleRegister() {
      try {
        //registration api 
        const regResponse = await fetch('http://127.0.0.1:5000/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: this.name,
            number: this.number,
            email: this.email,
            password: this.password
          })
        });

        const regData = await regResponse.json();

        if (regResponse.ok) {
          //autologin after registration 
          this.autoLogin();
        } else {
          this.error = regData.message || "Registration failed.";
        }
      } catch (err) {
        console.error(err);
        this.error = "Could not connect to server.";
      }
    },

    async autoLogin() {
      try {
        
        const loginResponse = await fetch('http://127.0.0.1:5000/login?include_auth_token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.email, password: this.password })
        });

        const loginData = await loginResponse.json();

        if (loginResponse.ok) {
          
          const token = loginData.response.user.authentication_token;
          localStorage.setItem('auth_token', token);
          localStorage.setItem('user_role', 'patient');
          localStorage.setItem('user_email', this.email);
          
          this.$router.push('/patient-dashboard');
        } else {
          this.error = "Registered successfully, but auto-login failed. Please login manually.";
        }
      } catch (err) {
        console.error("Auto-login error:", err);
      }
    }
  }
}
</script>