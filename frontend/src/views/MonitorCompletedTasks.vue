<template>
    <div>

        <div class="completed-tasks">
            <div>
                <h1>Review Completed Tasks</h1>
                <p>Here you can view all the tasks that have been completed.</p>
            </div>
        </div>

        <div>
            <h4 id="total-payments">Total Payments: ${{ total_payments }}</h4>
        </div>

        <div v-if="review_completed_tasks.length === 0">
            <p id="no-results">No completed tasks to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Campaign Name</th>
                            <th>Influencer Name</th>
                            <th>Payment Amount</th>
                            <th>Payment Status</th>
                            <th>Campaign Details</th>
                            <th>Request Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(task, index) in review_completed_tasks" :key="task.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ task.campaign.name }}</td>
                            <td>{{ task.influencer.name }}</td>
                            <td>{{ task.payment }}</td>
                            <td id="payment">Paid</td>
                            <td><router-link :to="{ name: 'SponsorViewCampaignDetails', params: { id: task.campaign.id } }"><button class="btn btn-warning">View</button></router-link></td>
                            <td><router-link :to="{ name: 'SponsorViewAdrequestDetails', params: { id: task.id } }"><button class="btn btn-warning">View</button></router-link></td>
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
    name: 'MonitorCompletedTasks',
    data() {
        return {
            review_completed_tasks: {},
            total_payments: 0,
        };
    },
    created() {
        this.getReviewCompletedTasks();
        this.getTotalPayments();
    },
    methods: {
        async getReviewCompletedTasks() {
            try {
                const response = await axios.get('/sponsor/review_completed_tasks');
                this.review_completed_tasks = response.data.review_completed_tasks;
            } catch (error) {
                console.error("Error Fetching Completed Tasks : ", error);
            }
        },
        async getTotalPayments() {
            try {
                const response = await axios.get('/sponsor/total_payments');
                this.total_payments = response.data.total_payments;
            } catch (error) {
                console.error("Error Fetching Total Payments : ", error);
            }
        }
    }
}
</script>

<style scoped>
.completed-tasks {
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
th, td {
    vertical-align: middle;
}
.progress {
    height: 25px;
    width: 500px;
    margin: 0 auto;

}
#payment {
    color: green;
    font-weight: bolder;
    font-size: large;
}
#total-payments {
    font-size: 1.5em;
    text-align: center;
    font-style: oblique;
    font-weight: bolder;
    color: crimson;
    padding: 10px;
    margin-top: 10px;
    margin-bottom: 25px;
}
</style>
