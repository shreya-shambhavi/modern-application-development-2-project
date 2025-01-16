<template>
    <div class="body">

        <div class="d-flex justify-content-end">
                <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="update-campaign">

            <div class="card" id="form">
                <h1>Update Campaign Details</h1><br>

                <div class = "form-group mb-3">
                    <label for = "campaign_name" class = "mb-2">Campaign Name</label>
                    <input v-model = "campaign.name" type = "text" class = "form-control" required>
                </div>

                <div class = "form-group mb-3">
                    <label for = "sponsor_name" class = "mb-2">Sponsor Name</label>
                    <input v-model = "sponsor.name" type = "text" class = "form-control" readonly>
                </div>

                <div class = "form-group mb-3">
                    <label for = "start_date" class = "mb-2">Start Date</label>
                    <input v-model = "campaign.start_date" type = "date" class = "form-control" required>
                </div>

                <div class = "form-group mb-3">
                    <label for = "end_date" class = "mb-2">End Date</label>
                    <input v-model = "campaign.end_date" type = "date" class = "form-control" required>
                </div>

                <div class = "form-group mb-3">
                    <label for = "budget" class = "mb-2">Budget</label>
                    <input v-model = "campaign.budget" type = "number" class = "form-control" required>
                </div>

                <div class = "form-group mb-3">
                    <label for = "visibility" class = "mb-2">Visibility</label>
                    <select v-model = "campaign.visibility" class = "form-select" required>
                        <option value = "Public">Public</option>
                        <option value = "Private">Private</option>
                    </select>
                </div>

                <div class="form-group mb-3">
                    <label for="target_audience" class="mb-2">Target Audience</label>
                    <select v-model="campaign.target_audience" class="form-select" required>>
                        <option value="Tech Enthusiasts">Tech Enthusiasts</option>
                        <option value="Health-Conscious Individuals">Health-Conscious Individuals</option>
                        <option value="Travel Enthusiasts">Travel Enthusiasts</option>
                        <option value="Fashion Lovers">Fashion Lovers</option>
                        <option value="Foodies">Foodies</option>
                        <option value="Gamers">Gamers</option>
                        <option value="Beauty Enthusiasts">Beauty Enthusiasts</option>
                        <option value="Photography Enthusiasts">Photography Enthusiasts</option>
                        <option value="Lifestyle Influencers">Lifestyle Influencers</option>
                        <option value="Music Lovers">Music Lovers</option>
                    </select>
                </div>

                <div class = "form-group mb-3">
                    <label for = "description" class = "mb-2">Description</label>    
                    <div class="form-floating">
                        <textarea v-model="campaign.description" class = "form-control" id = "description" style="height: 100px" required></textarea>
                    </div>
                </div>

                <div class="buttons">
                    <div id="update-button">
                        <button class="btn btn-primary" @click="updateCampaign">Update Details</button>
                    </div>
                    <div id="delete-button">
                        <button class="btn btn-danger" @click="deleteCampaign">Delete Campaign</button>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name : 'UpdateCampaign',
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            campaign: {},
            sponsor: {},
        }
    },
    created() {
        this.getSponsor();
        this.getCampaign();
    },
    methods: {
        async getSponsor() {
            try {
                const response = await axios.get('/sponsor/profile');
                this.sponsor = response.data.sponsor;
            } catch (error) {
                console.error("Error Fetching Sponsor : " , error);
            }
        },
        async getCampaign() {
            try {
                const response = await axios.get(`/api/campaign/${this.id}`);
                this.campaign = response.data;
            } catch (error) {
                console.error("Error Fetching Campaign : " , error);
            }
        },
        async updateCampaign() {
            if (!this.sponsor.id) {
                console.error("Sponsor ID is missing");
                return;
            }
            try {
                const response = await axios.put(`/api/campaign/${this.id}`, this.campaign);
                console.log("Campaign Updated Successfully");
                alert("Campaign Updated Successfully");
                this.$router.push('/sponsor/dashboard/mycampaigns');
            } catch (error) {
                console.error("Error Updating Campaign : ", error);
            }
        },
        async deleteCampaign() {
            const confirmed = confirm("Are you sure you want to delete this campaign?");
            if (confirmed) {
                try {
                    const response = await axios.delete(`/api/campaign/${this.id}`);
                    console.log("Campaign Deleted : ", response.data.message);
                    alert("Campaign Deleted Successfully");
                    this.$router.push('/sponsor/dashboard/mycampaigns');
                } catch (error) {
                    console.error("Error Deleting Campaign : ", error);
                }
            }
        },
        goBack() {
            this.$router.go(-1);
        },
    },
}
</script>

<style scoped>
.body {
    background-color: #D9D9D9;
    padding-bottom: 100px;
}
.update-campaign {
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
    height: auto;
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
#close-button {
    margin: 10px;
    padding: 10px;
    background-color: #E76F51;
    color: white;
    border: none;
    border-radius: 50%;
}
.buttons {
display: flex;
justify-content: space-between;
margin-top: 25px;
margin-bottom: 50px;
}
</style>
