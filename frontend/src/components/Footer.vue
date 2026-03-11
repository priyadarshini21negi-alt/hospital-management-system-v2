<template>
  <footer class="text-center py-3 border-top" style="background-color: #f8fbfd;">
    <p class="text-muted small mb-0">
      &copy; {{ currentYear }} Healix Hospital. All rights reserved.
    </p>
  </footer>
</template>

<script>
export default {
  name: 'FooterComponent',
  data() {
    return {
      currentYear: new Date().getFullYear()
    }
  }
}
</script>