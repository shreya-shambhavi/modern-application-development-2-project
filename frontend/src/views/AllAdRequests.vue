<template>
    <div>

        <div class="all-adrequests">
            <div>
                <h1>Ad Requests On Platform</h1>
                <p>These are all the ad requests on the platform.</p>
            </div>
        </div>
        <div v-if="all_adrequests.length === 0">
            <p id="no-results">No adrequest to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Campaign Name</th>
                            <th>Influencer Name</th>
                            <th>Request</th>
                            <th>Payment</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(adrequest, index) in all_adrequests" :key="adrequest.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ adrequest.campaign.name }}</td>
                            <td>{{ adrequest.influencer.name }}</td>
                            <td>{{ adrequest.title }}</td>
                            <td>{{ adrequest.payment }}</td>
                            <td><router-link :to="{ name: 'AdminViewAdrequestDetails', params: { id: adrequest.id } }"><button type="button" class="btn btn-warning">View</button></router-link></td>
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
    name: 'AllAdRequests',
    data() {
        return {
            all_adrequests: {},
        };
    },
    created() {
        this.getAllAdRequests();
    },
    methods: {
        async getAllAdRequests() {
            try {
                const response = await axios.get('/admin/all_adrequests');
                this.all_adrequests = response.data.all_adrequests;
            } catch (error) {
                console.error('Error fetching all adrequests:', error.response ? error.response.data : error.message);
            }
        },  
    }
}
</script>

<style scoped>
.all-adrequests {
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
</style>
