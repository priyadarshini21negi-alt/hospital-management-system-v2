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
import apiClient from '@/axios';
export default {
  name: 'AdminDashboard',
  data() {
    return {
     
      stats: { total_patients: 0, total_doctors: 0, total_appointments: 0 },
      
      searchQuery: '',
      patientSearchQuery: '',
      appSearchQuery: '',
      appCategory: '',
      
      doctors: [],
      patients: [],
      appointments: [],
      
      showAddForm: false,
      selectedDeptName: '',
      newDoctor: { name: '', username: '', password: '', department_id: '', career_start_year: '' },
      editingDoctor: null,
      editForm: { name: '', email:'', department_id: '', career_start_year: '' },
      
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
      try {
        const res = await apiClient.get('/api/admin/stats');
        this.stats = res.data;
      } catch (err) {
        console.error("Error fetching stats:", err);
      }
    },
      
    async fetchPatients() {
      try {
        const res = await apiClient.get('/api/patients', {
          params: { search: this.patientSearchQuery }
        });
        this.patients = res.data;
      } catch (err) {
        console.error("Error fetching patients:", err);
      }
    },

    async fetchDoctors() {
      try {
        const res = await apiClient.get('/api/doctors', {
          params: { search: this.searchQuery }
        });
        this.doctors = res.data;
      } catch (err) {
        console.error("Error fetching doctors:", err);
      }
    },

    async fetchAppointments() {
      try {
        const res = await apiClient.get('/api/admin/appointments', {
          params: { 
            search: this.appSearchQuery, 
            category: this.appCategory 
          }
        });
        this.appointments = res.data;
      } catch (err) {
        console.error("Error fetching appointments:", err);
      }
    },

    // --- DOCTOR ACTIONS ---
    updateDeptId() { 
      this.newDoctor.department_id = this.deptMapping[this.selectedDeptName]; 
    },

    async addDoctor() {
      const payload = {
        name: `Dr. ${this.newDoctor.name.trim()}`,
        email: `${this.newDoctor.username}@healix.com`,
        password: this.newDoctor.password,
        department_id: this.newDoctor.department_id,
        career_start_year: this.newDoctor.career_start_year
      };
      try {
        await apiClient.post('/api/doctors', payload);
        
        alert("Doctor Added");
        this.showAddForm = false;
        this.fetchDoctors();
        this.fetchStats();
        
        
        this.newDoctor = { name: '', username: '', password: '', department_id: '', career_start_year: '' };
        this.selectedDeptName = ''; 

      } catch (err) {
        
        const errMsg = err.response?.data?.message || err.response?.data?.response?.errors?.[0] || "Action Failed";
        alert("Error: " + errMsg);
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
      try {
        await apiClient.put(`/api/doctors/${this.editingDoctor}`, payload);
        
        this.editingDoctor = null;
        this.fetchDoctors();
      } catch (err) {
        const errMsg = err.response?.data?.message || err.response?.data?.response?.errors?.[0] || "Update Failed";
        alert("Error: " + errMsg);
      }
    },

    async deleteDoctor(id) {
      if (!confirm('Delete doctor profile and account?')) return;
      try {
        await apiClient.delete(`/api/doctors/${id}`);
        this.fetchDoctors();
        this.fetchStats();
      } catch (err) {
        alert("Error: " + (err.response?.data?.message || "Could not delete"));
      }
    },

    // --- PATIENT ACTIONS ---
    async deletePatient(id) {
      if (!confirm('Delete patient account?')) return;
      try {
        await apiClient.delete(`/api/patients/${id}`);
        this.fetchPatients();
        this.fetchStats();
      } catch (err) {
        alert("Error: " + (err.response?.data?.message || "Could not delete"));
      }
    },

    // --- APPOINTMENT ACTIONS ---
    async updateAppStatus(id, status) {
      try {
        await apiClient.put(`/api/admin/appointments/${id}`, { status });
        this.fetchAppointments();
      } catch (err) {
        alert("Error updating status: " + (err.response?.data?.message || "Failed"));
      }
    },

    async deleteAppointment(id) {
      if (!confirm('Delete appointment record?')) return;
      try {
        await apiClient.delete(`/api/admin/appointments/${id}`);
        this.fetchAppointments();
        this.fetchStats();
      } catch (err) {
        alert("Error: " + (err.response?.data?.message || "Could not delete"));
      }
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