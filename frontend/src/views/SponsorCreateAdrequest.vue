<template>
    <div class="body">

        <div class="d-flex justify-content-end">
                <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="create-adrequest">
            <div class="card" id=" form">

                <h1>Create An Ad Request</h1><br>

                <div v-if="type === 'campaign'">
                    <h3>Campaign: {{ campaign.name }}</h3><br>

                    <div class = "form-group mb-3">
                        <label for = "campaign_name" class = "mb-2">Campaign Name</label>
                        <input v-model = "campaign.name" type = "text" class = "form-control" readonly>
                    </div>

                    <div class = "form-group mb-3">
                        <label for = "influencer_name" class = "mb-2">Influencer Name</label>
                        <select v-model = "influencer.id" class = "form-select" required>
                            <option v-for="influencer in all_influencers" :key="influencer.id" :value="influencer.id">{{ influencer.name }}</option>
                        </select>
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
                    
                    <div v-if=" campaign.flag_status === 'Unflagged' " class="button">
                        <button id="create-button" class="btn btn-primary" @click="CreateAdrequest">Send Request</button>
                    </div>
                    <div v-else class="button">
                        <button id="create-button" class="btn btn-primary" disabled>Send Request</button>
                    </div>

                </div>

                <div v-if="type === 'influencer'">
                    <h3>Influencer: {{ influencer.name }}</h3><br>

                    <div class = "form-group mb-3">
                        <label for = "campaign_name" class = "mb-2">Campaign Name</label>
                        <select v-model = "campaign.id" class = "form-select" required>
                            <option v-for="campaign in my_campaigns" :key="campaign.id" :value="campaign.id">{{ campaign.name }}</option>
                        </select>
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
                        <button id="create-button" class="btn btn-primary" @click="CreateAdrequest">Send Request</button>
                    </div>

                </div>

            </div>
        </div>

    </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: "SponsorCreateAdrequest",
    props: {
        id: {
            type: Number,
            required: true
        },
        type: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            campaign: {},
            influencer: {},
            title: "",
            message: "",
            requirements: "",
            payment: 0,
            all_influencers: {},
            my_campaigns: {}
        };
    },
    created() {
        this.getAllInfluencers();
        this.getMyCampaigns();
        this.getCampaign();
        this.getInfluencer();
    },
    methods: {
        async getAllInfluencers() {
            try {
                const response = await axios.get("/sponsor/all_influencers");
                this.all_influencers = response.data.all_influencers;
            } catch (error) {
                console.error("Error fetching influencers", error);
            }
        },
        async getMyCampaigns() {
            try {
                const response = await axios.get("/sponsor/all_campaigns");
                this.my_campaigns = response.data.my_campaigns;
            } catch (error) {
                console.error("Error fetching campaigns", error);
            }
        },
        async CreateAdrequest() {
            if (this.type === "campaign") {
                if (!this.campaign.id) {
                    console.error("Campaign ID is missing");
                    return;
                }
                if (!this.influencer.id) {
                    console.error("Influencer ID is missing");
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
                        owner: "Sponsor"
                    });

                    console.log("Ad request created successfully", response);
                    alert("Ad request created successfully");
                    this.$router.push({ name: "SponsorSentRequests" });
                } catch (error) {
                    console.error("Error creating ad request", error);
                }

            } else if (this.type === "influencer") {
                if (!this.campaign.id) {
                    console.error("Campaign ID is missing");
                    return;
                }
                try {
                    const response = await axios.post(`/api/adrequest`, {
                        campaign_id: this.campaign.id,
                        influencer_id: this.id,
                        title: this.title,
                        message: this.message,
                        requirements: this.requirements,
                        payment: this.payment,
                        owner: "Sponsor"
                    });

                    console.log("Ad request created successfully", response);
                    alert("Ad request created successfully");
                    this.$router.push({ name: "SponsorSentRequests" });

                } catch (error) {
                    console.error("Error creating ad request", error);
                }
            }
        },
        goBack() {
            this.$router.go(-1);
        },
        async getCampaign() {

            if (this.type === "campaign") {
                const campaign_id = this.$route.params.id;
                if (!campaign_id) {
                    console.error("Campaign ID is not available");
                    return;
                }
                try {
                    const response = await axios.get(`/api/campaign/${campaign_id}`);
                    this.campaign = response.data;
                } catch (error) {
                    console.error("Error fetching campaign", error);
                }
            }
        },
        async getInfluencer() {
            if (this.type === "influencer") {
                const influencer_id = this.$route.params.id;
                if (!influencer_id) {
                    console.error("Influencer ID is not available");
                    return;
                }
                try {
                    const response = await axios.get(`/api/influencer/${influencer_id}`);
                    this.influencer = response.data;
                } catch (error) {
                    console.error("Error fetching influencer", error);
                }
            }
        },
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
    height: 1100px;
    padding: 50px;
}
h1 {
    font-size: 3.5em;
    text-align: center;
    font-weight: bold;
    color: #E76F51;
    font-style: oblique;
    padding: 10px;
    margin: 10px;
}
h3 {
    font-size: 2.5em;
    text-align: center;
    font-style: oblique;
    font-weight: bold;
    color: crimson;
    padding: 10px;
    margin: 10px;
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
