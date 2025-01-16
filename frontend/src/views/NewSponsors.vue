<template>
    <div>

        <div class="new-sponsors">
            <div>
                <h1>New Sponsors For Approval</h1>
                <p>Here are the new sponsors that have signed up and are waiting for approval.</p>
            </div>
        </div>

        <div v-if="new_sponsors.length == 0">
            <p id="no-results">No new sponsors to approve.</p>
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
                        <tr v-for="(sponsor, index) in new_sponsors" :key="sponsor.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ sponsor.name }}</td>
                            <td>{{ sponsor.industry }}</td>
                            <td>{{ sponsor.valuation }}</td>
                            <td><router-link :to="{ name: 'AdminViewSponsorDetails', params: { id: sponsor.id } }"><button type="button" class="btn btn-warning">View</button></router-link></td>
                            <td><button @click="approveSponsor(sponsor.user_id)" class="btn btn-success">Approve</button></td>
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
    name: 'NewSponsors',
    data() {
        return {
            new_sponsors: {},
        }
    },
    created() {
        this.fetchNewSponsors();
    },
    methods: {
        async fetchNewSponsors() {
            try {
                const response = await axios.get('/admin/new_sponsors');
                this.new_sponsors = response.data.new_sponsors;
            } catch (error) {
                console.error('Error fetching new sponsors:', error.response ? error.response.data : error.message);
            }
        },
        async approveSponsor(user_id) {
            try {
                const response = await axios.put(`/api/user/${user_id}`, { active : true });
                if (response.status === 200) {
                    this.new_sponsors = this.new_sponsors.filter(sponsor => sponsor.user_id !== user_id);
                    alert('Sponsor approved successfully');
                }
            } catch (error) {
                console.error('Error approving sponsor:', error.response ? error.response.data : error.message);
                alert('Error approving sponsor');
            }
        }
    },
}
</script>

<style scoped>
.new-sponsors {
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
