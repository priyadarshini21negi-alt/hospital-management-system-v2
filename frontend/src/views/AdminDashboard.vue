<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Admin Dashboard</h2>
      <button @click="logout" class="btn btn-danger">Logout</button>
    </div>

    <div class="card shadow">
      <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h4 class="mb-0">Manage Doctors</h4>
        <button @click="showAddForm = !showAddForm" class="btn btn-light btn-sm">
          {{ showAddForm ? 'Cancel' : '+ Add New Doctor' }}
        </button>
      </div>

      <div v-if="showAddForm" class="card-body bg-light border-bottom">
        <h5>Register a New Doctor</h5>
        <form @submit.prevent="addDoctor">
          <div class="row">
            <div class="col-md-6 mb-3">
              <input type="text" v-model="newDoctor.name" class="form-control" placeholder="Dr. Full Name" required>
            </div>
            <div class="col-md-6 mb-3">
              <input type="email" v-model="newDoctor.email" class="form-control" placeholder="Email Address" required>
            </div>
            <div class="col-md-4 mb-3">
              <input type="password" v-model="newDoctor.password" class="form-control" placeholder="Password" required>
            </div>
            <div class="col-md-4 mb-3">
              <input type="number" v-model="newDoctor.department_id" class="form-control" placeholder="Department ID (e.g., 1)" required>
            </div>
            <div class="col-md-4 mb-3">
              <input type="number" v-model="newDoctor.career_start_year" class="form-control" placeholder="Start Year (e.g., 2015)">
            </div>
          </div>
          <button type="submit" class="btn btn-success btn-sm">Save Doctor</button>
        </form>
      </div>
      
      <div class="card-body">
        <p v-if="error" class="text-danger">{{ error }}</p>
        <p v-if="doctors.length === 0" class="text-muted">No doctors found. Please add one.</p>

        <table v-else class="table table-striped table-hover mt-2">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in doctors" :key="doc.id">
              <td>{{ doc.id }}</td>
              <td>{{ doc.name }}</td>
              <td>
                <button @click="deleteDoctor(doc.id)" class="btn btn-sm btn-outline-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  data() {
    return {
      doctors: [], 
      error: null,
      showAddForm: false, // Controls if the form is visible
      newDoctor: {        // Holds the typed input
        name: '',
        email: '',
        password: '',
        department_id:'',
        career_start_year:''
      }
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    },

    // 1. FETCH DOCTORS
    async fetchDoctors() {
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:5000/api/doctors', {
          headers: { 'Authentication-Token': token }
        });
        if (response.ok) {
          this.doctors = await response.json();
        } else {
          this.error = "Failed to load doctors.";
        }
      } catch (err) {
        console.error(err);
      }
    },

    // 2. ADD DOCTOR
    async addDoctor() {
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:5000/api/doctors', {
          method: 'POST',
          headers: {
            'Authentication-Token': token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newDoctor)
        });

        const data = await response.json();

        if (response.ok) {
          alert("Doctor added successfully!");
          this.showAddForm = false; // Hide the form
          this.newDoctor = { name: '', email: '', password: '', department_id: '', career_start_year: '' }; // Clear inputs
          this.fetchDoctors(); // Refresh the table!
        } else {
          alert("Error: " + data.message);
        }
      } catch (err) {
        console.error(err);
        alert("Could not connect to server.");
      }
    },

    // 3. DELETE DOCTOR
    async deleteDoctor(id) {
      if (!confirm("Are you sure you want to delete this doctor?")) return;
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`http://127.0.0.1:5000/api/doctors/${id}`, {
          method: 'DELETE',
          headers: { 'Authentication-Token': token }
        });
        if (response.ok) {
          this.fetchDoctors(); // Refresh the table
        }
      } catch (err) {
        console.error(err);
      }
    }
  },
  mounted() {
    this.fetchDoctors();
  }
}
</script>