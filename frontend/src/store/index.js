import { createStore } from 'vuex'
import axios, { setAuthenticationToken } from '../assets/axios.js';

export default createStore({
  state: {
    username : null || localStorage.getItem('username'),
    role : null || localStorage.getItem('role'),
    token : null || localStorage.getItem('token'),
    id : null || localStorage.getItem('id'),
  },
  getters: {
    isLoggedIn: state => !!state.token,
    userRole: state => state.role,
  },
  mutations: {
    SET_USER_DATA(state, userData){
      state.username = userData.username
      state.role = userData.role
      state.token = userData.token
      state.id = userData.id

      localStorage.setItem('username', userData.username);
      localStorage.setItem('role', userData.role);
      localStorage.setItem('token', userData.token);
      localStorage.setItem('id', userData.id);

      setAuthenticationToken(userData.token);
      console.log('User data set in Vuex:', userData); // Debug log
    },
    CLEAR_USER_DATA(state){
      state.username = null;
      state.role = null;
      state.token = null;
      state.id = null;

      localStorage.removeItem('username');
      localStorage.removeItem('role');
      localStorage.removeItem('token');
      localStorage.removeItem('id');

      setAuthenticationToken(null);
      console.log('User data cleared in Vuex'); // Debug log
    }

  },
  actions: {
    async login({ commit }, credentials){
      try {
        const response = await axios.post('/user/login', credentials);
        if (response && response.data) {
          commit('SET_USER_DATA', response.data);
          return response.data;
        } else {
          console.error("Login Failed: No response data");
          throw new Error("Login Failed: No response data");
        }
      } catch (error) {
        console.error("Login Failed: ", error.response ? error.response.data : error.message);
        throw error;
      }
    },
    logout({ commit }){
      commit('CLEAR_USER_DATA');
    }
  },
  modules: {
  }
})
