<template>

    <nav id="navbar" class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand" id="navbar-brand">Influencer Engagement and Sponsorship Coordination Platform</router-link>
        <div class="ms-auto d-flex">
            <router-link to="/user/registration"><button id="registerbutton" type="button" class="btn">Register</button></router-link>
        </div>
        </div>
    </nav>

    <div class = "login">

        <div id = "card" class = "card shadow p-5 border rounded-3">

            <h1 class = "card-title text-center mb-4"><b>USER LOGIN</b></h1>

            <div class = "form-group mb-3">
                <label for = "username" class = "mb-2">Username</label>
                <input v-model = "username" type = "name" class = "form-control" required>
            </div>

            <div class = "form-group mb-4">
                <label for = "password" class = "mb-2">Password</label>
                <input v-model = "password" type = "password" class = "form-control" required/>
            </div>

            <div class = "mt-2">
                <button class = "btn btn-primary w-100" @click = "LoginUser">Login</button>
            </div>

        </div>
    </div>
    
</template>

<script>

import { mapActions } from 'vuex'

export default {
    name: 'LoginView',
    data() {
        return {
        username: "",
        password: "",
        }
    },
    methods: {
        ...mapActions(['login']),
        async LoginUser() {
            try {
                const userData = await this.login({ username: this.username, password: this.password });
                await this.redirectUser(userData.role);
            } catch (error) {
                if (error.response && error.response.status === 403) {

                    if (error.response.data.message === "Your Account is not yet approved by Admin.") {
                        console.log("Your Account is not yet approved by Admin.");
                        alert("Your Account is not yet approved by Admin.");
                    } else {
                        console.log("Login Failed : ", error);
                        alert("Login Failed. Please Check Your Credentials.");
                    }

                } else if (error.response && error.response.status === 400) {

                    if (error.response.data.message === "Invalid Login! User doesn't exist!") {
                        console.log("Invalid Login! User doesn't exist!");
                        alert("User Doesn't Exist. Kindly Register.");
                    } else if (error.response.data.message === "Wrong Password") {
                        console.log("Wrong Password");
                        alert("Please Check Your Password.");
                    } else {
                        console.log("Login Failed : ", error);
                        alert("Login Failed. Please Check Your Credentials.");
                    }

                } else {
                    console.log("Login Failed : ", error);
                    alert("Login Failed. Please Check Your Credentials.");
                }
            }
        },
        async redirectUser(role) {
            try {
                if (role === "Admin") {
                    this.$router.push("/admin/dashboard");
                } else if (role === "Influencer") {
                    this.$router.push("/influencer/dashboard/");
                } else if (role === "Sponsor") {
                    this.$router.push("/sponsor/dashboard/");
                } else {
                    console.error("No Matching Role Found");
                }
            } catch (error) {
                console.error("Error Redirecting User : ", error);
                alert("Error Redirecting User");
            }
        }
    }
}
</script>

<style scoped>
.login {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #D9D9D9;
}
#card {
    width: 700px;
    height: 400px;
    margin: 100px;
    color: #353535;
}
#navbar {
  background-color: #284B63;
}
#navbar-brand {
  color: #FFFFFF;
  font-weight: bold;
}
#registerbutton {
  color: #FFFFFF;
  font-weight: bold;
  font-size: large;
}
h1 {
    font-weight: bold;
    font-size: 3em;
    color: #E76F51;
}
</style>
