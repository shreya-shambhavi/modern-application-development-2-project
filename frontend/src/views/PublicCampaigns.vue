<template>
    <div>
        <div class="public-campaigns">
            <div>
                <h1>Active Public Campaigns On Platform</h1>
                <p>These are all the active public campaigns on the platform.</p>
            </div>
        </div>

        <div id="filter-button">
            <button @click="pushtoSearch" type="button" class="btn btn-outline-secondary">Apply Filters</button>
        </div>

        <div v-if="public_campaigns.length === 0">
            <p id="no-results">No public campaigns to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Campaign Name</th>
                            <th>Sponsor Name</th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th>Details</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(campaign, index) in public_campaigns" :key="campaign.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ campaign.name }}</td>
                            <td>{{ campaign.sponsor.name }}</td>
                            <td>{{ campaign.start_date }}</td>
                            <td>{{ campaign.end_date }}</td>
                            <td><router-link :to="{ name: 'InfluencerViewCampaignDetails', params: { id: campaign.id } }"><button class="btn btn-warning">View</button></router-link></td>
                            <td v-if=" influencer.flag_status === 'Unflagged' "><button @click="goToCreateAdrequestPage(campaign.id)" class="btn btn-success">Request</button></td>
                            <td v-else><button class="btn btn-success" disabled>Request</button></td>
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
    name: 'PublicCampaigns',
    data() {
        return {
            public_campaigns: {},
            influencer: {},
        };
    },
    created() {
        this.getPublicCampaigns();
        this.getInfluencer();
    },
    methods: {
        async getPublicCampaigns() {
            try {
                const response = await axios.get('/influencer/public_campaigns');
                this.public_campaigns = response.data.public_campaigns;
            } catch (error) {
                console.error("Error Fetching Public Campaigns : ", error);
            }
        },
        goToCreateAdrequestPage(campaign_id) {
            if (campaign_id) {
                this.$router.push({ name: 'InfluencerCreateAdrequest', params: { id: campaign_id } });
            } else {
                console.error("Campaign ID is not available");
            }
        },
        pushtoSearch() {
            this.$router.push({ name: 'InfluencerSearchCampaigns' });
        },
        async getInfluencer() {
            try {
                const response = await axios.get('/influencer/profile');
                this.influencer = response.data.influencer;
            } catch (error) {
                console.error("Error Fetching Influencer : ", error);
            }
        },
    }
}
</script>

<style scoped>
.public-campaigns {
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
    text-align: center;
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
