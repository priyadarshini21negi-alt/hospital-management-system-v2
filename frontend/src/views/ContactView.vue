<template>
  <div class="contact-wrapper" style="padding-top: 100px; min-height: 80vh; background: linear-gradient(135deg, #fdfdfd 0%, #e8f0f8 100%);">
    <div class="container pb-5">
      
      <div class="text-center mb-5">
        <p class="text-uppercase fw-bold mb-1" style="color: #5a7d9a; letter-spacing: 2px;">Get In Touch</p>
        <h2 class="display-6 fw-bold" style="color: #1f4e79;">Contact Information</h2>
      </div>

      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          
          <div class="glass-card p-5 rounded-4 shadow-sm" style="background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.8);">
            
            <ul class="list-unstyled mb-5">
              
              <li class="d-flex align-items-center mb-4">
                <i class="bi bi-geo-alt-fill fs-2 me-4" style="color: #1f4e79;"></i>
                <div>
                  <h6 class="mb-0 fw-bold" style="color: #1f4e79;">Address</h6>
                  <span style="color: #5a7d9a;">Wayne Manor, Gotham City</span>
                </div>
              </li>
              
              <li class="d-flex align-items-center mb-4">
                <i class="bi bi-envelope-fill fs-2 me-4" style="color: #1f4e79;"></i>
                <div>
                  <h6 class="mb-0 fw-bold" style="color: #1f4e79;">Email</h6>
                  <a href="mailto:admin@healix.com" class="text-decoration-none" style="color: #5a7d9a;">support@healix.com</a>
                </div>
              </li>
              
              <li class="d-flex align-items-center">
                <i class="bi bi-globe fs-2 me-4" style="color: #1f4e79;"></i>
                <div>
                  <h6 class="mb-0 fw-bold" style="color: #1f4e79;">Website</h6>
                  <router-link to="/" class="text-decoration-none" style="color: #5a7d9a;">www.healixhospital.com</router-link>
                </div>
              </li>

            </ul>

            <hr style="border-color: #5a7d9a; opacity: 0.2;">

            <div class="text-center mt-4">
              <h6 class="fw-bold mb-3" style="color: #1f4e79;">Follow Us</h6>
              <div class="d-flex justify-content-center gap-4">
                <a href="#" class="social-icon"><i class="bi bi-twitter-x fs-4"></i></a>
                <a href="#" class="social-icon"><i class="bi bi-instagram fs-4"></i></a>
                <a href="#" class="social-icon"><i class="bi bi-facebook fs-4"></i></a>
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.social-icon {
  color: #5a7d9a;
  transition: all 0.3s ease;
  display: inline-block; 
}

.social-icon:hover {
  color: #1f4e79;
  transform: translateY(-4px);
}
</style>