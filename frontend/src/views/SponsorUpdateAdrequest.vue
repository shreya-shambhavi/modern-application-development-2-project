<template>
    <div class="body" v-if="adrequest">

        <div class="d-flex justify-content-end">
                <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="update-adrequest">
            <div class="card" id=" form">

                <h1>Update An Ad Request</h1><br>

                    <div class = "form-group mb-3">
                        <label for = "campaign_name" class = "mb-2">Campaign Name</label>
                        <input v-model = "adrequest.campaign.name" type = "text" class = "form-control" readonly>
                    </div>

                    <div class = "form-group mb-3">
                        <label for = "imfluencer_name" class = "mb-2">Influencer Name</label>
                        <input v-model = "adrequest.influencer.name" type = "text" class = "form-control" readonly>
                    </div>

                    <div class = "form-group mb-3">
                        <label for = "adrequest_title" class = "mb-2">Title</label>
                        <input v-model = "adrequest.title" type = "text" class = "form-control" required>
                    </div>

                    <div class = "form-group mb-3">
                        <label for = "adrequest_message" class = "mb-2">Message</label>    
                        <div class="form-floating">
                            <textarea v-model="adrequest.message" class = "form-control" id = "adrequest_message" style="height: 100px" required></textarea>
                        </div>
                    </div>

                    <div class = "form-group mb-3">
                        <label for = "adrequest_requirements" class = "mb-2">Requirements</label>    
                        <div class="form-floating">
                            <textarea v-model="adrequest.requirements" class = "form-control" id = "adrequest_requirements" style="height: 100px" required></textarea>
                        </div>
                    </div>

                    <div class = "form-group mb-3">
                        <label for = "adrequest_payment" class = "mb-2">Payment</label>
                        <input v-model = "adrequest.payment" type = "number" class = "form-control" required>
                    </div>
                    
                    <div class="buttons">
                        <div id="update-button">
                            <button class="btn btn-primary" @click="updateAdrequest">Update Details</button>
                        </div>
                        <div id="delete-button">
                            <button class="btn btn-danger" @click="deleteAdrequest">Delete Ad Request</button>
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
            required: true,
        }
    },
    data() {
        return {
            adrequest: null,
        };
    },
    created() {
        this.getAdrequest();
    },
    methods: {
        async getAdrequest() {
            try {
                const response = await axios.get(`/api/adrequest/${this.id}`);
                this.adrequest = response.data;
            } catch (error) {
                console.error("Error Fetching Ad Request : ", error);
            }
        },
        async updateAdrequest() {
            try {
                const response = await axios.put(`/api/adrequest/${this.id}`, this.adrequest);
                console.log(response.data);
                alert("Ad Request Updated Successfully");
                this.$router.push({ name: 'SponsorSentRequests' });
            } catch (error) {
                console.error("Error Updating Ad Request : ", error);
                alert("Error Updating Ad Request");
            }
        },
        async deleteAdrequest() {
            const confirmDelete = confirm("Are you sure you want to delete this Ad Request?");
            if (confirmDelete) {
                try {
                    const response = await axios.delete(`/api/adrequest/${this.id}`);
                    console.log(response.data);
                    alert("Ad Request Deleted Successfully");
                    this.$router.push({ name: 'SponsorSentRequests' });
                } catch (error) {
                    console.error("Error Deleting Ad Request : ", error);
                    alert("Error Deleting Ad Request");
                }
            }
        },
        goBack() {
            this.$router.go(-1);
        },
    }
}
</script>

<style scoped>
.body {
    background-color: #D9D9D9;
    padding-bottom: 100px;
}
.update-adrequest {
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
margin-top: 30px;
margin-bottom: 50px;
}
</style>
