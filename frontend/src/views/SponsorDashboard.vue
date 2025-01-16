<template>
    <div v-if="isSponsor">

        <Navbar />
        <div v-if="!hasChildRoute">
            <div class="sponsor-dashboard">
                <div>
                    <h1>Welcome {{ username }}</h1>
                    <p>The sponsor dashboard helps sponsors keep a track of their active campaigns as well as provide a platform to search and send requests to various influencers.</p>
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

import Navbar from '@/components/Navbar.vue';
import { mapGetters } from 'vuex';
import axios from '../assets/axios.js';

export default {
    name: 'SponsorDashboard',
    components: {
        Navbar,
    },
    computed: {
        ...mapGetters(['isLoggedIn', 'userRole']),
        isSponsor() {
            return this.isLoggedIn && this.userRole === 'Sponsor';
        },
        hasChildRoute() {
            return this.$route.matched.length > 1;
        },
        username() {
            return this.$store.state.username
        }
    },
    created() {
        if (this.isSponsor) {
            axios.get('/sponsor/dashboard')
                .then (response => {
                    console.log('Sponsor Dashboard:', response.data.message);
                })
                .catch (error => {
                    console.error('Error fetching sponsor dashboard:', error.response ? error.response.data : error.message);
                });
        }
    }
}

</script>

<style scoped>
.sponsor-dashboard {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 200px;
    margin-bottom: 200px;
    padding-left: 50px;
    padding-right: 50px;
}
h1 {
    font-weight: bold;
    font-size: 3.5em;
    text-align: center;
}
</style>
