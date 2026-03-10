import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/UserLogin.vue'
import AdminDashboard from '../views/AdminDashboard.vue' 
import PatientDashboard from '../views/patients/PatientDashboard.vue'
import PatientRegister from '../views/patients/PatientRegistration.vue'
import DoctorDashboard from '../views/doctors/DoctorDashboard.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView },
  { 
    //lazy loading??
    path: '/about', name: 'about', component: () => import('../views/AboutView.vue') 
  },
  { 
    path: '/admin-dashboard', name: 'AdminDashboard', component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  { path: '/register', name: 'PatientRegister', component: PatientRegister },
  { 
    path: '/patient-dashboard', name: 'PatientDashboard', component: PatientDashboard,
    meta: { requiresAuth: true, role: 'patient' }
  },
  { 
    path: '/doctor-dashboard', name: 'DoctorDashboard', component: DoctorDashboard,
    meta: { requiresAuth: true, role: 'doctor' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  
  linkActiveClass: 'active',
  linkExactActiveClass: 'active'
})

// ========================================== 
// Navigation Guard
// ==========================================
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token');
  const userRole = localStorage.getItem('user_role');

  
  if (token && (to.path === '/login' || to.path === '/register')) {
    if (userRole === 'admin') return next('/admin-dashboard');
    if (userRole === 'doctor') return next('/doctor-dashboard');
    if (userRole === 'patient') return next('/patient-dashboard');
    return next('/');
  }

  if (to.matched.some(record => record.meta.requiresAuth)) {
    
    if (!token) {
      console.warn("Access Denied: No Token Found");
      next({ path: '/login' });
    } 
  
    else if (to.meta.role && to.meta.role !== userRole) {
      console.warn("Access Denied: Unauthorized Role");
      alert("You do not have permission to view this page.");
      next({ path: '/' }); 
    } 

    else {
      next(); 
    }
  } 
 
  else {
    next(); 
  }
})

export default router