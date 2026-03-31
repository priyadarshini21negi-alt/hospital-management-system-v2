<template>
  <div id="app" class="d-flex flex-column min-vh-100">
    <NavBar />

    <main class="flex-grow-1">
      <router-view/>
    </main>

    <Footer />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'; 
import Footer from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    NavBar,
    Footer 
  }
}
</script>

<style>

body {
  margin: 0;
  padding: 0;
}
</style>