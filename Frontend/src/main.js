import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';
import axios from 'axios';
import vuetify from './plugins/vuetify';

axios.defaults.withCredentials = true
axios.defaults.baseURL ='http://stopmurdoch.com:5000/api/'; //  'http://127.0.0.1:5000/api/'; // 
Vue.config.productionTip = false

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
