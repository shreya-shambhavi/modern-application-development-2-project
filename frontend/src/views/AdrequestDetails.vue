<template>

    <div class="d-flex justify-content-end">
        <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
    </div>

    <div class="adrequest-details" v-if="adrequest && Object.keys(adrequest).length > 0">
        <div>
            <h1>Ad Request Details</h1>
            <br>

            <p>Adrequest ID : <span>{{ adrequest.id }}</span></p>
            <p>Campaign Name : <span>{{ adrequest.campaign.name }}</span></p>
            <p>Influencer Name : <span>{{ adrequest.influencer.name }}</span></p>
            <p>Owner : <span>{{ adrequest.owner }}</span></p>
            <p>Title : <span>{{ adrequest.title }}</span></p>
            <p>Message : <span>{{ adrequest.message }}</span></p>
            <p>Requirements : <span>{{ adrequest.requirements }}</span></p>
            <p>Status : <span>{{ adrequest.status }}</span></p>
            <p>Work Status : <span>{{ adrequest.work_status }}</span></p>
            <br>
            <p id="payment"><b>Payment Amount : {{ adrequest.payment }}</b></p>
        </div>
    </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: 'AdrequestDetails',
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            adrequest: {},
        }
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
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>

<style scoped>
.adrequest-details {
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
#close-button {
    margin: 10px;
    padding: 10px;
    background-color: #E76F51;
    color: white;
    border: none;
    border-radius: 50%;
}
#payment {
    color: crimson;
    font-weight: bolder;
    font-size: 2em;
}
</style>
