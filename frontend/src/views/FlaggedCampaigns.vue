<template>
    <div>

        <div class="flagged-campaigns">
            <div>
                <h1>Flagged Campaigns On Platform</h1>
                <p>These are all the flagged campaigns on the platform.</p>
            </div>
        </div>
        <div v-if="flagged_campaigns.length === 0">
            <p id="no-results">No flagged campaigns to show.</p>
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
                            <th>Visibility</th>
                            <th>Details</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(campaign, index) in flagged_campaigns" :key="campaign.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ campaign.name }}</td>
                            <td>{{ campaign.sponsor.name }}</td>
                            <td>{{ campaign.start_date }}</td>
                            <td>{{ campaign.end_date }}</td>
                            <td>{{ campaign.visibility }}</td>
                            <td><router-link :to="{ name: 'AdminViewCampaignDetails', params: { id: campaign.id } }"><button type="button" class="btn btn-warning">View</button></router-link></td>
                            <td><button @click="removeCampaign(campaign.id)" class="btn btn-danger">Remove</button></td>
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
    name: 'FlaggedCampaigns',
    data() {
        return {
            flagged_campaigns: {},
        };
    },
    created() {
        this.getFlaggedCampaigns();
    },
    methods: {
        async getFlaggedCampaigns() {
            try {
                const response = await axios.get('/admin/flagged_campaigns');
                this.flagged_campaigns = response.data.flagged_campaigns;
            } catch (error) {
                console.error('Error fetching all flagged campaigns:', error.response ? error.response.data : error.message);
            }
        },
        async removeCampaign(id) {
            const confirmDelete = confirm('Are you sure you want to remove this campaign?');
            if (confirmDelete) {

                try {
                    const response = await axios.delete(`/api/campaign/${id}`);
                    if (response.status === 204) {
                        alert('Campaign removed successfully');
                        this.flagged_campaigns = this.flagged_campaigns.filter(campaign => campaign.id !== id);
                    }
                } catch (error) {
                    console.error('Error removing campaign:', error.response ? error.response.data : error.message);
                    alert('Error removing campaign');
                }
            }
        }    
    }
}
</script>

<style scoped>
.flagged-campaigns {
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
