<template>
    <div v-if="role">

        <div v-if= "role === 'Admin'">
            <nav class="navbar navbar-expand-lg">
                <div class="container-fluid">
                    <router-link id="nav-brand" class="navbar-brand" to="/admin/dashboard">Admin Dashboard</router-link>

                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>

                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/sponsors/new" active-class="active-link">New Sponsors</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/influencers/all" active-class="active-link">Influencers</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/sponsors/all" active-class="active-link">Sponsors</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/campaigns/all" active-class="active-link">Campaigns</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/adrequests/all" active-class="active-link">Adrequests</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/influencers/flagged" active-class="active-link">Flagged Influencers</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/sponsors/flagged" active-class="active-link">Flagged Sponsors</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/campaigns/flagged" active-class="active-link">Flagged Campaigns</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/admin/dashboard/platform/statistics" active-class="active-link">Platform Statistics</router-link>
                            </li>
                        </ul>

                        <div>
                            <button @click="LogoutUser" type="button" class="btn btn-danger">Logout</button>
                        </div>
                    </div>
                </div>
            </nav>
        </div>

        <div v-if= "role === 'Influencer'">
          <nav class="navbar navbar-expand-lg">
                <div class="container-fluid">
                    <router-link id="nav-brand" class="navbar-brand" to="/influencer/dashboard">Influencer Dashboard : <span>{{ username }}</span></router-link>

                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>

                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/influencer/dashboard/profile" active-class="active-link">Profile Page</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/influencer/dashboard/tasks/active" active-class="active-link">Active Tasks</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/influencer/dashboard/tasks/completed" active-class="active-link">Completed Tasks</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/influencer/dashboard/campaigns/public" active-class="active-link">Find a Campaign</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/influencer/dashboard/requests/recieved" active-class="active-link">New Ad Requests</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/influencer/dashboard/requests/sent" active-class="active-link">Requests Sent</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/influencer/dashboard/requests/directory" active-class="active-link">Requests Directory</router-link>
                            </li>
                        </ul>

                        <div>
                            <button @click="LogoutUser" type="button" class="btn btn-danger">Logout</button>
                        </div>
                    </div>
                </div>
            </nav>
        </div>

        <div v-if= "role === 'Sponsor'">
          <nav class="navbar navbar-expand-lg">
                <div class="container-fluid">
                    <router-link id="nav-brand" class="navbar-brand" to="/sponsor/dashboard">Sponsor Dashboard : <span>{{ username }}</span></router-link>

                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>

                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/sponsor/dashboard/profile" active-class="active-link">Profile Page</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/sponsor/dashboard/mycampaigns" active-class="active-link">My Campaigns</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/sponsor/dashboard/monitor/tasks/active" active-class="active-link">Monitor</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/sponsor/dashboard/review/tasks/completed" active-class="active-link">Review</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/sponsor/dashboard/find/influencers" active-class="active-link">Find an Influencer</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/sponsor/dashboard/requests/recieved" active-class="active-link">New Ad Requests</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/sponsor/dashboard/requests/sent" active-class="active-link">Requests Sent</router-link>
                            </li>
                            <li class="nav-item ms-1">
                                <router-link id="nav-links" class="nav-link active" aria-current="page" to="/sponsor/dashboard/requests/directory" active-class="active-link">Requests Directory</router-link>
                            </li>
                        </ul>

                        <div>
                            <button @click="LogoutUser" type="button" class="btn btn-danger">Logout</button>
                        </div>
                    </div>
                </div>
            </nav>
        </div>

    </div>
</template>

<script>
export default {
    name: 'Navbar',
    computed: {
        role() {
            return this.$store.state.role
        },
        username() {
            return this.$store.state.username
        }
    },
    methods: {
        LogoutUser() {
          this.$store.dispatch('logout');
          this.$router.push('/');
        }
    },
} 
</script>

<style scoped>
nav {
  background-color: #3C6E71;
}
#nav-brand {
  color: #F4A261;
  font-weight: bold;
}
#nav-links {
  color: white;
}
.active-link {
  font-weight: bolder;
}
span {
  color: #E9C46A;
}
</style>
