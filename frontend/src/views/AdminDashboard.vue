<template>
  <div class="container py-4 mt-5 pt-4">
<!--HEADER-->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-semibold text-primary">
        <i class="bi bi-speedometer2 me-2"></i>Admin Dashboard
      </h2>
      <button @click="logout" class="btn btn-outline-danger px-4 shadow-sm">
        Logout
      </button>
    </div>
<!--NUMBER OF PATIENTS, DOCTORS AND APPOINTMENTS-->
    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <div class="card bg-primary text-white shadow-sm border-0 h-100">
          <div class="card-body text-center py-4">
            <h6 class="text-uppercase small fw-bold opacity-75">Total Patients</h6>
            <h2 class="mb-0 fw-bold">{{ stats.total_patients }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-success text-white shadow-sm border-0 h-100">
          <div class="card-body text-center py-4">
            <h6 class="text-uppercase small fw-bold opacity-75">Total Doctors</h6>
            <h2 class="mb-0 fw-bold">{{ stats.total_doctors }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-info text-white shadow-sm border-0 h-100">
          <div class="card-body text-center py-4">
            <h6 class="text-uppercase small fw-bold opacity-75">Total Appointments</h6>
            <h2 class="mb-0 fw-bold">{{ stats.total_appointments }}</h2>
          </div>
        </div>
      </div>
    </div>


<div class="row g-4 mb-4">
<!--PATIENT TABLE-->
  <div class="col-lg-6 d-flex flex-column">
    <div class="card shadow-sm border-0 flex-grow-1 mb-0">
      <div class="card-header bg-success text-white py-3">
        <h4 class="mb-0 fw-semibold"><i class="bi bi-people-fill me-2"></i>Manage Patients</h4>
      </div>
      <!--patient search bar-->
      <div class="card-body border-bottom bg-light">
        <div class="input-group shadow-sm">
          <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
          <input type="text" class="form-control" v-model="patientSearchQuery" @input="fetchPatients" placeholder="Search by Name or ID">
          <button class="btn btn-outline-secondary" @click="patientSearchQuery='';fetchPatients()">Clear</button>
        </div>
      </div>
      <div class="card-body table-responsive">
        <div v-if="patients.length === 0" class="text-center py-4 text-muted">
          <i class="bi bi-folder-x fs-2"></i>
          <p>No patients found</p>
        </div>
        <table v-else class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr><th>ID</th><th>Name</th><th>Contact</th><th class="text-end">Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="patient in patients" :key="patient.id">
              <td>{{ patient.id }}</td>
              <td>{{ patient.name }}</td>
              <td>{{ patient.number || 'N/A' }}</td>
              <td class="text-end">
                <button @click="deletePatient(patient.id)" class="btn btn-sm btn-outline-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
<!--DOCTOR TABLE-->
  <div class="col-lg-6 d-flex flex-column">
    <div class="card shadow-sm border-0 flex-grow-1 mb-0">
      <div class="card-header bg-success text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="mb-0 fw-semibold"><i class="bi bi-person-badge-fill me-2"></i>Manage Doctors</h4>
        <button @click="showAddForm = !showAddForm; editingDoctor=null" class="btn btn-light btn-sm px-3 shadow-sm">
          {{ showAddForm ? 'Cancel' : '+ Add Doctor' }}
        </button>
      </div>

      <div class="card-body border-bottom bg-light">
        <div class="input-group shadow-sm">
          <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
          <input type="text" class="form-control" v-model="searchQuery" @input="fetchDoctors" placeholder="Name or Specialization">
          <button class="btn btn-outline-secondary" @click="searchQuery='';fetchDoctors()">Clear</button>
        </div>
      </div>

      <transition name="fade">
        <div v-if="showAddForm" class="card-body bg-light border-bottom">
            <h5 class="text-secondary mb-3 fw-semibold">Register New Doctor</h5>
            <form @submit.prevent="addDoctor">
                <div class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label small text-muted">Full Name</label>
                        <input type="text" v-model="newDoctor.name" class="form-control" placeholder="John Doe" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label small text-muted">Username (@healix.com)</label>
                        <input type="text" v-model="newDoctor.username" class="form-control" placeholder="johndoe" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label small text-muted">Password</label>
                        <input type="password" v-model="newDoctor.password" class="form-control" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label small text-muted">Department</label>
                        <select class="form-select" v-model="selectedDeptName" @change="updateDeptId" required>
                            <option disabled value="">Select Department</option>
                            <option v-for="(id, name) in deptMapping" :key="id">{{ name }}</option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label small text-muted">Career Start Year</label>
                        <input type="number" v-model="newDoctor.career_start_year" class="form-control" placeholder="2015">
                    </div>
                    <div class="col-12 mt-3">
                        <button type="submit" class="btn btn-success px-4">Save Doctor</button>
                    </div>
                </div>
            </form>
        </div>
      </transition>

      <transition name="fade">
        <div v-if="editingDoctor" class="card-body bg-warning-subtle border-bottom">
            <h5 class="fw-semibold mb-3">Edit Doctor Profile</h5>
            <form @submit.prevent="submitEdit">
                <div class="row g-3">
                    <div class="col-md-3">
                        <label class="form-label small text-muted">Name</label>
                        <input type="text" v-model="editForm.name" class="form-control" required>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label small text-muted">Email</label>
                        <div class="input-group">
                            <input type="text" v-model="editForm.email" class="form-control" required>
                            <span class="input-group-text bg-light text-muted">@healix.com</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label small text-muted">Department</label>
                        <select class="form-select" v-model="editForm.department_id" required> 
                            <option v-for="(id, name) in deptMapping" :key="id" :value="id">
                                {{ name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label small text-muted">Start Year</label>
                        <input type="number" v-model="editForm.career_start_year" class="form-control">
                    </div>
                    <div class="col-12 mt-3">
                        <button class="btn btn-warning px-4 me-2 shadow-sm">Update</button>
                        <button type="button" class="btn btn-outline-secondary px-4 shadow-sm" @click="editingDoctor=null">Cancel</button>
                    </div>
                </div>
            </form>
        </div>
      </transition>

      <div class="card-body table-responsive">
        <div v-if="doctors.length === 0" class="text-center py-4 text-muted">
          <p>No doctors found</p>
        </div>
        <table v-else class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr><th>ID</th><th>Name</th><th>Department</th><th class="text-end">Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="doc in doctors" :key="doc.id">
              <td>{{ doc.id }}</td>
              <td>{{ doc.name }}</td>
              <td>{{ doc.department_name }}</td>
              <td class="text-end">
                <button @click="startEdit(doc)" class="btn btn-sm btn-outline-primary me-2">Edit</button>
                <button @click="deleteDoctor(doc.id)" class="btn btn-sm btn-outline-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

</div>

  <!----------------------------------------------------------->
  <!--APPOINTMENT TABLE-->
  <!----------------------------------------------------------->

    <div class="card shadow-sm border-0">
      <div class="card-header bg-primary text-white py-3">
        <h4 class="mb-0 fw-semibold"><i class="bi bi-calendar-check me-2"></i>All Appointments</h4>
      </div>
      <div class="card-body border-bottom bg-light">
        <div class="row g-3">
          <div class="col-md-6">
            <input type="text" class="form-control shadow-sm" v-model="appSearchQuery" @input="fetchAppointments" placeholder="Search Doctor, Patient or Status">
          </div>
          <div class="col-md-6">
            <select class="form-select shadow-sm" v-model="appCategory" @change="fetchAppointments">
              <option value="">All Appointments</option>
              <option value="upcoming">Upcoming</option>
              <option value="past">Past</option>
            </select>
          </div>
        </div>
      </div>
      <div class="card-body">
        <div v-if="appointments.length === 0" class="text-center py-4 text-muted">
          <p>No appointments scheduled.</p>
        </div>
        <table v-else class="table table-hover align-middle">
          <thead class="table-light">
            <tr><th>Date & Time</th><th>Doctor</th><th>Patient</th><th>Status</th><th class="text-end">Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="app in appointments" :key="app.id">
              <td>{{ new Date(app.date).toLocaleString() }}</td>
              <td>{{ app.doctor_name }}</td>
              <td>{{ app.patient_name }}</td>
              <td><span :class="getStatusClass(app.status)">{{ app.status }}</span></td>
              <td class="text-end">
                <button v-if="app.status !== 'Cancelled'" @click="updateAppStatus(app.id, 'Cancelled')" class="btn btn-sm btn-outline-warning me-2">Cancel</button>
                <button @click="deleteAppointment(app.id)" class="btn btn-sm btn-outline-danger">Delete</button>
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
      // Stats
      stats: { total_patients: 0, total_doctors: 0, total_appointments: 0 },
      // Search Queries
      searchQuery: '',
      patientSearchQuery: '',
      appSearchQuery: '',
      appCategory: '',
      // Data Arrays
      doctors: [],
      patients: [],
      appointments: [],
      // Doctor Form States
      showAddForm: false,
      selectedDeptName: '',
      newDoctor: { name: '', username: '', password: '', department_id: '', career_start_year: '' },
      editingDoctor: null,
      editForm: { name: '', email:'', department_id: '', career_start_year: '' },
      // Mappings
      deptMapping: {
        "Cardiology": 1, "Dermatology": 2, "Emergency Medicine": 3,
        "General Medicine": 4, "Neurology": 5, "Oncology": 6
      }
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    },

    // --- FETCHING LOGIC ---
    async fetchStats() {
      const res = await fetch('http://127.0.0.1:5000/api/admin/stats', {
        headers: { 'Authentication-Token': localStorage.getItem('auth_token') }
      });
      if (res.ok) this.stats = await res.json();
    },

    async fetchPatients() {
      let url = 'http://127.0.0.1:5000/api/patients';
      if (this.patientSearchQuery) url += `?search=${this.patientSearchQuery}`;
      const res = await fetch(url, { headers: { 'Authentication-Token': localStorage.getItem('auth_token') } });
      if (res.ok) this.patients = await res.json();
    },

    async fetchDoctors() {
      let url = 'http://127.0.0.1:5000/api/doctors';
      if (this.searchQuery) url += `?search=${this.searchQuery}`;
      const res = await fetch(url, { headers: { 'Authentication-Token': localStorage.getItem('auth_token') } });
      if (res.ok) this.doctors = await res.json();
    },

    async fetchAppointments() {
      let url = `http://127.0.0.1:5000/api/admin/appointments?search=${this.appSearchQuery}&category=${this.appCategory}`;
      const res = await fetch(url, { headers: { 'Authentication-Token': localStorage.getItem('auth_token') } });
      if (res.ok) this.appointments = await res.json();
    },

    // --- DOCTOR ACTIONS ---
    updateDeptId() { this.newDoctor.department_id = this.deptMapping[this.selectedDeptName]; },

    async addDoctor() {
      const data = {
        name: `Dr. ${this.newDoctor.name.trim()}`,
        email: `${this.newDoctor.username}@healix.com`,
        password: this.newDoctor.password,
        department_id: this.newDoctor.department_id,
        career_start_year: this.newDoctor.career_start_year
      };
      const res = await fetch('http://127.0.0.1:5000/api/doctors', {
        method: 'POST',
        headers: { 'Authentication-Token': localStorage.getItem('auth_token'), 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (res.ok) {
        alert("Doctor Added");
        this.showAddForm = false;
        this.fetchDoctors();
        this.fetchStats();
        
        // emptying the boxes when adding new doc 
        this.newDoctor = { name: '', username: '', password: '', department_id: '', career_start_year: '' };
        this.selectedDeptName = ''; 

      } else {
        const errorData = await res.json().catch(() => ({}));
        const errMsg = errorData.message 
                    || (errorData.response && errorData.response.errors ? errorData.response.errors[0] : null) 
                    || JSON.stringify(errorData);
                    
        alert("Action Failed: " + errMsg);
      }
      
    },
    startEdit(doc) {
      this.editingDoctor = doc.id;
      const emailPrefix = doc.email ? doc.email.split('@')[0] : '';

      this.editForm = { 
        name: doc.name, 
        email: emailPrefix,
        department_id: doc.department_id, 
        career_start_year: doc.career_start_year };
    },

    async submitEdit() {
      const payload = {
        name: this.editForm.name,
        email: `${this.editForm.email}@healix.com`, 
        department_id: this.editForm.department_id,
        career_start_year: this.editForm.career_start_year
      };

      const res = await fetch(`http://127.0.0.1:5000/api/doctors/${this.editingDoctor}`, {
        method: 'PUT',
        headers: { 'Authentication-Token': localStorage.getItem('auth_token'), 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (res.ok) {
        this.editingDoctor = null;
        this.fetchDoctors();
      } else {
        const errorData = await res.json().catch(() => ({}));
        const errMsg = errorData.message || (errorData.response?.errors?.[0]) || JSON.stringify(errorData);
        alert("Action Failed: " + errMsg);
      }
    },

    async deleteDoctor(id) {
      if (!confirm('Delete doctor profile and account?')) return;
      await fetch(`http://127.0.0.1:5000/api/doctors/${id}`, {
        method: 'DELETE',
        headers: { 'Authentication-Token': localStorage.getItem('auth_token') }
      });
      this.fetchDoctors();
      this.fetchStats();
    },

    // --- PATIENT ACTIONS ---
    async deletePatient(id) {
      if (!confirm('Delete patient account?')) return;
      await fetch(`http://127.0.0.1:5000/api/patients/${id}`, {
        method: 'DELETE',
        headers: { 'Authentication-Token': localStorage.getItem('auth_token') }
      });
      this.fetchPatients();
      this.fetchStats();
    },

    // --- APPOINTMENT ACTIONS ---
    async updateAppStatus(id, status) {
      await fetch(`http://127.0.0.1:5000/api/admin/appointments/${id}`, {
        method: 'PUT',
        headers: { 'Authentication-Token': localStorage.getItem('auth_token'), 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      });
      this.fetchAppointments();
    },

    async deleteAppointment(id) {
      if (!confirm('Delete appointment record?')) return;
      await fetch(`http://127.0.0.1:5000/api/admin/appointments/${id}`, {
        method: 'DELETE',
        headers: { 'Authentication-Token': localStorage.getItem('auth_token') }
      });
      this.fetchAppointments();
      this.fetchStats();
    },

    getStatusClass(status) {
      return {
        'badge bg-success': status === 'Booked',
        'badge bg-danger': status === 'Cancelled',
        'badge bg-info': status === 'Completed'
      };
    }
  },
  mounted() {
    this.fetchStats();
    this.fetchPatients();
    this.fetchDoctors();
    this.fetchAppointments();
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.card { border-radius: 12px; }
.table thead th { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
</style>