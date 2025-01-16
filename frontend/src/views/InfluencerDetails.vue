<template>

    <div class="d-flex justify-content-end">
        <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
    </div>

    <div class="influencer-details" v-if="influencer && Object.keys(influencer).length > 0">
        <div>
            <h1 id="title">{{ influencer.name }}</h1>
            <h5 id="sub-head">Influencer</h5>
            <br>
            <p>User ID : <span>{{ influencer.user_id }}</span></p>
            <p>Influencer ID : <span>{{ influencer.id }}</span></p>
            <p>Email Address : <span>{{ influencer.email }}</span></p>
            <p>Category : <span>{{ influencer.category }}</span></p>
            <p>Reach : <span>{{ influencer.reach }}</span></p>
            <p>Flag Status : <span>{{ influencer.flag_status }}</span></p>
            <br>
            <p>{{ influencer.description }}</p>
        </div>
    </div>

    <div id="adrequest-details">
        <div>
            <h3 id="relation-head">Ad Requests of the Influencer</h3>
            <br>
            <div v-if="influencer.adrequests && influencer.adrequests.length > 0">
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
                            <tr v-for="(adrequest, index) in influencer.adrequests" :key="adrequest.id">
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
    name: 'InfluencerDetails',
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            influencer: {},
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
        this.getInfluencer();
    },
    methods: {
        async getInfluencer() {
            try {
                const response = await axios.get(`/api/influencer/${this.id}`);
                this.influencer = response.data;
            } catch (error) {
                console.error("Error Fetching Influencer : ", error);
            }
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>

<style scoped>
.influencer-details {
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
