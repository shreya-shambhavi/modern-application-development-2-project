<template>
  <nav id="navbar" class="navbar navbar-expand-lg">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand" id="navbar-brand">Influencer Engagement and Sponsorship Coordination Platform</router-link>
      <div class="ms-auto d-flex">
        <router-link to="/user/registration"><button id="buttonset" type="button" class="btn">Register</button></router-link>
        <router-link to="/user/login"><button id="buttonset" type="button" class="btn">Login</button></router-link>
      </div>
    </div>
  </nav>
  <div class="home">
    <div>
      <h1>"Fusing Brands with Influential Voices"</h1>
      <p>Our platform is designed to bridge the gap between brands and influencers, creating seamless partnerships that drive results. Whether you're a brand looking to expand your reach or an influencer seeking new opportunities, our platform provides the tools and support you need to succeed.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 225px;
  margin-bottom: 225px;
  padding-left: 50px;
  padding-right: 50px;
}
h1 {
  font-size: 3.5em;
  text-align: center;
  font-weight: bolder;
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
#navbar {
  background-color: #284B63;
}
#navbar-brand {
  color: #FFFFFF;
  font-weight: bold;
}
#buttonset {
  color: #FFFFFF;
  font-weight: bold;
  font-size: large;
}
</style>
