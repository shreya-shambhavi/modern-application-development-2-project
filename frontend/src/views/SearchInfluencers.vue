<template>

  <div class="d-flex justify-content-end">
    <button @click="goBack" id="close-button" type="button" class="btn-close" aria-label="Close"></button>
  </div>

  <div class="search-influencer">
    <div class="search-container">
      <div>
        <h1>Search Influencers</h1>

        <div class = "form-group mb-3">
          <label for = "name" class = "mb-2">Name</label>
          <input v-model = "searchQuery.name" type="search" class="form-control me-2" placeholder="Search">
        </div>

        <div id = "category" class = "form-group mb-3">
          <label for = "category" class = "mb-2">Category</label>
          <select v-model="searchQuery.category" class="form-select">
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
          <select v-model="searchQuery.reach" class="form-select">
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
                  <th>Influencer Name</th>
                  <th>Category</th>
                  <th>Reach</th>
                  <th>Details</th>
                  <th>Action</th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="(result, index) in results" :key="result.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ result.name }}</td>
                  <td>{{ result.category }}</td>
                  <td>{{ result.reach }}</td>
                  <td><router-link :to="{ name: 'SponsorViewInfluencerDetails', params: { id: result.id } }"><button class="btn btn-warning">View</button></router-link></td>
                  <td><button @click="goToCreateAdrequestPage(result.id)" class="btn btn-success">Request</button></td>
              </tr>
          </tbody>
      </table>
    </div>
  </div>

  <div v-if="results.length === 0 && searchAttempted" class="no-results">
    <p>No influencers found matching your search criteria.</p>
  </div>

</template>

<script>
import axios from '../assets/axios.js';

export default {
  name: "SearchInfluencers",
  data() {
    return {
      searchQuery: {
        name: "",
        category: "",
        reach: ""
      },
      results: [],
      searchAttempted: false
    };
  },
  methods: {
    Search() {
      this.searchAttempted = true;
      axios.post('/search-influencers', this.searchQuery)
        .then((response) => {
          this.results = response.data.searchQuery;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    goToCreateAdrequestPage(influencer_id) {
        if (influencer_id) {
            this.$router.push({ name: 'SponsorCreateAdrequest', params: { id: influencer_id }, query: { type: 'influencer' } });
        } else {
            console.error('Influencer ID is not available');
        }
    },
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.search-influencer {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
  margin-bottom: 50px;
  margin-left: 50px;
  margin-right: 50px;
}
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-left: 100px;
  padding-right: 100px;
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
