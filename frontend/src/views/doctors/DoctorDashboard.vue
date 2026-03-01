<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-2 border-primary-subtle">
      <h2 class="fw-bolder text-primary tracking-tight">
        <i class="bi bi-heart-pulse-fill me-2 text-danger"></i>Doctor Portal
      </h2>
      <button @click="logoutAccount" class="btn btn-outline-danger px-4 fw-semibold shadow-sm rounded-pill">
        Sign Out
      </button>
    </div>

    <div class="row gy-4">
      
      <div class="col-lg-7 col-xl-8">
        <div class="d-flex align-items-center mb-3">
          <h4 class="mb-0 text-dark fw-bold">My Consultations</h4>
          <span class="badge bg-primary ms-3 rounded-pill">{{ consultations?.length || 0 }} Total</span>
        </div>

        <div v-if="!consultations || consultations.length === 0" class="text-center text-muted py-5 bg-light rounded-4 border border-dashed">
          <i class="bi bi-cup-hot fs-1 text-secondary opacity-50"></i>
          <h5 class="mt-3 fw-medium">No consultations booked yet.</h5>
          <p class="small">When patients book your slots, they will appear here.</p>
        </div>

        <div class="row g-3">
          <div class="col-md-6" v-for="record in consultations" :key="record.id">
            <div class="card h-100 doc-card shadow-sm border-0" 
                 :class="record.status === 'Completed' ? 'border-top border-success border-4' : 'border-top border-warning border-4'">
              
              <div class="card-body d-flex flex-column">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <span class="badge px-3 py-2 rounded-pill" 
                        :class="record.status === 'Completed' ? 'bg-success' : 'bg-warning text-dark'">
                    {{ record.status }}
                  </span>
                  <small class="text-secondary fw-semibold">
                    {{ new Date(record.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }) }}
                  </small>
                </div>
                
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <h5 class="card-title fw-bolder text-dark mb-0">
                    <i class="bi bi-person-circle me-2 text-primary"></i>{{ record.patient_name }}
                  </h5>
                  <button @click="viewPatientHistory(record.patient_id, record.patient_name)" class="btn btn-sm btn-outline-info rounded-pill shadow-sm" data-bs-toggle="modal" data-bs-target="#patientHistoryModal">
                    <i class="bi bi-journal-medical me-1"></i> History
                  </button>
                </div>

                <p class="text-muted small mb-3">
                  <i class="bi bi-clock me-2"></i>{{ new Date(record.date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}
                </p>

                <div v-if="record.status === 'Booked'" class="mt-auto">
                  <div v-if="activeTreatmentId !== record.id" class="d-flex gap-2">
                    <button @click="activeTreatmentId = record.id" class="btn btn-primary btn-sm w-100 fw-bold shadow-sm">
                      Provide Treatment
                    </button>
                    <button @click="cancelAppointment(record.id)" class="btn btn-outline-danger btn-sm w-100 fw-bold shadow-sm">
                      Cancel Visit
                    </button>
                  </div>
                  
                  <form v-if="activeTreatmentId === record.id" @submit.prevent="finalizeTreatment(record.id)" class="mt-3 bg-light p-3 rounded-3 border">
                    <div class="mb-2">
                      <label class="form-label small fw-bold text-secondary">Diagnosis</label>
                      <input type="text" v-model="prescriptionForm.diagnosis" class="form-control form-control-sm" required>
                    </div>
                    <div class="mb-2">
                      <label class="form-label small fw-bold text-secondary">Prescription Details</label>
                      <textarea v-model="prescriptionForm.prescription" class="form-control form-control-sm" rows="2" required></textarea>
                    </div>
                    <div class="mb-3">
                      <label class="form-label small fw-bold text-secondary">Private Notes</label>
                      <input type="text" v-model="prescriptionForm.notes" class="form-control form-control-sm">
                    </div>
                    <div class="d-flex gap-2">
                      <button type="submit" class="btn btn-success btn-sm w-100 fw-bold">Submit</button>
                      <button type="button" @click="activeTreatmentId = null" class="btn btn-outline-secondary btn-sm w-100">Cancel</button>
                    </div>
                  </form>
                </div>

                <div v-if="record.status === 'Completed' && record.treatment" class="bg-success bg-opacity-10 p-3 rounded-3 mt-auto border border-success border-opacity-25">
                  <p class="mb-1 small text-dark"><strong class="text-success">Diagnosis:</strong> {{ record.treatment.diagnosis }}</p>
                  <p class="mb-1 small text-dark"><strong class="text-success">Prescription:</strong> {{ record.treatment.prescription }}</p>
                  <p class="mb-0 small text-muted mt-2 border-top pt-1" v-if="record.treatment.notes"><em>Note: {{ record.treatment.notes }}</em></p>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-5 col-xl-4">
        <h4 class="mb-3 text-dark fw-bold">Manage Schedule</h4>
        
        <div class="card shadow-sm border-0 mb-4 bg-primary bg-opacity-10">
          <div class="card-body p-4">
            <h6 class="fw-bold mb-3 text-primary"><i class="bi bi-calendar-plus me-2"></i>Open a Time Slot</h6>
            <form @submit.prevent="submitNewAvailability">
              <div class="mb-3">
                <label class="form-label small fw-bold text-dark">Shift Start</label>
                <input type="datetime-local" class="form-control" v-model="availabilityForm.start" :min="getMinDate()" :max="getMaxDate()" required>
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold text-dark">Shift End</label>
                <input type="datetime-local" class="form-control" v-model="availabilityForm.end" :min="getMinDate()" :max="getMaxDate()" required>
              </div>
              <button type="submit" class="btn btn-primary w-100 fw-bold shadow-sm">Confirm Availability</button>
            </form>
          </div>
        </div>

        <div class="card shadow-sm border-0 overflow-hidden">
          <div class="card-header bg-white border-bottom py-3">
            <h6 class="mb-0 fw-bold text-dark">My Published Slots</h6>
          </div>
          <ul class="list-group list-group-flush" style="max-height: 400px; overflow-y: auto;">
            <li v-if="openSlots.length === 0" class="list-group-item text-muted text-center py-4 small bg-light">
              No upcoming slots published.
            </li>
            
            <li v-for="slot in openSlots" :key="slot.id" class="list-group-item d-flex justify-content-between align-items-center p-3 hover-bg">
              <div>
                <span class="d-block fw-bold text-dark">{{ new Date(slot.start).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }}</span>
                <small class="text-secondary fw-medium">
                  {{ new Date(slot.start).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }} - 
                  {{ new Date(slot.end).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}
                </small>
              </div>
              <div>
                <span v-if="slot.is_booked" class="badge bg-success shadow-sm"><i class="bi bi-check-circle me-1"></i>Booked</span>
                <button v-else @click="removeSlot(slot.id)" class="btn btn-sm btn-outline-danger shadow-sm fw-bold">
                  Delete Slot
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>

    </div>
  </div>

  <div class="modal fade" id="patientHistoryModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-info text-white">
          <h5 class="modal-title fw-bold"><i class="bi bi-file-medical me-2"></i>Medical History: {{ selectedPatientName }}</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body p-4 bg-light">
          
          <div v-if="!patientHistory || patientHistory.length === 0" class="text-center py-4 text-muted">
            <i class="bi bi-folder2-open fs-1 opacity-50"></i>
            <p class="mt-2 fw-medium">No prior medical history found for this patient.</p>
          </div>

          <ul v-else class="list-group list-group-flush rounded-3 shadow-sm">
            <li class="list-group-item p-3 mb-2 border-0 rounded-3" v-for="visit in patientHistory" :key="visit.id">
              <div class="d-flex justify-content-between border-bottom pb-2 mb-2">
                <span class="fw-bold text-dark"><i class="bi bi-h-square text-danger me-2"></i>Treated by: {{ visit.doctor_name }}</span>
                <small class="text-muted fw-bold">{{ new Date(visit.date).toLocaleDateString() }}</small>
              </div>
              <div v-if="visit.treatment">
                <p class="mb-1 small"><strong class="text-info">Diagnosis:</strong> {{ visit.treatment.diagnosis }}</p>
                <p class="mb-1 small"><strong class="text-info">Prescription:</strong> {{ visit.treatment.prescription }}</p>
                <p class="mb-0 small text-muted" v-if="visit.treatment.notes"><em>Notes: {{ visit.treatment.notes }}</em></p>
              </div>
            </li>
          </ul>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorDashboard',
  data() {
    return {
      consultations: [],
      openSlots: [],
      activeTreatmentId: null,
      prescriptionForm: {
        diagnosis: '',
        prescription: '',
        notes: ''
      },
      availabilityForm: {
        start: '',
        end: ''
      },
      // FIX: Added data properties for history modal
      patientHistory: [],
      selectedPatientName: ''
    }
  },
  methods: {
    getMinDate() {
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      return now.toISOString().slice(0, 16);
    },
    getMaxDate() {
      const limit = new Date();
      limit.setDate(limit.getDate() + 7);
      limit.setMinutes(limit.getMinutes() - limit.getTimezoneOffset());
      return limit.toISOString().slice(0, 16);
    },
    logoutAccount() {
      localStorage.removeItem('auth_token');
      this.$router.push('/login');
    },
    
    // --- Data Fetching ---
    async loadConsultations() {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) return;

        const response = await fetch('http://127.0.0.1:5000/api/doctor/appointments', { 
          headers: { 'Authentication-Token': token } 
        });
        
        const data = await response.json();
        
        if (response.ok && Array.isArray(data)) {
          this.consultations = data;
        } else {
          this.consultations = [];
        }
      } catch (err) {
        console.error("Error fetching consultations:", err);
        this.consultations = [];
      }
    },

    async loadSchedule() {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) return;

        const response = await fetch('http://127.0.0.1:5000/api/doctor/availability', { 
          headers: { 'Authentication-Token': token } 
        });
        
        const data = await response.json();
        
        if (response.ok) {
          if (Array.isArray(data)) {
            this.openSlots = data;
          } else if (data && typeof data === 'object') {
            const extractedArray = Object.values(data).find(val => Array.isArray(val));
            this.openSlots = extractedArray || [];
          } else {
            this.openSlots = [];
          }
        } else {
          this.openSlots = [];
        }
      } catch (err) {
        console.error("Error fetching schedule:", err);
        this.openSlots = [];
      }
    },
    async cancelAppointment(appointmentId) {
      if (!confirm("Are you sure you want to cancel this appointment? The patient will be notified.")) return;

      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`http://127.0.0.1:5000/api/doctor/appointments/${appointmentId}`, {
          method: 'PUT',
          headers: { 
            'Authentication-Token': token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ status: 'Cancelled' })
        });

        if (response.ok) {
          alert("Appointment cancelled successfully.");
          this.loadConsultations(); 
          this.loadSchedule();     
        } else {
          const errorData = await response.json();
          alert("Error: " + errorData.message);
        }
      } catch (err) {
        console.error("Error cancelling appointment:", err);
      }
    },
    
    async viewPatientHistory(patientId, patientName) {
      if (!patientId) {
        console.error("No patient ID provided");
        return;
      }
      
      this.selectedPatientName = patientName;
      this.patientHistory = []; 

      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`http://127.0.0.1:5000/api/doctor/patient/${patientId}/history`, {
          headers: { 'Authentication-Token': token }
        });
        
        const data = await response.json();
        if (response.ok) {
          this.patientHistory = data;
        } else {
          console.error("Failed to load history:", data.message);
        }
      } catch (err) {
        console.error("Error fetching patient history:", err);
      }
    },

    // --- Schedule Management ---
    async submitNewAvailability() {
      try {
        const token = localStorage.getItem('auth_token');
        const formattedStart = this.availabilityForm.start.replace('T', ' ') + ':00';
        const formattedEnd = this.availabilityForm.end.replace('T', ' ') + ':00';

        const response = await fetch('http://127.0.0.1:5000/api/doctor/availability', {
          method: 'POST',
          headers: { 
            'Authentication-Token': token, 
            'Content-Type': 'application/json' 
          },
          body: JSON.stringify({ 
            start_time: formattedStart, 
            end_time: formattedEnd 
          })
        });

        if (response.ok) {
          this.availabilityForm = { start: '', end: '' };
          this.loadSchedule(); 
        } else {
          const errorData = await response.json();
          alert("Error: " + (errorData.message || "Could not save slot"));
        }
      } catch (err) {
        console.error("Error adding slot:", err);
      }
    },

    async removeSlot(slotId) {
      if (!confirm("Are you sure you want to remove this available time slot?")) return;
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`http://127.0.0.1:5000/api/doctor/availability/${slotId}`, { 
          method: 'DELETE', 
          headers: { 'Authentication-Token': token } 
        });
        
        if (response.ok) {
          this.loadSchedule();
        } else {
          const errorData = await response.json();
          alert(errorData.message);
        }
      } catch (err) {
        console.error("Error deleting slot:", err);
      }
    },

    // --- Treatment Management ---
    async finalizeTreatment(appointmentId) {
      try {
        const token = localStorage.getItem('auth_token');
        const payload = {
          appointment_id: appointmentId,
          diagnosis: this.prescriptionForm.diagnosis,
          prescription: this.prescriptionForm.prescription,
          notes: this.prescriptionForm.notes
        };

        const response = await fetch('http://127.0.0.1:5000/api/doctor/appointments', {
          method: 'POST',
          headers: { 
            'Authentication-Token': token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          this.activeTreatmentId = null;
          this.prescriptionForm = { diagnosis: '', prescription: '', notes: '' };
          this.loadConsultations();
        } else {
          const errorData = await response.json();
          alert(errorData.message);
        }
      } catch (err) {
        console.error("Error finalizing treatment:", err);
      }
    }
  },
  mounted() {
    this.loadConsultations();
    this.loadSchedule();
  }
}
</script>