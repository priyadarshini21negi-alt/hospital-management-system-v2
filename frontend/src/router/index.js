import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/UserLogin.vue'
import AdminDashboard from '../views/AdminDashboard.vue' 


const routes = [
  {
    path: '/', name: 'home', component: HomeView
  },
  {
    path: '/login', name: 'login', component: LoginView
  },
  {
    path: '/about', name: 'about', component: () => import( '../views/AboutView.vue')
  },
  {
    path: '/admin-dashboard', name: 'AdminDashboard', component: AdminDashboard,
    meta : { requiresAuth: true, role:'admin'}
  },


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// ========================================== 
// Navigation Guard
// ==========================================
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token');
  const userRole = localStorage.getItem('user_role');

  // Check if the destination route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    
    // If no token exists, kick them to the login page
    if (!token) {
      console.warn("Access Denied: No Token Found");
      next({ path: '/login' });
    } 
    // If token exists, check if they have the correct role for this specific page
    else if (to.meta.role && to.meta.role !== userRole) {
      console.warn("Access Denied: Unauthorized Role");
      alert("You do not have permission to view this page.");
      next({ path: '/' }); // Send them back to home
    } 
    // If everything is good, let them through
    else {
      next(); 
    }
  } 
  // If the route does NOT require auth (like Home or Login), let them through
  else {
    next(); 
  }
})
export default router
