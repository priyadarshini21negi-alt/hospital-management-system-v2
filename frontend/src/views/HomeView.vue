<template>

<div class="hms-home-wrapper">
<!--HOME-->
<section id="home-section" style="min-height: 80vh; padding-top: 100px;">
  <div class="container">
    
    <div class="hero-wrapper p-4 rounded-5 shadow-sm" style="background: linear-gradient(135deg, #e0f4f1 0%, #d4eaf5 100%);">
      <div class="row align-items-center">
        
        <div class="col-lg-6 text-start mb-5 mb-lg-0">
          <!--transclucent div-->
          <div class="glass-card p-4 rounded-4 shadow-sm d-inline-block" style="background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.6);">
    
    <h2 class="display-4 fw-bold" style="color: #1f4e79;">Your Health,<br> Our Mission</h2>
    <p class="lead mb-4" style="color: #2c3e50;">We are committed to delivering advanced,<br> patient-centered healthcare with compassion <br>and excellence.</p>

    <div class="d-flex gap-3">
      <router-link to="/login" class="btn btn-primary px-4 py-2">
        Login
      </router-link> 
      <router-link to="/register" class="btn btn-outline-primary px-4 py-2 bg-white">
        Register
      </router-link>
    </div>
          </div>
        </div>

        <div class="col-lg-6 text-center">
          <img src="/images/dochome.png" alt="Doctor Consultation" class="img-fluid" style="max-height: 550px; mix-blend-mode: multiply;">
        </div>

      </div>
    </div>
    
  </div>
</section>
<!--SERVICES-->
<section id="services-section" style="min-height: 80vh; padding-top: 80px; padding-bottom: 80px;">
  <div class="container">
    <div class="text-center mb-5">
      <p class="text-uppercase fw-bold mb-1" style="color: #5a7d9a; letter-spacing: 2px;">Our Departments</p>
      <h2 class="display-6 fw-bold" style="color: #1f4e79;">For Your Health</h2>
    </div>

    <div class="row g-4 justify-content-center">
      <div class="col-lg-4 col-md-6">
        <div class="service-card p-4 rounded-4 shadow-sm text-center d-flex flex-column align-items-center justify-content-center h-100">
          <i class="bi bi-truck-front fs-1 mb-3 service-icon"></i>
          <h5 class="fw-bold mb-0 service-title">🩺 Emergency Medicine</h5>
        </div>
      </div>

      <div class="col-lg-4 col-md-6">
        <div class="service-card p-4 rounded-4 shadow-sm text-center d-flex flex-column align-items-center justify-content-center h-100">
          <i class="bi bi-stethoscope fs-1 mb-3 service-icon"></i>
          <h5 class="fw-bold mb-0 service-title">⚕︎ General Medicine</h5>
        </div>
      </div>

      <div class="col-lg-4 col-md-6">
        <div class="service-card p-4 rounded-4 shadow-sm text-center d-flex flex-column align-items-center justify-content-center h-100">
          <i class="bi bi-heart-pulse fs-1 mb-3 service-icon"></i>
          <h5 class="fw-bold mb-0 service-title">🫀 Cardiology</h5>
        </div>
      </div>

      <div class="col-lg-4 col-md-6">
        <div class="service-card p-4 rounded-4 shadow-sm text-center d-flex flex-column align-items-center justify-content-center h-100">
          <i class="bi bi-diagram-3 fs-1 mb-3 service-icon"></i>
          <h5 class="fw-bold mb-0 service-title">🧠 Neurology</h5>
        </div>
      </div>

      <div class="col-lg-4 col-md-6">
        <div class="service-card p-4 rounded-4 shadow-sm text-center d-flex flex-column align-items-center justify-content-center h-100">
          <i class="bi bi-ribbon fs-1 mb-3 service-icon"></i>
          <h5 class="fw-bold mb-0 service-title">🎗 Oncology</h5>
        </div>
      </div>

      <div class="col-lg-4 col-md-6">
        <div class="service-card p-4 rounded-4 shadow-sm text-center d-flex flex-column align-items-center justify-content-center h-100">
          <i class="bi bi-stars fs-1 mb-3 service-icon"></i>
          <h5 class="fw-bold mb-0 service-title">👤 Dermatology</h5>
        </div>
      </div>
    </div>
    </div>
    </section>

<!--ABOUT-->
  <section id="about-section" style="height: 100vh; padding-top: 80px;">
      <h2>About Us</h2>
      <p>Information about HMS V2 goes here.</p>
    </section>

<!--TESTIMONIALS-->
   <section id="testimonials-section" style="min-height: 80vh; padding-top: 80px; padding-bottom: 80px; background: linear-gradient(135deg, #fdfdfd 0%, #e8f0f8 100%);">
  <div class="container">
    <div class="text-center mb-5">
      <h2 class="display-6 fw-bold" style="color: #1f4e79;">Testimonials</h2>
      <p class="lead" style="color: #5a7d9a;">What our patients say about us.</p>
    </div>

    <div class="row g-4">
      <div class="col-md-4">
        <div class="glass-card p-4 rounded-4 shadow-sm h-100" style="background: rgba(255, 255, 255, 0.5); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.7);">
          <div class="d-flex align-items-center mb-3">
            <div class="rounded-circle d-flex align-items-center justify-content-center text-white fw-bold" style="width: 50px; height: 50px; background-color: #1f4e79;">
              JD
            </div>
            <div class="ms-3">
              <h5 class="mb-0 fw-bold" style="color: #1f4e79;">John Doe</h5>
              <small style="color: #5a7d9a;">Cardiology Patient</small>
            </div>
          </div>
          <p class="fst-italic text-muted mb-0">
            "The care I received at Healix Hospital was exceptional. The staff was incredibly attentive, and the facilities are state-of-the-art. I felt safe and well-cared for every step of the way."
          </p>
        </div>
      </div>

  


      <div class="col-md-4">
        <div class="glass-card p-4 rounded-4 shadow-sm h-100" style="background: rgba(255, 255, 255, 0.5); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.7);">
          <div class="d-flex align-items-center mb-3">
            <div class="rounded-circle d-flex align-items-center justify-content-center text-white fw-bold" style="width: 50px; height: 50px; background-color: #1f4e79;">
              JD
            </div>
            <div class="ms-3">
              <h5 class="mb-0 fw-bold" style="color: #1f4e79;">Jane Doe</h5>
              <small style="color: #5a7d9a;">Oncology</small>
            </div>
          </div>
          <p class="fst-italic text-muted mb-0">
            "Facing a cancer diagnosis is terrifying, but the oncology team at Healix provided not just cutting-edge treatment, but genuine compassion. They fought alongside me every single day, and I am forever grateful."
          </p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="glass-card p-4 rounded-4 shadow-sm h-100" style="background: rgba(255, 255, 255, 0.5); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.7);">
          <div class="d-flex align-items-center mb-3">
            <div class="rounded-circle d-flex align-items-center justify-content-center text-white fw-bold" style="width: 50px; height: 50px; background-color: #1f4e79;">
              DK
            </div>
            <div class="ms-3">
              <h5 class="mb-0 fw-bold" style="color: #1f4e79;">David Kim</h5>
              <small style="color: #5a7d9a;">Dermatology</small>
            </div>
          </div>
          <p class="fst-italic text-muted mb-0">
            "I struggled with a severe skin condition for years before coming to Healix. The specialists quickly diagnosed the root cause and created a personalized treatment plan. My skin and my confidence have completely transformed."
          </p>
        </div>
      </div>

    </div>
  </div>
</section>
<!------------------------ -->
<FooterComponent />
</div>
</template>


<script>
import FooterComponent from '@/components/Footer.vue'; 

/* scrollspy in js */
export default {
  name: 'HomeView',
  components: {
    FooterComponent
  },
  mounted() {
    
    this.$nextTick(() => {
     
      if (window.bootstrap) {
        
        new window.bootstrap.ScrollSpy(document.body, {
          target: '#navbar-hms',
          rootMargin: '0px 0px -20%'
        });
      }
    });
  },
  beforeUnmount() {
    
    if (window.bootstrap) {
      const spy = window.bootstrap.ScrollSpy.getInstance(document.body);
      if (spy) spy.dispose();
    }
  }
}
</script>

<style>
.department-card{
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease-in-out;
  cursor: pointer;
  min-height: 160px;
}
.service-icon, .service-title {
  color: #1f4e79;
  transition: color 0.3s ease-in-out;
}

/* inverting colours */
.service-card:hover {
  background-color: #1f4e79 !important;
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(31, 78, 121, 0.2) !important;
}

.service-card:hover .service-icon,
.service-card:hover .service-title {
  color: #ffffff !important;
}
</style>