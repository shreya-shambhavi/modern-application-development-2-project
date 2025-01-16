<template>
    <div>

        <div class="all-campaigns">
            <div>
                <h1>Campaigns On Platform</h1>
                <p>These are all the campaigns on the platform.</p>
            </div>
        </div>
        <div v-if="all_campaigns.length === 0">
            <p id="no-results">No campaigns to show.</p>
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
                        <tr v-for="(campaign, index) in all_campaigns" :key="campaign.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ campaign.name }}</td>
                            <td>{{ campaign.sponsor.name }}</td>
                            <td>{{ campaign.start_date }}</td>
                            <td>{{ campaign.end_date }}</td>
                            <td>{{ campaign.visibility }}</td>
                            <td><router-link :to="{ name: 'AdminViewCampaignDetails', params: { id: campaign.id } }"><button type="button" class="btn btn-warning">View</button></router-link></td>
                            <td v-if="campaign.flag_status === 'Unflagged'"><button @click="flagCampaign(campaign.id)" class="btn btn-danger">Flag</button></td>
                            <td v-else><button @click="unflagCampaign(campaign.id)" class="btn btn-success">Unflag</button></td>
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
    name: 'AllCampaigns',
    data() {
        return {
            all_campaigns: {},
        };
    },
    created() {
        this.getAllCampaigns();
    },
    methods: {
        async getAllCampaigns() {
            try {
                const response = await axios.get('/admin/all_campaigns');
                this.all_campaigns = response.data.all_campaigns;
            } catch (error) {
                console.error('Error fetching all campaigns:', error.response ? error.response.data : error.message);
            }
        },
        async flagCampaign(id) {
            try {
                const response = await axios.put(`/api/campaign/${id}`, { flag_status: "Flagged" });
                if (response.status === 200) {
                    alert('Campaign flagged successfully');
                    this.getAllCampaigns();
                }
            } catch (error) {
                console.error('Error flagging campaign:', error.response ? error.response.data : error.message);
                alert('Error flagging campaign');
            }
        } ,
        async unflagCampaign(id) {
            try {
                const response = await axios.put(`/api/campaign/${id}`, { flag_status: "Unflagged" });
                if (response.status === 200) {
                    alert('Campaign unflagged successfully');
                    this.getAllCampaigns();
                }
            } catch (error) {
                console.error('Error unflagging campaign:', error.response ? error.response.data : error.message);
                alert('Error unflagging campaign');
            }
        }   
    }
}
</script>

<style scoped>
.all-campaigns {
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
