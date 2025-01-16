<template>
    <div>

        <div class="monitor-tasks">
            <div>
                <h1>Monitor Active Tasks</h1>
                <p>Monitor the progress of your active ad requests here.</p>
            </div>
        </div>
        <div v-if="monitor_influencer_tasks.length === 0">
            <p id="no-results">No active tasks to show.</p>
        </div>
        <div v-else>
            <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Campaign Name</th>
                            <th>Influencer Name</th>
                            <th>Work Progress Bar</th>
                            <th>Action</th>
                            <th>Campaign Details</th>
                            <th>Request Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(task, index) in monitor_influencer_tasks" :key="task.id">
                            <td>{{ index + 1 }}</td>
                            <td>{{ task.campaign.name }}</td>
                            <td>{{ task.influencer.name }}</td>

                            <td v-if="task.work_status === '0%'">
                                <div class="progress" role="progressbar" aria-label="Animated striped" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 0%">0%</div>
                                </div>
                            </td>
                            <td v-else-if="task.work_status === '25%'">
                                <div class="progress" role="progressbar" aria-label="Animated striped" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 25%">25%</div>
                                </div>
                            </td>
                            <td v-else-if="task.work_status === '50%'">
                                <div class="progress" role="progressbar" aria-label="Animated striped" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 50%">50%</div>
                                </div>
                            </td>
                            <td v-else-if="task.work_status === '75%'">
                                <div class="progress" role="progressbar" aria-label="Animated striped" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 75%">75%</div>
                                </div>
                            </td>
                            <td v-else>
                                <div class="progress" role="progressbar" aria-label="Animated striped" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%">100%</div>
                                </div>
                            </td>

                            <td v-if="task.work_status === '0%'"><button id="action" @click="updateTask(task)" class="btn btn-outline-danger" disabled>0% Done</button></td>
                            <td v-else-if="task.work_status === '25%'"><button id="action" @click="updateTask(task)" class="btn btn-outline-danger" disabled>25% done</button></td>
                            <td v-else-if="task.work_status === '50%'"><button id="action" @click="updateTask(task)" class="btn btn-outline-warning" disabled>50% done</button></td>
                            <td v-else-if="task.work_status === '75%'"><button id="action" @click="updateTask(task)" class="btn btn-outline-warning" disabled>75% done</button></td>
                            <td v-else-if="task.work_status === '100%'"><button id="action" @click="updateTask(task)" class="btn btn-outline-success" disabled>100% done</button></td>
                            <td v-else-if="task.work_status === 'Confirmation Pending'"><button id="action" @click="updateTask(task)" class="btn btn-success">Confirm</button></td>
                            <td v-else-if="task.work_status === 'Payment Pending'"><button id="action" @click="updateTask(task)" class="btn btn-success">Pay</button></td>
                            <td v-else-if="task.work_status === 'Payment Recieved'"><button id="action" @click="updateTask(task)" class="btn btn-danger">Paid</button></td>

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
    name: 'MonitorTasks',
    data() {
        return {
            monitor_influencer_tasks: {},
        };
    },
    created() {
        this.getActiveTasks();
    },
    methods: {
        async getActiveTasks() {
            try {
                const response = await axios.get('/sponsor/monitor_influencer_tasks');
                this.monitor_influencer_tasks = response.data.monitor_influencer_tasks;
            } catch (error) {
                console.error("Error Fetching Active Tasks : ", error);
            }
        },
        async updateTask(task) {
            try {
                let work_status;
                if (task.work_status === '0%') {
                    work_status = '25%';
                } else if (task.work_status === '25%') {
                    work_status = '50%';
                } else if (task.work_status === '50%') {
                    work_status = '75%';
                } else if (task.work_status === '75%') {
                    work_status = '100%';
                } else if (task.work_status === '100%') {
                    work_status = 'Confirmation Pending';
                } else if (task.work_status === 'Confirmation Pending') {
                    work_status = 'Payment Pending';
                } else if (task.work_status === 'Payment Pending') {
                    work_status = 'Payment Received';
                }

                const response = await axios.put(`/api/adrequest/${task.id}`, { 
                    id: task.id,
                    campaign_id: task.campaign_id,
                    influencer_id: task.influencer_id,
                    title: task.title,
                    message: task.message,
                    requirements: task.requirements,
                    payment: task.payment,
                    status: task.status,
                    owner: task.owner,
                    work_status: work_status,
                });

                console.log("Task Updated Successfully");
                alert("Task Updated Successfully");
                this.getActiveTasks();

            } catch (error) {
                console.error("Error Updating Task : ", error);
                alert("Error Updating Task : ", error);
            }
        }
    }
}
</script>

<style scoped>
.monitor-tasks {
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
#action {
    font-weight: bolder;
}
</style>
