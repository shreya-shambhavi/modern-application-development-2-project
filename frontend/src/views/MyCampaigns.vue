<template>

    <div class="mycampaigns">
        <div>
            <h1>My Campaigns</h1>
            <p>Here you can see all the campaigns you have created.</p>
        </div>
    </div>

    <div class="buttons">

        <div v-if=" sponsor.flag_status === 'Unflagged' ">
            <button @click="goToCreateCampaign(sponsor.id)" id="create" type="button" class="btn btn-danger">Create New Campaign +</button>
        </div>
        <div v-else>
            <button id="create" type="button" class="btn btn-danger" disabled>Create New Campaign +</button>
        </div>

        <button @click="exportCampaigns" id="export" type="button" class="btn">Export Data as CSV</button>
    </div>

    <div v-if="my_campaigns.length === 0">
        <p id="no-results">No campaign to show.</p>
    </div>

    <div v-else>
        <div class="table-container">
            <table class="table table-bordered table hover">
                <thead class="table-dark">
                    <tr>
                        <th>S No.</th>
                        <th>Campaign Name</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Visibility</th>
                        <th>Details</th>
                        <th>Action</th>
                        <th>Create</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(campaign, index) in my_campaigns" :key="campaign.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ campaign.name }}</td>
                        <td>{{ campaign.start_date }}</td>
                        <td>{{ campaign.end_date }}</td>
                        <td>{{ campaign.visibility }}</td>
                        <td><router-link :to="{ name: 'SponsorViewCampaignDetails', params: { id: campaign.id } }"><button class="btn btn-warning">View</button></router-link></td>
                        <td><router-link :to="{ name: 'SponsorUpdateCampaign', params: { id: campaign.id } }"><button class="btn btn-primary">Update</button></router-link></td>
                        <td v-if=" campaign.flag_status === 'Unflagged' "><button @click="goToCreateAdrequestPage(campaign.id)" class="btn btn-success">New Adrequest</button></td>
                        <td v-else><button class="btn btn-success" disabled>New Adrequest</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: 'MyCampaigns',
    data() {
        return {
            my_campaigns: {},
            sponsor: {},
        };
    },
    created() {
        this.getMyCampaigns();
        this.getSponsor();
    },
    methods: {
        async getMyCampaigns() {
            try {
                const response = await axios.get('/sponsor/my_campaigns');
                this.my_campaigns = response.data.my_campaigns;
            } catch (error) {
                console.error("Error fetching campaigns", error);
            }
        },
        async getSponsor() {
            try {
                const response = await axios.get('/sponsor/profile');
                this.sponsor = response.data.sponsor;
            } catch (error) {
                console.error("Error fetching sponsor", error);
            }
        },
        goToCreateCampaign(sponsor_id) {
            if (sponsor_id) {
                this.$router.push({ name: 'CreateCampaign', params: { id: sponsor_id } });
            } else {
                console.error("Sponsor ID is not available");
            }
        },
        goToCreateAdrequestPage(campaign_id) {
            if (campaign_id) {
                this.$router.push({ name: 'SponsorCreateAdrequest', params: { id: campaign_id }, query: { type: 'campaign' } });
            } else {
                console.error("Campaign ID is not available");
            }
        },
        exportCampaigns() {
            axios.get('/sponsor/export_campaigns')
                .then(response => {
                    const taskId = response.data.task_id;

                    const checkTaskStatus = setInterval(() => {
                        axios.get(`/download_campaigns/${taskId}`, { responseType: 'blob' })
                            .then(downloadResponse => {
                                if (downloadResponse.status === 200) {
                                    alert("File is ready for download!");
                                    console.log("File is ready for download!");
                                    clearInterval(checkTaskStatus);
                                    const url = window.URL.createObjectURL(new Blob([downloadResponse.data]));
                                    const link = document.createElement('a');
                                    link.href = url;
                                    link.setAttribute('download', 'campaigns.csv');
                                    document.body.appendChild(link);
                                    link.click();
                                    document.body.removeChild(link);
                                }
                            })
                            .catch(error => {
                                if (error.response && error.response.status !== 404) {
                                    clearInterval(checkTaskStatus);
                                    console.error("Error downloading the file:", error);
                                }
                            });
                    }, 3000);
                })
                .catch(error => {
                    console.error("Error triggering export:", error);
                });
        }
    }

        // exportCampaigns() {

        // axios.get('/sponsor/export_campaigns')
        //     .then(response => {
        //     const taskId = response.data.task_id;

        //     const checkTaskStatus = setInterval(() => {
        //         axios.get(`/download_campaigns/${taskId}`)
        //         .then(downloadResponse => {
        //             if (downloadResponse.status === 200) {
        //                 alert("File is ready for download!");
        //                 clearInterval(checkTaskStatus);

        //                 const url = window.URL.createObjectURL(new Blob([downloadResponse.data]));
        //                 const link = document.createElement('a');
        //                 link.href = url;
        //                 link.setAttribute('download', 'campaigns.csv');
        //                 document.body.appendChild(link);
        //                 link.click();
        //                 document.body.removeChild(link);
        //             }
        //         })
        //         .catch(error => {
        //             if (error.response && error.response.status !== 404) {
        //                 clearInterval(checkTaskStatus);
        //                 console.error("Error downloading the file:", error);
        //             }
        //         });
        //     }, 3000);
        //     })
        //     .catch(error => {
        //     console.error("Error triggering export:", error);
        //     });
        // }

}
</script>

<style scoped>
.mycampaigns {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
    margin-bottom: 10px;
    padding-left: 10px;
    padding-right: 10px;
}
.buttons {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    margin-bottom: 20px;
    padding-left: 20px;
    padding-right: 20px;
}
#create {
    font-weight: bold;
    padding: 10px;
    margin-right: 10px;
}
#export {
    font-weight: bold;
    padding: 10px;
    background-color: #4A4E69;
    color: white;
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
