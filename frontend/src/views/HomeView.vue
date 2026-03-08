<template>

<div 
  data-bs-spy="scroll"
  data-bs-target="#navbar-hms"
  data-bs-root-margin="0px 0px -40%" 
  data-bs-smooth-scroll="true"
  class="scrollspy-example"
  tabindex="0"
>
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
<section id="services-section" style="height: 100vh; padding-top: 80px;">
      <h2>Our Services</h2>
      <p>This is the services area.</p>
    </section>
  
<!--ABOUT-->
  <section id="about-section" style="height: 100vh; padding-top: 80px;">
      <h2>About Us</h2>
      <p>Information about HMS V2 goes here.</p>
    </section>

<!--TESTIMONIALS-->
    <section id="testimonials-section" style="height: 100vh; padding-top: 80px;">
      <h2>Testimonials</h2>
      <p>What our patients say about us.</p>
    </section>

<!------------------------ -->
</div>
</template>


<script>
export default {
  name: 'HomeView',
  
  
}
</script>