<template>
    <div>
        <div class="platform-statistics">
            <div>
                <h1>Platform Statistics</h1>
                <p>These are the statistics of the platform.</p>
            </div>
        </div>
        <div class="table-container">
                <table class="table table-bordered table hover">
                    <thead class="table-dark">
                        <tr>
                            <th>S No.</th>
                            <th>Measure</th>
                            <th>Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td id="serial-number">1</td>
                            <td id="measure">Total Number Of Active Sponsors</td>
                            <td id="count">{{ platform_statistics.total_sponsors }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">2</td>
                            <td id="measure">Total Number Of Active Influencers</td>
                            <td id="count">{{ platform_statistics.total_influencers }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">3</td>
                            <td id="measure">Total Number Of Active Campaigns</td>
                            <td id="count">{{ platform_statistics.active_campaigns }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">4</td>
                            <td id="measure">Total Number Of Active Public Campaigns</td>
                            <td id="count">{{ platform_statistics.active_public_campaigns }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">5</td>
                            <td id="measure">Total Number Of Active Private Campaigns</td>
                            <td id="count">{{ platform_statistics.active_private_campaigns }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">6</td>
                            <td id="measure">Total Number Of Ad Requests Shared</td>
                            <td id="count">{{ platform_statistics.total_adrequests }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">7</td>
                            <td id="measure">Total Number Of Pending Ad Requests</td>
                            <td id="count">{{ platform_statistics.total_pending_adrequests }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">8</td>
                            <td id="measure">Total Number Of Accepted Ad Requests</td>
                            <td id="count">{{ platform_statistics.total_accepted_adrequests }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">9</td>
                            <td id="measure">Total Number Of Rejected Ad Requests</td>
                            <td id="count">{{ platform_statistics.total_rejected_adrequests }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">10</td>
                            <td id="measure">Total Number Of Flagged Sponsors</td>
                            <td id="count">{{ platform_statistics.total_flagged_sponsors }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">11</td>
                            <td id="measure">Total Number Of Flagged Influencers</td>
                            <td id="count">{{ platform_statistics.total_flagged_sponsors }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">12</td>
                            <td id="measure">Total Number Of Flagged Campaigns</td>
                            <td id="count">{{ platform_statistics.total_flagged_sponsors }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">13</td>
                            <td id="measure">Total Number Of Ad Requests sent by Sponsors</td>
                            <td id="count">{{ platform_statistics.adrequest_sent_by_sponsor }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">14</td>
                            <td id="measure">Total Number Of Ad Requests sent by Influencers</td>
                            <td id="count">{{ platform_statistics.adrequest_sent_by_influencer }}</td>
                        </tr>
                        <tr>
                            <td id="serial-number">15</td>
                            <td id="measure">Total Number Of Completed Campaigns</td>
                            <td id="count">{{ platform_statistics.completed_campaigns }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
    </div>
</template>

<script>

import axios from '../assets/axios.js';

export default {
    name: 'PlatformStatistics',
    data() {
        return {
            platform_statistics: {},
        };
    },
    created() {
        this.getPlatformStatistics();
    },
    methods: {
        async getPlatformStatistics() {
            try {
                const response = await axios.get('/admin/platform_statistics');
                this.platform_statistics = response.data.platform_statistics;
            } catch (error) {
                console.error('Error fetching platform statistics:', error.response ? error.response.data : error.message);
            }
        }
    }    
}
</script>

<style scoped>
.platform-statistics {
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
.table-container {
    padding-left: 100px;
    padding-right: 100px;
    width: 100%;
    text-align: center;
}
#serial-number {
    font-size: x-large;
    vertical-align: middle;
}
#measure {
    font-size: larger;
    text-align: left;
    vertical-align: middle;
}
#count {
    font-size: 4em;
    text-align: center;
    font-weight: bolder;
    vertical-align: middle;
    color: #F4A261;
}
</style>
