<template>
  <div id="app">
    <NavBar />

    <main>
      <router-view/>
    </main>
  </div>
</template>

<script>
// 1. Ensure the path exactly matches your folder structure and capitalization!
import NavBar from './components/NavBar.vue'; 

export default {
  name: 'App',
  components: {
    
    NavBar 
  }
}
</script>

<style>

</style>