<template>
    <div>
        <div class="new-adrequests">
            <div>
                <h1>New Ad Requests</h1>
                <p>These are the new ad requests recieved for various influencers.</p>
            </div>
        </div>
        <div v-if="new_adrequests.length === 0">
            <p id="no-results">No new ad requests to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Influencer Name</th>
                            <th>Request</th>
                            <th>Payment Amount</th>
                            <th>Influencer Details</th>
                            <th>Request Details</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(adrequest, index) in new_adrequests" :key="adrequest.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ adrequest.influencer.name }}</td>
                            <td>{{ adrequest.title }}</td>
                            <td>{{ adrequest.payment }}</td>
                            <td><router-link :to="{ name: 'SponsorViewInfluencerDetails', params: { id: adrequest.influencer.id } }"><button class="btn btn-warning">View</button></router-link></td>
                            <td><router-link :to="{ name: 'SponsorViewAdrequestDetails', params: { id: adrequest.id } }"><button class="btn btn-warning">View</button></router-link></td>
                            <td id="accept-reject">
                                <button @click="acceptAdrequest(adrequest.id)" class="btn btn-success me-5">Accept</button>
                                <button @click="rejectAdrequest(adrequest.id)" class="btn btn-danger">Reject</button>
                            </td>
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
    name: 'SponsorNewRequests',
    data() {
        return {
            new_adrequests: {},
        };
    },
    created() {
        this.getNewAdRequests();
    },
    methods: {
        async getNewAdRequests() {
            try {
                const response = await axios.get('/sponsor/new_adrequests');
                this.new_adrequests = response.data.new_adrequests;
            } catch (error) {
                console.error("Error Fetching New Ad Requests : ", error);
            }
        },
        async acceptAdrequest(adrequest_id) {
            try {
                const response = await axios.put(`/api/adrequest/${adrequest_id}`, {
                    id: adrequest_id,
                    campaign_id: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).campaign_id,
                    influencer_id: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).influencer_id,
                    title: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).title,
                    message: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).message,
                    requirements: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).requirements,
                    payment: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).payment,
                    status: 'Accepted',
                    owner: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).owner,
                    work_status: '0%',
                });
                if (response.status === 200) {
                    this.new_adrequests = this.new_adrequests.filter(adrequest => adrequest.id !== adrequest_id);
                    alert('Ad request accepted successfully');
                    console.log('Ad request accepted successfully');
                }
            } catch (error) {
                console.error('Error accepting ad request:', error.response ? error.response.data : error.message);
                alert('Error accepting ad request');
            }
        },
        async rejectAdrequest(adrequest_id) {
            try {
                const response = await axios.put(`/api/adrequest/${adrequest_id}`, {
                    id: adrequest_id,
                    campaign_id: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).campaign_id,
                    influencer_id: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).influencer_id,
                    title: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).title,
                    message: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).message,
                    requirements: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).requirements,
                    payment: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).payment,
                    status: 'Rejected',
                    owner: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).owner,
                    work_status: this.new_adrequests.find(adrequest => adrequest.id === adrequest_id).work_status,
                });
                if (response.status === 200) {
                    this.new_adrequests = this.new_adrequests.filter(adrequest => adrequest.id !== adrequest_id);
                    alert('Ad request rejected successfully');
                    console.log('Ad request rejected successfully');
                }
            } catch (error) {
                console.error('Error rejecting ad request:', error.response ? error.response.data : error.message);
                alert('Error rejecting ad request');
            }
        }
    }
}
</script>

<style scoped>
.new-adrequests {
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
