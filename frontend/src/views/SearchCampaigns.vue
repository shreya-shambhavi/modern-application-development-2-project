<template>

    <div class="d-flex justify-content-end">
        <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
    </div>

    <div class="search-campaign">
        <div class="search-container">
            <div id="random">
                <h1>Search Campaigns</h1>

                <div class = "form-group mb-3">
                    <label for = "name" class = "mb-2">Name</label>
                    <input v-model = "searchQuery.name" type="search" class="form-control me-2" placeholder="Search">
                </div>

                <div id = "budget" class = "form-group mb-3">
                    <label for = "budget" class = "mb-2">Budget</label>
                    <input v-model = "searchQuery.budget" type = "number" class = "form-control me-2" placeholder="Search">
                </div>

                <div id = "target_audience" class = "form-group mb-3">
                    <label for = "target_audience" class = "mb-2">Target Audience</label>
                    <select v-model="searchQuery.target_audience" class="form-select">
                        <option value="Tech Enthusiasts">Tech Enthusiasts</option>
                        <option value="Health-Conscious Individuals">Health-Conscious Individuals</option>
                        <option value="Travel Enthusiasts">Travel Enthusiasts</option>
                        <option value="Fashion Lovers">Fashion Lovers</option>
                        <option value="Foodies">Foodies</option>
                        <option value="Gamers">Gamers</option>
                        <option value="Beauty Enthusiasts">Beauty Enthusiasts</option>
                        <option value="Photography Enthusiasts">Photography Enthusiasts</option>
                        <option value="Lifestyle Influencers">Lifestyle Influencers</option>
                        <option value="Music Lovers">Music Lovers</option>
                    </select>
                </div>

                <div class="search-button">
                    <button @click="Search" class="btn btn-outline-success" type="submit">Search</button>
                </div>
            </div>
        </div>
    </div>

    <div v-if="results.length" class="results-container">

        <h2 id="searches">Search Results</h2>

        <div class="table-container">
            <table class="table table-bordered table hover">
                <thead class="table-dark">
                    <tr>
                        <th>S No.</th>
                        <th>Campaign Name</th>
                        <th>Sponsor Name</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Details</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(result, index) in results" :key="result.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ result.name }}</td>
                        <td>{{ result.sponsor.name }}</td>
                        <td>{{ result.start_date }}</td>
                        <td>{{ result.end_date }}</td>
                        <td><router-link :to="{ name: 'InfluencerViewCampaignDetails', params: { id: result.id } }"><button class="btn btn-warning">View</button></router-link></td>
                        <td><button @click="goToCreateAdrequestPage(result.id)" class="btn btn-success">Request</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div v-if="results.length === 0 && searchAttempted" class="no-results">
        <p>No campaign found matching your search criteria.</p>
    </div>

</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: "SearchCampaigns",
    data() {
    return {
        searchQuery: {
            name: "",
            budget: 0,
            target_audience: ""
        },
            results: [],
            searchAttempted: false
        };
    },
    methods: {
        Search() {
            this.searchAttempted = true;
            axios.post('/search-campaigns', this.searchQuery)
                .then((response) => {
                    this.results = response.data.searchQuery;
            })
            .catch((error) => {
                console.log(error);
            });
        },
        goToCreateAdrequestPage(campaign_id) {
            if (campaign_id) {
                this.$router.push({ name: 'InfluencerCreateAdrequest', params: { id: campaign_id } });
            } else {
                console.error('Campaign ID is not available');
            }
        },
        goBack() {
            this.$router.go(-1);
        }
    }
};
</script>

<style scoped>
.search-campaign {
display: flex;
justify-content: center;
align-items: center;
margin-top: 50px;
margin-bottom: 50px;
margin-left: 50px;
margin-right: 50px;
}
#random {
padding-left: 20px;
padding-right: 20px;
}
.search-container {
display: flex;
justify-content: center;
align-items: center;
padding-left: 200px;
padding-right: 200px;
}
h1 {
text-align: center;
margin-bottom: 30px;
font-size: 3em;
font-weight: bold;
font-style: oblique;
color: #E76F51;
}
#searches {
font-size: 2.5em;
font-style: oblique;
text-align: center;
color: #2A9D8F;
margin-bottom: 50px;
}
.search-button {
margin-bottom: 20px;
text-align: center;
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
.no-results {
margin-top: 20px;
text-align: center;
color: #888;
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
