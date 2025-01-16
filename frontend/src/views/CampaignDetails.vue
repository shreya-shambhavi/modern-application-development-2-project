<template>

    <div class="d-flex justify-content-end">
        <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
    </div>

    <div class="campaign-details" v-if="campaign && Object.keys(campaign).length > 0">
        <div>
            <h1 id="title">{{ campaign.name }}</h1>
            <h5 id="sub-head">{{ campaign.visibility }} Campaign</h5>
            <br>
            <p>Campaign ID : <span>{{ campaign.id }}</span></p>
            <p>Sponsor Name : <span>{{ campaign.sponsor.name }}</span></p>
            <p>Start Date : <span>{{ campaign.start_date }}</span></p>
            <p>End Date : <span>{{ campaign.end_date }}</span></p>
            <p>Budget : <span>{{ campaign.budget }}</span></p>
            <p>Target Audience : <span>{{ campaign.target_audience }}</span></p>
            <p>Status : <span>{{ campaign.status }}</span></p>
            <p>Flag Status : <span>{{ campaign.flag_status }}</span></p>
            <br>
            <p>{{ campaign.description }}</p>
        </div>
    </div>

    <div id="adrequest-details">
        <div>
            <h3 id="relation-head">Ad Requests of the Campaign</h3>
            <br>
            <div v-if="campaign.adrequests && campaign.adrequests.length > 0">
                <div class="table-container">
                    <table class="table table-bordered table hover">
                        <thead class="table-warning">
                            <tr>
                                <th>S No.</th>
                                <th>Owner</th>
                                <th>Request</th>
                                <th>Payment</th>
                                <th>Status</th>
                                <th>Details</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(adrequest, index) in campaign.adrequests" :key="adrequest.id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ adrequest.owner }}</td>
                                <td>{{ adrequest.title }}</td>
                                <td>{{ adrequest.payment }}</td>
                                <td>{{ adrequest.status }}</td>
                                <td><router-link :to="{ name: dynamicRouteName, params: { id: adrequest.id } }"><button type="button" class="btn btn-primary">View</button></router-link></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div v-else>
                <p>No ad requests to show.</p>
            </div>

        </div>
    </div>
</template>

<script>

import axios from '../assets/axios.js';
import { mapGetters } from 'vuex';

export default {
    name: 'CampaignDetails',
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            campaign: {},
        }
    },
    computed: {
        ...mapGetters(['userRole']),
        dynamicRouteName() {
            switch (this.userRole) {
                case 'Admin':
                    return 'AdminViewAdrequestDetails';
                case 'Sponsor':
                    return 'SponsorViewAdrequestDetails';
                case 'Influencer':
                    return 'InfluencerViewAdrequestDetails';
            }
        }
    },
    created() {
        this.getCampaign();
    },
    methods: {
        async getCampaign() {
            try {
                const response = await axios.get(`/api/campaign/${this.id}`);
                this.campaign = response.data;
            } catch (error) {
                console.error("Error Fetching Campaign : ", error);
            }
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>

<style scoped>
.campaign-details {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
    margin-bottom: 50px;
    padding-left: 50px;
    padding-right: 50px;
}
#title {
    font-size: 5em;
    text-align: center;
    font-weight: bold;
    color: #E76F51;
    font-style: oblique;
    padding: 10px;
}
#sub-head {
    font-size: 1.5em;
    text-align: center;
    font-style: oblique;
    color: #F4A261;
    padding: 10px;
}
#relation-head {
    font-size: 3em;
    text-align: center;
    font-weight: bold;
    color: #2A9D8F;
    font-style: oblique;
    padding: 10px;
}
p {
    font-size: 1.25em;
    font-style: oblique;
    text-align: center;
    padding-left: 25px;
    padding-right: 25px;
    color: #353535;
}
span {
    font-weight: bolder;
}
#close-button {
    margin: 10px;
    padding: 10px;
    background-color: #E76F51;
    color: white;
    border: none;
    border-radius: 50%;
}
.table-container {
    padding-left: 20px;
    padding-right: 20px;
    width: 100%;
    text-align: center;
    vertical-align: middle;
}
table {
    width: 100%;
}
th {
    vertical-align: middle;
}
td {
    vertical-align: middle;
}
</style>
