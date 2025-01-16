<template>
    <div v-if="isAdmin">

        <Navbar />
        <div v-if="!hasChildRoute">
            <div class="admin-dashboard">
                <div>
                    <h1>Welcome Admin</h1>
                    <p>The administrator dashboard for the Influencer Engagement and Sponsorship Coordination Platform helps monitor and control all the workings of the application.</p>
                </div>
            </div>
        </div>

        <router-view></router-view>

    </div>

    <div v-else>
        <h1>You are not authorized to view this page.</h1>
    </div>

</template>

<script>

import { mapGetters } from 'vuex';
import Navbar from '@/components/Navbar.vue';
import axios from '../assets/axios.js';

export default {
    name: 'AdminDashboard',
    components: {
        Navbar,
    },
    computed: {
        ...mapGetters(['isLoggedIn', 'userRole']),
        isAdmin() {
            return this.isLoggedIn && this.userRole === 'Admin';
        },
        hasChildRoute() {
            return this.$route.matched.length > 1;
        },
    },
    created() {
        if (this.isAdmin) {
            axios.get('/admin/dashboard')
                .then (response => {
                    console.log('Admin Dashboard:', response.data.message);
                    // alert('Successfully logged in to Admin Dashboard');
                })
                .catch (error => {
                    console.error('Error fetching admin dashboard:', error.response ? error.response.data : error.message);
                    // alert('Error fetching admin dashboard');
                });
        }
    }
}
</script>

<style scoped>
.admin-dashboard {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 225px;
    margin-bottom: 225px;
    padding-left: 50px;
    padding-right: 50px;
}
h1 {
    font-weight: bold;
    font-size: 3.5em;
    text-align: center;
}
</style>
