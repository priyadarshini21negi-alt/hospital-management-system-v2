<template>
  <nav id="navbar-hms" class="navbar navbar-expand-lg fixed-top ">
    <div class="container">
      <router-link class="navbar-brand d-flex align-items-center" to="/" @click="scrollToTop">
        <img src="/images/logo.png" alt="Healix Logo" class="nav-logo">
        <div class="brand-text-wrapper">
          <span class="brand-main">HEALIX</span>
          <span class="brand-sub">HOSPITAL</span>
        </div>
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#hmsNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="hmsNav">
        <ul class="navbar-nav mx-auto nav-pills">
          <li class="nav-item"><a class="nav-link" href="#home-section">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="#services-section">Services</a></li>
          <li class="nav-item"><a class="nav-link" href="#about-section">About Us</a></li>
          <li class="nav-item"><a class="nav-link" href="#testimonials-section">Testimonials</a></li>
        </ul>
        
        <div class="d-none d-lg-flex gap-2">
          <router-link to="/login" class="btn btn-sm btn-outline-primary">Login</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  methods: {
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.nav-logo {
  height: 50px;
  width: auto;
  margin-right: 10px;
}

.brand-text-wrapper {
  line-height: 1.1;
  display: flex;
  flex-direction: column;
}

.brand-main {
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: #1f4e79;
}

.brand-sub {
  font-size: 0.75rem;
  letter-spacing: 4px;
  color: #5a7d9a;
  font-weight: 600;
}

/* Nav Pill Customization */
.nav-link {
  color: #4a5568;
  font-weight: 500;
  margin: 0 5px;
  transition: all 0.2s ease-in-out;
}

#navbar-hms .nav-pills .nav-link.active {
  background-color: #e0f2fe !important;
  color: #1f4e79 !important;
  font-weight: 700;
}

.nav-link:hover {
  color: #1f4e79;
}

@media (max-width: 991px) {
  .navbar-nav {
    padding: 1rem 0;
  }
}
</style>