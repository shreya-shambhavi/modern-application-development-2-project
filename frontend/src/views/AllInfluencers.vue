<template>
    <div>
        <div class="all-influencers">
            <div>
                <h1>Influencers On Platform</h1>
                <p>These are all the influencers on the platform.</p>
            </div>
        </div>
        <div v-if="all_influencers.length === 0">
            <p id="no-results">No influencers to show.</p>
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
                        <tr v-for="(influencer, index) in all_influencers" :key="influencer.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ influencer.name }}</td>
                            <td>{{ influencer.category }}</td>
                            <td>{{ influencer.reach }}</td>
                            <td><router-link :to="{ name: 'AdminViewInfluencerDetails', params: { id: influencer.id } }"><button type="button" class="btn btn-warning">View</button></router-link></td>
                            <td v-if="influencer.flag_status === 'Unflagged'"><button @click="flagInfluencer(influencer.id)" class="btn btn-danger">Flag</button></td>
                            <td v-else><button @click="unflagInfluencer(influencer.id)" class="btn btn-success">Unflag</button></td>
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
    name: 'AllInfluencers',
    data() {
        return {
            all_influencers: {},
        };
    },
    created() {
        this.getAllInfluencers();
    },
    methods: {
        async getAllInfluencers() {
            try {
                const response = await axios.get('/admin/all_influencers');
                this.all_influencers = response.data.all_influencers;
            } catch (error) {
                console.error('Error fetching all influencers:', error.response ? error.response.data : error.message);
            }
        },
        async flagInfluencer(id) {
            try {
                const response = await axios.put(`/api/influencer/${id}`, { flag_status: "Flagged" });
                if (response.status === 200) {
                    alert('Influencer flagged successfully');
                    this.getAllInfluencers();
                }
            } catch (error) {
                console.error('Error flagging influencer:', error.response ? error.response.data : error.message);
                alert('Error flagging influencer');
            }
        },
        async unflagInfluencer(id) {
            try {
                const response = await axios.put(`/api/influencer/${id}`, { flag_status: "Unflagged" });
                if (response.status === 200) {
                    alert('Influencer unflagged successfully');
                    this.getAllInfluencers();
                }
            } catch (error) {
                console.error('Error unflagging influencer:', error.response ? error.response.data : error.message);
                alert('Error unflagging influencer');
            }
        }

    }
}
</script>

<style scoped>
.all-influencers {
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
