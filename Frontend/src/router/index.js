import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store';
import Home from '../views/Home.vue'
import Login from '../views/Login'
import Twitter from '../views/Twitter';
import Users from '../views/Users';

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {requiresAuth: true},
  },{
    path: '/login',
    name: "Login",
    component: Login,
  },
  {
    path: '/twitter',
    name: "Twitter",
    component: Twitter
  },{
    path: '/users',
    name: "Users",
    component: Users
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isAuthenticated) {
      next()
      return
    }
    next('/login')
  }
   else {
    next()
  }
  
})

export default router
