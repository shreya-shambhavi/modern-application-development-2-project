<template>

    <nav id="navbar" class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand" id="navbar-brand">Influencer Engagement and Sponsorship Coordination Platform</router-link>
            <div class="ms-auto d-flex">
                <router-link to="/user/login"><button id="loginbutton" type="button" class="btn">Login</button></router-link>
            </div>
        </div>
    </nav>

    <div class = "register">

        <div id="card" class = "card shadow p-5 border rounded-3">

            <h1 id="cardtitle" class = "card-title text-center mb-4"><b>USER REGISTRATION FORM</b></h1>

                <div class = "form-group mb-3">
                    <label for = "username" class = "mb-2">Username</label>
                    <input v-model = "username" type = "text" class = "form-control" required>
                </div>

                <div class = "form-group mb-3">
                    <label for = "password" class = "mb-2">Password</label>
                    <input v-model = "password" type = "password" class = "form-control" required/>
                </div> 

                <div class = "form-group mb-3">
                    <label for = "role" class = "mb-2">Role</label>
                    <select v-model = "role" class = "form-select" id = "role" required>
                        <option value = "Influencer">Influencer</option>
                        <option value = "Sponsor">Sponsor</option>
                    </select>
                </div>

                <div v-if="role === 'Influencer'">

                    <div class = "form-group mb-3">
                        <label for = "name" class = "mb-2">Name</label>
                        <input v-model = "name" type = "text" class = "form-control" required>
                    </div>

                    <div class = "form-group mb-3">
                        <label for = "email" class = "mb-2">Email ID</label>
                        <input v-model = "email" type = "email" class = "form-control" required>
                    </div>

                    <div id = "category" class = "form-group mb-3">
                        <label for = "category" class = "mb-2">Category</label>
                        <select v-model = "category" class = "form-select" id = "category" required>
                            <option selected>Select Category</option>
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
                        <select v-model = "reach" class = "form-select" id = "reach" required>
                            <option selected>Select Reach</option>
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
                            <textarea v-model="description" class = "form-control" id = "description" style="height: 100px" required></textarea>
                        </div>
                    </div>

                </div>

                <div v-if="role === 'Sponsor'">

                    <div class = "form-group mb-3">
                        <label for = "name" class = "mb-2">Name</label>
                        <input v-model = "name" type = "name" class = "form-control" required>
                    </div>

                    <div class = "form-group mb-3">
                        <label for = "email" class = "mb-2">Email ID</label>
                        <input v-model = "email" type = "email" class = "form-control" required>
                    </div>

                    <div id = "industry" class = " form-group mb-3">
                        <label for = "industry" class = "mb-2">Industry</label>
                        <select v-model = "industry" class = "form-select" id = "industry" required>
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
                        <select v-model = "valuation" class = "form-select" id = "valuation" required>
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
                            <textarea v-model = "description" class = "form-control" id = "description" style="height: 100px" required></textarea>
                        </div>
                    </div>

                </div>

                <div class = "mt-4">
                    <button class = "btn btn-primary w-100" @click ="registerUser">Register</button>
                </div>

        </div>
    </div>

</template>

<script>

import axios from "../assets/axios.js";

export default {
    name: 'RegisterView',
    data() {
        return{
            username: "",
            password: "",
            role: "",
            name: "",
            email: "",
            category: "",
            reach: "",
            description: "",
            industry: "",
            valuation: ""
        };
    },
    methods: {
        async registerUser() {
            const url = `/user/registration`;

            let body = {
                username: this.username,
                password: this.password,
                role: this.role,
            };

            if (this.role === "Influencer") {
                body = {
                    ...body,
                    name: this.name,
                    email: this.email,
                    category: this.category,
                    reach: this.reach,
                    description: this.description
                };
            } else if (this.role === "Sponsor") {
                body = {
                    ...body,
                    name: this.name,
                    email: this.email,
                    industry: this.industry,
                    valuation: this.valuation,
                    description: this.description
                };
            }

            try {
                const response = await axios.post(url, body);

                console.log('Response status:', response.status);
                console.log('Response data:', response.data);

                if (response.status >= 200 && response.status < 300) {
                    alert("User registered successfully!");
                    this.$router.push("/user/login");
                } else {
                    alert("User registration failed!");
                }
            } catch (error) {
                console.error("There was an error registering the user:", error);
                alert("User registration failed!");
            }
        }
    }
}
</script>

<style scoped>
.register {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #D9D9D9;
}
#navbar {
  background-color: #284B63;
}
#navbar-brand {
  color: #FFFFFF;
  font-weight: bold;
}
#loginbutton {
  color: #FFFFFF;
  font-weight: bold;
  font-size: large;
}
#card {
    width: 1000px;
    height: auto;
    margin: 80px;
    color: #353535;
}
#cardtitle {
    font-weight: bold;
    font-size: 3em;
    color: #E76F51;
}
</style>
