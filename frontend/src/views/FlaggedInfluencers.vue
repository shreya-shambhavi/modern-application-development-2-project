<template>
    <div>

        <div class="flagged-influencers">
            <div>
                <h1>Flagged Influencers On Platform</h1>
                <p>These are all the flagged influencers on the platform.</p>
            </div>
        </div>
        <div v-if="flagged_influencers.length === 0">
            <p id="no-results">No flagged influencers to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Influencer Name</th>
                            <th>Category</th>
                            <th>Reach</th>
                            <th>Details</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(influencer, index) in flagged_influencers" :key="influencer.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ influencer.name }}</td>
                            <td>{{ influencer.category }}</td>
                            <td>{{ influencer.reach }}</td>
                            <td><router-link :to="{ name: 'AdminViewInfluencerDetails', params: { id: influencer.id } }"><button type="button" class="btn btn-warning">View</button></router-link></td>
                            <td><button @click="removeInfluencer(influencer.id)" class="btn btn-danger">Remove</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
    </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: 'FlaggedInfluencers',
    data() {
        return {
            flagged_influencers: {},
        };
    },
    created() {
        this.getFlaggedInfluencers();
    },
    methods: {
        async getFlaggedInfluencers() {
            try {
                const response = await axios.get('/admin/flagged_influencers');
                this.flagged_influencers = response.data.flagged_influencers;
            } catch (error) {
                console.error('Error fetching all flagged influencers:', error.response ? error.response.data : error.message);
            }
        },
        async removeInfluencer(id) {
            const confirmDelete = confirm('Are you sure you want to remove this influencer?');
            if (confirmDelete) {

                try {
                    const response = await axios.delete(`/api/influencer/${id}`);
                    if (response.status === 204) {
                        alert('Influencer removed successfully');
                        this.flagged_influencers = this.flagged_influencers.filter(influencer => influencer.id !== id);
                    }
                } catch (error) {
                    console.error('Error removing influencer:', error.response ? error.response.data : error.message);
                    alert('Error removing influencer');
                }
            }    
        }
    }
}
</script>

<style scoped>
.flagged-influencers {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
    margin-bottom: 10px;
    padding-left: 10px;
    padding-right: 10px;
}
h1 {
    font-size: 2.5em;
    text-align: center;
    font-weight: bold;
    color: #E76F51;
    font-style: oblique;
    padding: 10px;
}
p {
    font-size: 1em;
    font-style: oblique;
    text-align: center;
    padding-left: 25px;
    padding-right: 25px;
    color: #353535;
}
#no-results {
    padding: 20px;
}
.table-container {
    padding-left: 20px;
    padding-right: 20px;
    width: 100%;
    text-align: center;
    vertical-align: middle;
}
th {
    vertical-align: middle;
}
td {
    vertical-align: middle;
}
</style>
