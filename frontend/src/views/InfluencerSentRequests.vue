<template>
    <div>
        <div class="sent-adrequests">
            <div>
                <h1>Status of Ad Requests Sent</h1>
                <p>Here you can see the status of the ad requests you have sent to the campaigns.</p>
            </div>
        </div>
        <div v-if="sent_adrequests.length === 0">
            <p id="no-results">No ad requests sent.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Campaign Name</th>
                            <th>Request</th>
                            <th>Payment Amount</th>
                            <th>Details</th>
                            <th>Action</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(adrequest, index) in sent_adrequests" :key="adrequest.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ adrequest.campaign.name }}</td>
                            <td>{{ adrequest.title }}</td>
                            <td>{{ adrequest.payment }}</td>
                            <td><router-link :to="{  name: 'InfluencerViewAdrequestDetails', params: { id: adrequest.id } }"><button class="btn btn-warning">View</button></router-link></td>
                            <td v-if=" adrequest.status == 'Pending' "><button @click="goToUpdateAdrequest(adrequest.id)" id="update-button" type="button" class="btn btn-primary">Update</button></td>
                            <td v-else><button @click="goToUpdateAdrequest(adrequest.id)" id="update-button" type="button" class="btn btn-primary" disabled>Update</button></td>
                            <td v-if=" adrequest.status == 'Pending' "><span id="badge1">Pending</span></td>
                            <td v-else-if=" adrequest.status == 'Accepted' "><span id="badge2">Accepted</span></td>
                            <td v-if=" adrequest.status == 'Rejected' "><span id="badge3">Rejected</span></td>
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
    name: 'InfluencerSentRequests',
    data() {
        return {
            sent_adrequests: {},
        };
    },
    created() {
        this.getSentAdRequests();
    },
    methods: {
        async getSentAdRequests() {
            try {
                const response = await axios.get('/influencer/sent_adrequests');
                this.sent_adrequests = response.data.sent_adrequests;
            } catch (error) {
                console.error("Error Fetching Sent Ad Requests : ", error);
            }
        },
        goToUpdateAdrequest(adrequest_id) {
            this.$router.push({ name: 'InfluencerUpdateAdrequest', params: { id: adrequest_id } });
        }
    }
}
</script>

<style scoped>
.sent-adrequests {
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
th, td {
    vertical-align: middle;
}
#badge1 {
    background-color: grey;
    color: white;
    padding: 10px;
    border-radius: 10px;
    font-weight: bold;
}
#badge2 {
    background-color: lightgreen;
    color: black;
    padding: 10px;
    border-radius: 10px;
    font-weight: bold;
}
#badge3 {
    background-color: lightcoral;
    color: white;
    padding: 10px;
    border-radius: 10px;
    font-weight: bold;
}
</style>
