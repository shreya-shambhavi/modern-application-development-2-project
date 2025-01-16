import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/styles.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import axios, { setAuthenticationToken } from './assets/axios.js';

// Set the token in the axios headers
const token = store.state.token;
if (token) {
  setAuthenticationToken(token);
}

createApp(App).use(store).use(router).mount('#app')
