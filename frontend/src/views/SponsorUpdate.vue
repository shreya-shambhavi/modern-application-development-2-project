<template>

    <div class="d-flex justify-content-end">
        <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
    </div>

    <div class="profile-update">
        <div id="form">
            <h1>Update Profile Details</h1><br>

            <div class = "form-group mb-3">
                <label for = "name" class = "mb-2">Name</label>
                <input v-model = "sponsor.name" type = "text" class = "form-control" required>
            </div>

            <div class = "form-group mb-3">
                <label for = "email" class = "mb-2">Email ID</label>
                <input v-model = "sponsor.email" type = "email" class = "form-control" required>
            </div>

            <div id = "industry" class = " form-group mb-3">
                <label for = "industry" class = "mb-2">Industry</label>
                <select v-model = "sponsor.industry" class = "form-select" id = "industry" required>
                    <option value="Fashion">Fashion</option>
                    <option value="Beauty and Skincare">Beauty and Skincare</option>
                    <option value="Health and Fitness">Health and Fitness</option>
                    <option value="Travel">Travel</option>
                    <option value="Food and Beverage">Food and Beverage</option>
                    <option value="Technology">Technology</option>
                    <option value="Lifestyle">Lifestyle</option>
                    <option value="Automotive">Automotive</option>
                    <option value="Education">Education</option>
                    <option value="Finance">Finance</option>
                    <option value="Real Estate">Real Estate</option>
                    <option value="Investment">Investment</option>
                    <option value="Luxury Goods">Luxury Goods</option>
                    <option value="Sustainability and Environment">Sustainability and Environment</option>
                    <option value="Entertainment and Media">Entertainment and Media</option>
                    <option value="Others">Others</option>
                </select>
            </div>

            <div id = "valuation" class = "form-group mb-3">
                <label for = "valuation" class = "mb-2">Valuation</label>
                <select v-model = "sponsor.valuation" class = "form-select" id = "valuation" required>
                    <option value="Valuation lies between 1K - 10K">Valuation lies between 1K - 10K</option>
                    <option value="Valuation lies between 10K - 50K">Valuation lies between 10K - 50K</option>
                    <option value="Valuation lies between 50K - 100K">Valuation lies between 50K - 100K</option>
                    <option value="Valuation lies between 100K - 500K">Valuation lies between 100K - 500K</option>
                    <option value="Valuation lies between 500K - 1 Million">Valuation lies between 500K - 1 Million</option>
                    <option value="Valuation lies between 1 Million - 10 Million">Valuation lies between 1 Million - 10 Million</option>
                    <option value="Valuation lies between 10 Million - 50 Million">Valuation lies between 10 Million - 50 Million</option>
                    <option value="Valuation lies between 50 Million - 100 Million">Valuation lies between 50 Million - 100 Million</option>
                    <option value="Valuation lies between 100 Million - 500 Million">Valuation lies between 100 Million - 500 Million</option>
                    <option value="Valuation is more than 500 Million">Valuation is more than 500 Million</option>
                </select>
            </div>

            <div class = "form-group mb-3">
                <label for = "description" class = "mb-2">Description</label>    
                <div class="form-floating">
                    <textarea v-model="sponsor.description" class = "form-control" id = "description" style="height: 100px" required></textarea>
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
    name: "SponsorUpdate",
    props: {
        id: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            sponsor: {},
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
        async updateProfile() {
            try {
                const response = await axios.put(`/api/sponsor/${this.id}`, this.sponsor);
                console.log("Sponsor Profile Updated Successfully");
                alert("Sponsor Profile Updated Successfully");
                this.$router.push('/sponsor/dashboard/profile');
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
