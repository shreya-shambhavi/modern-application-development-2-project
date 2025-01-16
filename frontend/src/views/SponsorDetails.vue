<template>
    <div>
        <div class="d-flex justify-content-end">
            <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="sponsor-details" v-if="sponsor && Object.keys(sponsor).length > 0">
            <div>
                <h1 id="title">{{ sponsor.name }}</h1>
                <h5 id="sub-head">Sponsor</h5>
                <br>
                <p>User ID : <span>{{ sponsor.user_id }}</span></p>
                <p>Sponsor ID : <span>{{ sponsor.id }}</span></p>
                <p>Email Address : <span>{{ sponsor.email }}</span></p>
                <p>Industry : <span>{{ sponsor.industry }}</span></p>
                <p>Valuation : <span>{{ sponsor.valuation }}</span></p>
                <p>Flag Status : <span>{{ sponsor.flag_status }}</span></p>
                <br>
                <p>{{ sponsor.description }}</p>
            </div>
        </div>

        <div id="campaign-details">
            <div>
                <h3 id="relation-head">Campigns of the Sponsor</h3>
                <br>
                <div v-if="sponsor.campaigns && sponsor.campaigns.length > 0">
                    <div class="table-container">
                        <table class="table table-bordered table hover">
                            <thead class="table-warning">
                                <tr>
                                    <th>S No.</th>
                                    <th>Name</th>
                                    <th>Start Date</th>
                                    <th>End Date</th>
                                    <th>Visibility</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(campaign, index) in sponsor.campaigns" :key="campaign.id">
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ campaign.name }}</td>
                                    <td>{{ campaign.start_date }}</td>
                                    <td>{{ campaign.end_date }}</td>
                                    <td>{{ campaign.visibility }}</td>
                                    <td><router-link :to="{ name: dynamicRouteName, params: { id: campaign.id } }"><button type="button" class="btn btn-primary">View</button></router-link></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div v-else>
                    <p>No campaigns to show.</p>
                </div>

            </div>        
        </div>
        
    </div>
</template>

<script>

import axios from '../assets/axios.js';
import { mapGetters } from 'vuex';

export default {
    name: 'SponsorDetails',
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            sponsor: {},
        }
    },
    computed: {
        ...mapGetters(['userRole']),
        dynamicRouteName() {
            switch (this.userRole) {
                case 'Admin':
                    return 'AdminViewCampaignDetails';
                case 'Sponsor':
                    return 'SponsorViewCampaignDetails';
                case 'Influencer':
                    return 'InfluencerViewCampaignDetails';
            }
        }
    },
    created() {
        this.getSponsor();
    },
    methods: {
        async getSponsor() {
            try {
                const response = await axios.get(`/api/sponsor/${this.id}`);
                this.sponsor = response.data;
            } catch (error) {
                console.error("Error Fetching Sponsor : ", error);
            }
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>

<style scoped>
.sponsor-details {
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
