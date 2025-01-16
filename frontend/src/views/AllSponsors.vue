<template>
    <div>
        
        <div class="all-sponsors">
            <div>
                <h1>Sponsors On Platform</h1>
                <p>These are all the sponsors on the platform.</p>
            </div>
        </div>
        <div v-if="all_sponsors.length === 0">
            <p id="no-results">No sponsors to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Sponsor Name</th>
                            <th>Industry</th>
                            <th>Valuation</th>
                            <th>Details</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(sponsor, index) in all_sponsors" :key="sponsor.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ sponsor.name }}</td>
                            <td>{{ sponsor.industry }}</td>
                            <td>{{ sponsor.valuation }}</td>
                            <td><router-link :to="{ name: 'AdminViewSponsorDetails', params: { id: sponsor.id } }"><button type="button" class="btn btn-warning">View</button></router-link></td>
                            <td v-if="sponsor.flag_status === 'Unflagged'"><button @click="flagSponsor(sponsor.id)" class="btn btn-danger">Flag</button></td>
                            <td v-else><button @click="unflagSponsor(sponsor.id)" class="btn btn-success">Unflag</button></td>
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
    name: 'AllSponsors',
    data() {
        return {
            all_sponsors: {},
        };
    },
    created() {
        this.getAllSponsors();
    },
    methods: {
        async getAllSponsors() {
            try {
                const response = await axios.get('/admin/all_sponsors');
                this.all_sponsors = response.data.all_sponsors;
            } catch (error) {
                console.error('Error fetching all sponsors:', error.response ? error.response.data : error.message);
            }
        },
        async flagSponsor(id) {
            try {
                const response = await axios.put(`/api/sponsor/${id}`, { flag_status: "Flagged" });
                if (response.status === 200) {
                    alert('Sponsor flagged successfully');
                    this.getAllSponsors();
                }
            } catch (error) {
                console.error('Error flagging sponsor:', error.response ? error.response.data : error.message);
                alert('Error flagging sponsor');
            }
        },
        async unflagSponsor(id) {
            try {
                const response = await axios.put(`/api/sponsor/${id}`, { flag_status: "Unflagged" });
                if (response.status === 200) {
                    alert('Sponsor unflagged successfully');
                    this.getAllSponsors();
                }
            } catch (error) {
                console.error('Error unflagging sponsor:', error.response ? error.response.data : error.message);
                alert('Error unflagging sponsor');
            }
        }
    }
}
</script>

<style scoped>
.all-sponsors {
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
