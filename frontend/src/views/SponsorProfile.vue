<template>
    <div>
        <div class="sponsor-profile">
            <div>
                <h1>{{ sponsor.name }}</h1>
                <h4>Sponsor</h4>
                <br>
                <p>User ID : <span>{{ sponsor.user_id }}</span></p>
                <p>Sponsor ID : <span>{{ sponsor.id }}</span></p>
                <p>Email Address : <span>{{ sponsor.email }}</span></p>
                <p>Industry : <span>{{ sponsor.industry }}</span></p>
                <p>Valuation : <span>{{ sponsor.valuation }}</span></p>
                <br>
                <p>{{ sponsor.description }}</p>

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
    name: 'SponsorProfile',
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
                const response = await axios.get('/sponsor/profile');
                this.sponsor = response.data.sponsor;
            } catch (error) {
                console.error("Error Fetching sponsor : ", error);
            }
        },
        goToUpdatePage() {
            this.$router.push({ name: 'SponsorProfileUpdate', params: { id: this.sponsor.id } });
        }
    }
}
</script>

<style scoped>
.sponsor-profile {
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
