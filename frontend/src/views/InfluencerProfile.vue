<template>
    <div>
        <div class="influencer-profile">
            <div>
                <h1>{{ influencer.name }}</h1>
                <h4>Influencer</h4>
                <br>
                <p>User ID : <span>{{ influencer.user_id }}</span></p>
                <p>Influencer ID : <span>{{ influencer.id }}</span></p>
                <p>Email Address : <span>{{ influencer.email }}</span></p>
                <p>Category : <span>{{ influencer.category }}</span></p>
                <p>Reach : <span>{{ influencer.reach }}</span></p>
                <br>
                <p>{{ influencer.description }}</p>

                <div class="update">
                    <button @click="goToUpdatePage" type="button" class="btn btn-primary">Update Profile Details</button>
                </div>

            </div>
        </div>
    </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: 'InfluencerProfile',
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
                const response = await axios.get('/influencer/profile');
                this.influencer = response.data.influencer;
            } catch (error) {
                console.error("Error Fetching Influencer : ", error);
            }
        },
        goToUpdatePage() {
            this.$router.push({ name: 'InfluencerProfileUpdate', params: { id: this.influencer.id } });
        }
    }
}
</script>

<style scoped>
.influencer-profile {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
    margin-bottom: 50px;
    padding-left: 50px;
    padding-right: 50px;
}
h1 {
    font-size: 3.5em;
    text-align: center;
    font-weight: bold;
    color: #E76F51;
    font-style: oblique;
    padding: 10px;
}
h4 {
    font-size: 1.5em;
    text-align: center;
    font-style: oblique;
    color: #F4A261;
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
.update {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
    margin-bottom: 50px;
}
</style>
