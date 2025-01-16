<template>
    <div>
        <div class="requests-directory">
            <div>
                <h1>Ad Requests Directory</h1>
                <p>View all your accepted and rejected ad requests here.</p>
            </div>
        </div>
        <div v-if="adrequests.length === 0">
            <p id="no-results">No ad requests to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Delivery</th>
                            <th>Status</th>
                            <th>Campaign Name</th>
                            <th>Request</th>
                            <th>Payment Amount</th>
                            <th>Work Status</th>
                            <th>Campaign Details</th>
                            <th>Request Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(adrequest, index) in adrequests" :key="adrequest.id">
                            <td>{{ index + 1 }}</td>
                            <td id="recieved" v-if=" adrequest.owner === 'Sponsor' ">Recieved</td>
                            <td id="sent" v-else>Sent</td>
                            <td id="accepted" v-if=" adrequest.status === 'Accepted' ">{{ adrequest.status }}</td>
                            <td id="rejected" v-if=" adrequest.status === 'Rejected' ">{{ adrequest.status }}</td>
                            <td>{{ adrequest.campaign.name }}</td>
                            <td>{{ adrequest.title }}</td>
                            <td>{{ adrequest.payment }}</td>
                            <td>{{ adrequest.work_status }}</td>
                            <td><router-link :to="{ name: 'InfluencerViewCampaignDetails', params: { id: adrequest.campaign.id } }"><button class="btn btn-warning">View</button></router-link></td>
                            <td><router-link :to="{ name: 'InfluencerViewAdrequestDetails', params: { id: adrequest.id } }"><button class="btn btn-warning">View</button></router-link></td>
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
    name: 'InfluencerRequestsDirectory',
    data() {
        return {
            adrequests: {},
        };
    },
    created() {
        this.getAdRequests();
    },
    methods: {
        async getAdRequests() {
            try {
                const response = await axios.get('/influencer/adrequests_directory');
                this.adrequests = response.data.adrequests;
            } catch (error) {
                console.error("Error Fetching Ad Requests : ", error);
            }
        },
    }
}
</script>

<style scoped>
.requests-directory {
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
#recieved {
    color: orange;
    font-weight: bold;
}
#sent {
    color: blue;
    font-weight: bold;
}
#accepted {
    color: green;
    font-weight: bold;
}
#rejected {
    color: red;
    font-weight: bold;
}
</style>
