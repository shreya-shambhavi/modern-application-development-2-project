<template>

    <div class="body">

        <div class="d-flex justify-content-end">
                <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="create-adrequest">

            <div class="card" id="form">
                <h1>Create An Ad Request</h1><br>

                <div class = "form-group mb-3">
                    <label for = "campaign_name" class = "mb-2">Campaign Name</label>
                    <input v-model = "campaign.name" type = "text" class = "form-control" readonly>
                </div>

                <div class = "form-group mb-3">
                    <label for = "influencer_name" class = "mb-2">Influencer Name</label>
                    <input v-model = "influencer.name" type = "text" class = "form-control" readonly>
                </div>

                <div class = "form-group mb-3">
                    <label for = "adrequest_title" class = "mb-2">Title</label>
                    <input v-model = "title" type = "text" class = "form-control" required>
                </div>

                <div class = "form-group mb-3">
                    <label for = "adrequest_message" class = "mb-2">Message</label>    
                    <div class="form-floating">
                        <textarea v-model="message" class = "form-control" id = "adrequest_message" style="height: 100px" required></textarea>
                    </div>
                </div>

                <div class = "form-group mb-3">
                    <label for = "adrequest_requirements" class = "mb-2">Requirements</label>    
                    <div class="form-floating">
                        <textarea v-model="requirements" class = "form-control" id = "adrequest_requirements" style="height: 100px" required></textarea>
                    </div>
                </div>

                <div class = "form-group mb-3">
                    <label for = "adrequest_payment" class = "mb-2">Payment</label>
                    <input v-model = "payment" type = "number" class = "form-control" required>
                </div>

                <div class="button">
                    <button id="sent-button" class="btn btn-primary" @click="CreateAdrequest">Send Request</button>
                </div>

            </div>
        </div>
    </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name : 'InfluencerCreateAdrequest',
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            campaign: {},
            influencer: {},
            adrequest: {},
        }
    },
    created() {
        this.getCampaign();
        this.getInfluencer();
    },
    methods: {

        async getCampaign() {
            const campaign_id = this.$route.params.id;
            if (!campaign_id) {
                console.error("Campaign ID is not available");
                return;
            }
            try {
                const response = await axios.get(`/api/campaign/${campaign_id}`);
                this.campaign = response.data;
            } catch (error) {
                console.error("Error Fetching Campaign: ", error);
            }
        },
        async getInfluencer() {
            try {
                const response = await axios.get('/influencer/profile');
                this.influencer = response.data.influencer;
            } catch (error) {
                console.error("Error Fetching Influencer : ", error);
            }
        },
        async CreateAdrequest() {
            if (!this.campaign.id || !this.influencer.id) {
                console.error("Campaign ID or Influencer ID is missing");
                return;
            }
            try {
                const response = await axios.post(`/api/adrequest`, {
                    campaign_id: this.campaign.id,
                    influencer_id: this.influencer.id,
                    title: this.title,
                    message: this.message,
                    requirements: this.requirements,
                    payment: this.payment,
                    owner: this.$store.state.role
                });
                console.log("Ad Request Created Successfully");
                alert("Ad Request Created Successfully");
                this.$router.push('/influencer/dashboard/requests/sent');
            } catch (error) {
                console.error("Error Creating Ad Request: ", error);
            }
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>

<style scoped>
.body {
    background-color: #D9D9D9;
    padding-bottom: 100px;
}
.create-adrequest {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
    margin-bottom: 30px;
    padding-left: 20px;
    padding-right: 20px;
    background-color: #D9D9D9;
}
#form {
    width: 80%;
}
.card {
    width: 1000px;
    height: 1000px;
    padding: 50px;
}
h1 {
    font-size: 3.5em;
    text-align: center;
    font-weight: bold;
    color: #E76F51;
    font-style: oblique;
    padding: 10px;
    margin: 30px;
}
h4 {
    font-size: 1.5em;
    text-align: center;
    font-style: oblique;
    color: #F4A261;
    padding: 10px;
}
.button {
    display: flex;
    justify-content: center;
    margin-top: 30px;
    margin-bottom: 50px;
}
#sent-button {
    color: white;
    border-radius: 50px;
    padding: 10px 20px;
}
#close-button {
    margin: 10px;
    padding: 10px;
    background-color: #E76F51;
    color: white;
    border: none;
    border-radius: 50%;
}
</style>
