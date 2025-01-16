<template>
    <div>
        <div class="platform-influencers">
            <div>
                <h1>Influencers On Platform</h1>
                <p>These are all the influencers on the platform.</p>
            </div>
        </div>

        <div id="filter-button">
            <button @click="pushtoSearch" type="button" class="btn btn-outline-secondary">Apply Filters</button>
        </div>

        <div v-if="platform_influencers.length === 0">
            <p id="no-results">No influencers to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Influencer Name</th>
                            <th>Category</th>
                            <th>Reach</th>
                            <th>Details</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(influencer, index) in platform_influencers" :key="influencer.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ influencer.name }}</td>
                            <td>{{ influencer.category }}</td>
                            <td>{{ influencer.reach }}</td>
                            <td><router-link :to="{ name: 'SponsorViewInfluencerDetails', params: { id: influencer.id } }"><button class="btn btn-warning">View</button></router-link></td>
                            <td><button @click="goToCreateAdrequestPage(influencer.id)" class="btn btn-success">Request</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: 'PlatformInfluencers',
    data() {
        return {
            platform_influencers: {},
        };
    },
    created() {
        this.getPlatformInfluencers();
    },
    methods: {
        async getPlatformInfluencers() {
            try {
                const response = await axios.get('/sponsor/platform_influencers');
                this.platform_influencers = response.data.platform_influencers;
            } catch (error) {
                console.error('Error fetching influencers:', error.response ? error.response.data : error.message);
            }
        },
        goToCreateAdrequestPage(influencer_id) {
            if (influencer_id) {
                this.$router.push({ name: 'SponsorCreateAdrequest', params: { id: influencer_id }, query: { type: 'influencer' } });
            } else {
                console.error('Influencer ID is not available');
            }
        },
        pushtoSearch() {
            this.$router.push({ name: 'SponsorSearchInfluencers' });
        },   
    }
}
</script>

<style scoped>
.platform-influencers {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
    margin-bottom: 10px;
    padding-left: 10px;
    padding-right: 10px;
}
h1 {
    font-size: 2.5em;
    text-align: center;
    font-weight: bold;
    color: #E76F51;
    font-style: oblique;
    padding: 10px;
}
p {
    font-size: 1em;
    font-style: oblique;
    text-align: center;
    padding-left: 25px;
    padding-right: 25px;
    color: #353535;
}
#no-results {
    padding: 20px;
}
.table-container {
    padding-left: 20px;
    padding-right: 20px;
    width: 100%;
    text-align: center;
    vertical-align: middle;
}
th {
    vertical-align: middle;
}
td {
    vertical-align: middle;
}
#filter-button {
    padding-left: 20px;
    padding-right: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}
</style>
