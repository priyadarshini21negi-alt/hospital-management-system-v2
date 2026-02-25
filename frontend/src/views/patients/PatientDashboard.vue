<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-2 border-success-subtle">
      <h2 class="fw-bolder text-success tracking-tight">
        <i class="bi bi-person-heart me-2 text-primary"></i>Patient Portal
      </h2>
      <button @click="logoutAccount" class="btn btn-outline-danger px-4 fw-semibold shadow-sm rounded-pill">
        Sign Out
      </button>
    </div>

    <div class="row gy-4">
      <div class="col-lg-5">
        <div class="card shadow-sm border-0 bg-success bg-opacity-10 rounded-4">
          <div class="card-header bg-success text-white py-3 rounded-top-4 border-0">
            <h5 class="mb-0 fw-bold"><i class="bi bi-calendar-plus me-2"></i>Schedule a Visit</h5>
          </div>
          <div class="card-body bg-white border border-success border-opacity-25 rounded-bottom-4 p-4">
            <form @submit.prevent="submitBooking">
              
              <div class="mb-3">
                <label class="form-label small fw-bold text-secondary">Step 1: Select a Specialist</label>
                <select class="form-select border-success-subtle" v-model="bookingForm.doctor_id" @change="loadAvailableSlots" required>
                  <option value="" disabled>Choose your doctor...</option>
                  <option v-for="doc in availableDoctors" :key="doc.id" :value="doc.id">
                    Dr. {{ doc.name }} ({{ doc.department_name }})
                  </option>
                </select>
              </div>

              <div class="mb-4">
                <label class="form-label small fw-bold text-secondary">Step 2: Choose an Open Slot</label>
                <select class="form-select border-success-subtle" v-model="bookingForm.slot_id" :disabled="!bookingForm.doctor_id" required>
                  <option value="" disabled>
                    {{ openSlots.length === 0 && bookingForm.doctor_id ? 'No available slots right now' : 'Select an exact time...' }}
                  </option>
                  <option v-for="slot in openSlots" :key="slot.id" :value="slot.id">
                    {{ new Date(slot.start).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }} 
                    at {{ new Date(slot.start).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}
                  </option>
                </select>
              </div>

              <button type="submit" class="btn btn-success w-100 fw-bold shadow-sm" :disabled="!bookingForm.slot_id">
                Confirm Appointment
              </button>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-7">
        <div class="card shadow-sm border-0 rounded-4 overflow-hidden">
          <div class="card-header bg-light border-bottom py-3 d-flex justify-content-between align-items-center">
            <h5 class="mb-0 text-dark fw-bold"><i class="bi bi-clock-history me-2 text-primary"></i>My Medical History</h5>
            <span class="badge bg-secondary rounded-pill">{{ myAppointments?.length || 0 }} Visits</span>
          </div>
          
          <div class="card-body p-0" style="max-height: 500px; overflow-y: auto;">
            <div v-if="!myAppointments || myAppointments.length === 0" class="text-center py-5 text-muted bg-light">
              <i class="bi bi-folder-x fs-1 opacity-50"></i>
              <p class="mt-2 fw-medium">No appointment history found.</p>
            </div>
            
            <ul v-else class="list-group list-group-flush">
              <li class="list-group-item p-4 hover-bg" v-for="app in myAppointments" :key="app.id">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h6 class="fw-bolder text-dark mb-1">
                      <i class="bi bi-person-badge me-2 text-secondary"></i>{{ app.doctor_name }}
                    </h6>
                    <small class="text-muted fw-medium">
                      {{ new Date(app.date).toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}
                      at {{ new Date(app.date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}
                    </small>
                  </div>
                  <span class="badge px-3 py-2 rounded-pill shadow-sm" 
                        :class="app.status === 'Completed' ? 'bg-success' : 'bg-warning text-dark'">
                    {{ app.status }}
                  </span>
                </div>
                
                <div v-if="app.status === 'Completed' && app.treatment" class="mt-3 bg-light p-3 rounded-3 border border-secondary border-opacity-25">
                  <p class="mb-1 small"><strong class="text-primary">Diagnosis:</strong> {{ app.treatment.diagnosis }}</p>
                  <p class="mb-1 small"><strong class="text-primary">Prescription:</strong> {{ app.treatment.prescription }}</p>
                  <p class="mb-0 small text-muted mt-2 border-top pt-1" v-if="app.treatment.notes"><em>Note: {{ app.treatment.notes }}</em></p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientDashboard',
  data() {
    return {
      availableDoctors: [],
      openSlots: [], 
      myAppointments: [],
      bookingForm: {
        doctor_id: '',
        slot_id: '' // We send slot_id to the backend now, NOT a random datetime
      }
    }
  },
  methods: {
    logoutAccount() {
      localStorage.removeItem('auth_token');
      this.$router.push('/login');
    },

    async fetchDoctorList() {
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:5000/api/doctors', {
          headers: { 'Authentication-Token': token }
        });
        const data = await response.json();
        this.availableDoctors = Array.isArray(data) ? data : [];
      } catch (err) {
        console.error("Error fetching doctors:", err);
      }
    },

    async fetchAppointmentHistory() {
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:5000/api/patient/appointments', {
          headers: { 'Authentication-Token': token }
        });
        const data = await response.json();
        this.myAppointments = Array.isArray(data) ? data : [];
      } catch (err) {
        console.error("Error fetching history:", err);
      }
    },

    // Triggered when the user selects a doctor in the first dropdown
    async loadAvailableSlots() {
      this.bookingForm.slot_id = ''; // Reset slot choice
      this.openSlots = []; 
      
      if (!this.bookingForm.doctor_id) return;

      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`http://127.0.0.1:5000/api/doctor/${this.bookingForm.doctor_id}/slots`, {
          headers: { 'Authentication-Token': token }
        });
        const data = await response.json();
        this.openSlots = Array.isArray(data) ? data : [];
      } catch (err) {
        console.error("Error fetching slots:", err);
      }
    },

    async submitBooking() {
      try {
        const token = localStorage.getItem('auth_token');
        const payload = { slot_id: this.bookingForm.slot_id };

        const response = await fetch('http://127.0.0.1:5000/api/patient/appointments', {
          method: 'POST',
          headers: { 
            'Authentication-Token': token, 
            'Content-Type': 'application/json' 
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          alert("Appointment successfully secured!");
          this.bookingForm = { doctor_id: '', slot_id: '' }; 
          this.openSlots = []; 
          this.fetchAppointmentHistory(); // Instantly update the UI
        } else {
          const errorData = await response.json();
          alert(errorData.message);
        }
      } catch (err) {
        console.error("Booking error:", err);
      }
    }
  },
  mounted() {
    this.fetchDoctorList();
    this.fetchAppointmentHistory();
  }
}
</script>

<style scoped>
.tracking-tight { letter-spacing: -0.02em; }
.hover-bg { transition: background-color 0.2s ease; }
.hover-bg:hover { background-color: #f8f9fa; }

/* Custom scrollbar */
.card-body::-webkit-scrollbar { width: 6px; }
.card-body::-webkit-scrollbar-track { background: #f1f1f1; }
.card-body::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 4px; }
.card-body::-webkit-scrollbar-thumb:hover { background: #a8a8a8; }
</style>