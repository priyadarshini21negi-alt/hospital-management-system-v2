<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-2 border-success-subtle">
      <h2 class="fw-bolder text-success tracking-tight text-capitalize">
        <i class="bi bi-person-heart me-2 text-primary"></i>Welcome, {{ patientProfile.name || 'Patient' }}
      </h2>
      <button class="btn btn-outline-primary px-4 fw-semibold shadow-sm rounded-pill" data-bs-toggle="modal" data-bs-target="#editProfileModal">
          <i class="bi bi-pencil-square me-1"></i> Edit Profile
        </button>
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
                     {{ doc.name }} ({{ doc.department_name }})
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
                
                <div v-if="app.status === 'Booked'" class="mt-3 text-end border-top pt-2">
                  <button @click="cancelAppointment(app.id)" class="btn btn-sm btn-outline-danger shadow-sm rounded-pill px-3">
                    <i class="bi bi-x-circle me-1"></i> Cancel Visit
                  </button>
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
  <div class="modal fade" id="editProfileModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title fw-bold"><i class="bi bi-person-lines-fill me-2"></i>Edit My Profile</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close" id="closeProfileModal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label fw-bold text-secondary small">Full Name</label>
                <input type="text" class="form-control" v-model="patientProfile.name" required>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold text-secondary small">Phone Number</label>
                <input type="text" class="form-control" v-model="patientProfile.number" required>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold text-secondary small">Email (Read-Only)</label>
                <input type="email" class="form-control bg-light" v-model="patientProfile.email" disabled>
              </div>
              <button type="submit" class="btn btn-primary w-100 fw-bold mt-2">Save Changes</button>
            </form>
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
        slot_id: '' 
      },
      
      patientProfile: {
        name: '',
        number: '',
        email: ''
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
    async cancelAppointment(appointmentId) {
      if (!confirm("Are you sure you want to cancel this appointment?")) return;

      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`http://127.0.0.1:5000/api/patient/appointments/${appointmentId}`, {
          method: 'DELETE',
          headers: { 'Authentication-Token': token }
        });

        if (response.ok) {
          alert("Appointment cancelled.");
          this.fetchAppointmentHistory(); // Refresh the list
          
          // If the patient is currently viewing this doctor's slots, refresh the dropdown too
          if (this.bookingForm.doctor_id) {
            this.loadAvailableSlots(); 
          }
        } else {
          const errorData = await response.json();
          alert("Error: " + errorData.message);
        }
      } catch (err) {
        console.error("Cancel error:", err);
      }
    },

    async loadAvailableSlots() {
      this.bookingForm.slot_id = ''; 
      this.openSlots = []; 
      
      if (!this.bookingForm.doctor_id) return;

      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`http://127.0.0.1:5000/api/doctors/${this.bookingForm.doctor_id}/slots`, {
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
        const selectedSlot = this.openSlots.find(slot => slot.id === this.bookingForm.slot_id);
        if (!selectedSlot) return alert("Please select a valid time slot.");
        
        const payload = { 
          doctor_id: this.bookingForm.doctor_id,
          appointment_datetime: selectedSlot.start
         };

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
          this.fetchAppointmentHistory(); 
        } else {
          const errorData = await response.json();
          alert(errorData.message);
        }
      } catch (err) {
        console.error("Booking error:", err);
      }
    },

    // FIX 2: Added the methods to fetch and update the profile
    async loadProfile() {
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:5000/api/patient/profile', {
          headers: { 'Authentication-Token': token }
        });
        if (response.ok) {
          this.patientProfile = await response.json();
        }
      } catch (err) {
        console.error("Error loading profile:", err);
      }
    },

    async updateProfile() {
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:5000/api/patient/profile', {
          method: 'PUT',
          headers: { 
            'Authentication-Token': token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.patientProfile.name,
            number: this.patientProfile.number
          })
        });

        if (response.ok) {
          alert("Profile updated successfully!");
          document.getElementById('closeProfileModal').click();
        } else {
          const errorData = await response.json();
          alert("Error: " + errorData.message);
        }
      } catch (err) {
        console.error("Error updating profile:", err);
      }
    }
  },
  mounted() {
    this.fetchDoctorList();
    this.fetchAppointmentHistory();
    this.loadProfile(); // FIX 3: Load the profile when dashboard opens
  }
}
</script>