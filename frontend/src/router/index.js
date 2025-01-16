import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

// Public views
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import UnauthorizedView from '@/views/UnauthorizedView.vue'

// Admin views
import AdminDashboard from '@/views/AdminDashboard.vue'
import NewSponsors from '@/views/NewSponsors.vue'
import AllInfluencers from '@/views/AllInfluencers.vue'
import AllSponsors from '@/views/AllSponsors.vue'
import AllCampaigns from '@/views/AllCampaigns.vue'
import AllAdRequests from '@/views/AllAdRequests.vue'
import FlaggedInfluencers from '@/views/FlaggedInfluencers.vue'
import FlaggedSponsors from '@/views/FlaggedSponsors.vue'
import FlaggedCampaigns from '@/views/FlaggedCampaigns.vue'
import PlatformStatistics from '@/views/PlatformStatistics.vue'

// Influencer views
import InfluencerDashboard from '@/views/InfluencerDashboard.vue'
import InfluencerProfile from '@/views/InfluencerProfile.vue'
import InfluencerTasks from '@/views/InfluencerTasks.vue'
import InfluencerCompletedTasks from '@/views/InfluencerCompletedTasks.vue'
import PublicCampaigns from '@/views/PublicCampaigns.vue'
import InfluencerNewRequests from '@/views/InfluencerNewRequests.vue'
import InfluencerSentRequests from '@/views/InfluencerSentRequests.vue'
import InfluencerRequestsDirectory from '@/views/InfluencerRequestsDirectory.vue'

// Sponsor views
import SponsorDashboard from '@/views/SponsorDashboard.vue'
import SponsorProfile from '@/views/SponsorProfile.vue'
import MyCampaigns from '@/views/MyCampaigns.vue'
import MonitorTasks from '@/views/MonitorTasks.vue'
import MonitorCompletedTasks from '@/views/MonitorCompletedTasks.vue'
import PlatformInfluencers from '@/views/PlatformInfluencers.vue'
import SponsorNewRequests from '@/views/SponsorNewRequests.vue'
import SponsorSentRequests from '@/views/SponsorSentRequests.vue'
import SponsorRequestsDirectory from '@/views/SponsorRequestsDirectory.vue'

// CRUD views
import SponsorDetails from '@/views/SponsorDetails.vue'
import InfluencerDetails from '@/views/InfluencerDetails.vue'
import CampaignDetails from '@/views/CampaignDetails.vue'
import AdrequestDetails from '@/views/AdrequestDetails.vue'
import CreateCampaign from '@/views/CreateCampaign.vue'
import InfluencerCreateAdrequest from '@/views/InfluencerCreateAdrequest.vue'
import SponsorCreateAdrequest from '@/views/SponsorCreateAdrequest.vue'
import InfluencerUpdate from '@/views/InfluencerUpdate.vue'
import SponsorUpdate from '@/views/SponsorUpdate.vue'
import UpdateCampaign from '@/views/UpdateCampaign.vue'
import InfluencerUpdateAdrequest from '@/views/InfluencerUpdateAdrequest.vue'
import SponsorUpdateAdrequest from '@/views/SponsorUpdateAdrequest.vue'

// Search views
import SearchInfluencers from '@/views/SearchInfluencers.vue'
import SearchCampaigns from '@/views/SearchCampaigns.vue'


const routes = [
  { path: '/',name: 'Home', component : HomeView },
  { path: '/user/login', name: 'Login', component : LoginView },
  { path: '/user/registration', name: 'Register', component : RegisterView },
  { path: '/unauthorized', name: 'Unauthorized', component : UnauthorizedView },

  { 
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component : AdminDashboard,
    meta: { requiresAuth: true, role: 'Admin' },
    children: [
      { path: 'sponsors/new', name: 'NewSponsors', component : NewSponsors },
      { path: 'influencers/all', name: 'AllInfluencers', component : AllInfluencers },
      { path: 'sponsors/all', name: 'AllSponsors', component : AllSponsors },
      { path: 'campaigns/all', name: 'AllCampaigns', component : AllCampaigns },
      { path: 'adrequests/all', name: 'AllAdrequests', component : AllAdRequests },
      { path: 'influencers/flagged', name: 'FlaggedInfluencers', component : FlaggedInfluencers },
      { path: 'sponsors/flagged', name: 'FlaggedSponsors', component : FlaggedSponsors },
      { path: 'campaigns/flagged', name: 'FlaggedCampaigns', component : FlaggedCampaigns },
      { path: 'platform/statistics', name: 'PlatformStatistics', component : PlatformStatistics },

      { path: 'sponsor/details/:id', name: 'AdminViewSponsorDetails', component : SponsorDetails, props: true },
      { path: 'influencer/details/:id', name: 'AdminViewInfluencerDetails', component : InfluencerDetails, props: true },
      { path: 'campaign/details/:id', name: 'AdminViewCampaignDetails', component : CampaignDetails, props: true },
      { path: 'adrequest/details/:id', name: 'AdminViewAdrequestDetails', component : AdrequestDetails, props: true },
    ]
  },

  { 
    path: '/influencer/dashboard/',
    name: 'InfluencerDashboard',
    component : InfluencerDashboard,
    meta: { requiresAuth: true, role: 'Influencer' },
    children: [
      { path: 'profile', name: 'InfluencerProfile', component : InfluencerProfile },
      { path: 'tasks/active', name: 'InfluencerActiveTasks', component : InfluencerTasks },
      { path: 'tasks/completed', name: 'InfluencerCompletedTasks', component : InfluencerCompletedTasks },
      { path: 'campaigns/public', name: 'PublicCampaigns', component : PublicCampaigns },
      { path: 'requests/recieved', name: 'InfluencerNewRequests', component : InfluencerNewRequests },
      { path: 'requests/sent', name: 'InfluencerSentRequests', component : InfluencerSentRequests },
      { path: 'requests/directory', name: 'InfluencerRequestsDirectory', component : InfluencerRequestsDirectory },
      { path: 'search/campaigns', name: 'InfluencerSearchCampaigns', component : SearchCampaigns },

      { path: 'create/adrequest/:id', name: 'InfluencerCreateAdrequest', component : InfluencerCreateAdrequest, props: true },
      { path: 'profile/update/:id', name: 'InfluencerProfileUpdate', component : InfluencerUpdate, props: true },
      { path: 'update/adrequest/:id', name: 'InfluencerUpdateAdrequest', component :  InfluencerUpdateAdrequest, props: true },

      { path: 'sponsor/details/:id', name: 'InfluencerViewSponsorDetails', component : SponsorDetails, props: true },
      { path: 'influencer/details/:id', name: 'InfluencerViewInfluencerDetails', component : InfluencerDetails, props: true },
      { path: 'campaign/details/:id', name: 'InfluencerViewCampaignDetails', component : CampaignDetails, props: true },
      { path: 'adrequest/details/:id', name: 'InfluencerViewAdrequestDetails', component : AdrequestDetails, props: true },
    ]
  },

  {
    path: '/sponsor/dashboard/',
    name: 'SponsorDashboard',
    component : SponsorDashboard,
    meta: { requiresAuth: true, role: 'Sponsor' },
    children: [
      { path: 'profile', name: 'SponsorProfile', component : SponsorProfile },
      { path: 'mycampaigns', name: 'MyCampaigns', component : MyCampaigns },
      { path: 'monitor/tasks/active', name: 'MonitorTasks', component : MonitorTasks },
      { path: 'review/tasks/completed', name: 'ReviewCompletedTasks', component : MonitorCompletedTasks },
      { path: 'find/influencers', name: 'PlatformInfluencers', component : PlatformInfluencers },
      { path: 'requests/recieved', name: 'SponsorNewRequests', component : SponsorNewRequests },
      { path: 'requests/sent', name: 'SponsorSentRequests', component : SponsorSentRequests },
      { path: 'requests/directory', name: 'SponsorRequestsDirectory', component : SponsorRequestsDirectory },
      { path: 'search/influencers', name: 'SponsorSearchInfluencers', component : SearchInfluencers },

      { path: 'create/campaign/:id', name: 'CreateCampaign', component : CreateCampaign, props: true },
      { path: 'create/adrequest/:id', name: 'SponsorCreateAdrequest', component: SponsorCreateAdrequest, props: route => ({ id: route.params.id, type: route.query.type }) },
      { path: 'profile/update/:id', name: 'SponsorProfileUpdate', component : SponsorUpdate, props: true },
      { path: 'update/campaign/:id', name: 'SponsorUpdateCampaign', component :  UpdateCampaign, props: true },
      { path: 'update/adrequest/:id', name: 'SponsorUpdateAdrequest', component : SponsorUpdateAdrequest, props: true },

      { path: 'sponsor/details/:id', name: 'SponsorViewSponsorDetails', component : SponsorDetails, props: true },
      { path: 'influencer/details/:id', name: 'SponsorViewInfluencerDetails', component : InfluencerDetails, props: true },
      { path: 'campaign/details/:id', name: 'SponsorViewCampaignDetails', component : CampaignDetails, props: true },
      { path: 'adrequest/details/:id', name: 'SponsorViewAdrequestDetails', component : AdrequestDetails, props: true },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters.isLoggedIn;
  const userRole = store.getters.userRole;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      next({ name: 'Login' });
    } else {
      if (to.matched.some(record => record.meta.role)) {
        if (userRole === to.meta.role) {
          next();
        } else {
          next({name: 'Unauthorized'});
        }
      } else {
        next();
      }
    }
  } else {
    next();
  }
});

export default router

