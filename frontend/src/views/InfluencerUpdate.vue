<template>
        <div class="d-flex justify-content-end">
            <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="profile-update">
            <div id="form">
                <h1>Update Profile Details</h1><br>

                <div class = "form-group mb-3">
                    <label for = "name" class = "mb-2">Name</label>
                    <input v-model = "influencer.name" type = "text" class = "form-control" required>
                </div>

                <div class = "form-group mb-3">
                    <label for = "email" class = "mb-2">Email ID</label>
                    <input v-model = "influencer.email" type = "email" class = "form-control" required>
                </div>

                <div id = "category" class = "form-group mb-3">
                    <label for = "category" class = "mb-2">Category</label>
                    <select v-model = "influencer.category" class = "form-select" id = "category" required>
                        <option value="Fashion">Fashion</option>
                        <option value="Beauty and Skincare">Beauty and Skincare</option>
                        <option value="Health and Fitness">Health and Fitness</option>
                        <option value="Travel">Travel</option>
                        <option value="Food and Beverage">Food and Beverage</option>
                        <option value="Technology">Technology</option>
                        <option value="Lifestyle">Lifestyle</option>
                        <option value="Gaming">Gaming</option>
                        <option value="Education">Education</option>
                        <option value="Finance">Finance</option>
                        <option value="DIY and Crafts">DIY and Crafts</option>
                        <option value="Photography and Videography">Photography and Videography</option>
                        <option value="Motivation and Self-improvement">Motivation and Self-improvement</option>
                        <option value="Sustainability and Environment">Sustainability and Environment</option>
                        <option value="Entertainment">Entertainment</option>
                        <option value="Others">Others</option>
                    </select>
                </div>

                <div id = "reach" class = "form-group mb-3">
                    <label for = "reach" class = "mb-2">Reach</label>
                    <select v-model = "influencer.reach" class = "form-select" id = "reach" required>
                        <option value="Followers across various social media platforms lie between 1K - 10K">Followers across various social media platforms lie between 1K - 10K</option>
                        <option value="Followers across various social media platforms lie between 10K - 50K">Followers across various social media platforms lie between 10K - 50K</option>
                        <option value="Followers across various social media platforms lie between 50K - 100K">Followers across various social media platforms lie between 50K - 100K</option>
                        <option value="Followers across various social media platforms lie between 100K - 500K">Followers across various social media platforms lie between 100K - 500K</option>
                        <option value="Followers across various social media platforms lie between 500K - 1 Million">Followers across various social media platforms lie between 500K - 1 Million</option>
                        <option value="Followers across various social media platforms lie between 1 Million - 10 Million">Followers across various social media platforms lie between 1 Million - 10 Million</option>
                        <option value="Followers across various social media platforms lie between 10 Million - 50 Million">Followers across various social media platforms lie between 10 Million - 50 Million</option>
                        <option value="Followers across various social media platforms lie between 50 Million - 100 Million">Followers across various social media platforms lie between 50 Million - 100 Million</option>
                        <option value="Followers across various social media platforms lie between 100 Million - 500 Million">Followers across various social media platforms lie between 100 Million - 500 Million</option>
                        <option value="Followers across various social media platforms are more than 500 Million">Followers across various social media platforms are more than 500 Million</option>
                    </select>
                </div>

                <div class = "form-group mb-3">
                    <label for = "description" class = "mb-2">Description</label>    
                    <div class="form-floating">
                        <textarea v-model="influencer.description" class = "form-control" id = "description" style="height: 100px" required></textarea>
                    </div>
                </div>

                <div class="button">
                    <div id="update-button">
                        <button class="btn btn-primary" @click="updateProfile">Update Details</button>
                    </div>
                </div>

            </div>
        </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: "InfluencerUpdate",
    props: {
        id: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            influencer: {},
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
        async updateProfile() {
            try {
                const response = await axios.put(`/api/influencer/${this.id}`, this.influencer);
                console.log("Influencer Profile Updated Successfully");
                alert("Influencer Profile Updated Successfully");
                this.$router.push('/influencer/dashboard/profile');
            } catch (error) {
                console.error("Error Updating Profile : ", error);
            }
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>

<style scoped>
.profile-update {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
    margin-bottom: 30px;
    padding-left: 20px;
    padding-right: 20px;
}
#form {
    width: 70%;
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
    margin-top: 50px;
    margin-bottom: 50px;
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
