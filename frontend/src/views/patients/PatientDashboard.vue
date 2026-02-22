<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-semibold text-success">Patient Dashboard</h2>
      <button @click="logout" class="btn btn-outline-danger px-4">Logout</button>
    </div>
    
    <div class="card shadow-sm border-0 p-4 text-center">
      <h4>Welcome to Healix Hospital!</h4>
      <p class="text-muted">You have successfully logged in.</p>
      </div>
  </div>
</template>

<script>
export default {
  name: 'PatientDashboard',
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
}
</script>