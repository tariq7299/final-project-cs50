<template>

    <div class="view-container">
        
    
    <Header class="sector" pageTitle="Log In"></Header>

    <v-form @submit.prevent="login" class="formTest">

        <v-text-field v-model="username" class="input" id="user-name" name="user-name" placeholder="Type a username for you account..." label="username" type="text" prepend-icon="mdi-account" variant="outlined">
        </v-text-field>

        <v-text-field v-model="password" class="input" id="password" name="password" placeholder="Type a password for your account..." label="Password" type="password" prepend-icon="mdi-account" variant="outlined" autocomplete="false">
        </v-text-field>

        <v-btn class="" type="submit">Log in</v-btn>
        
    </v-form>

    <p>{{ console.log(username) }}</p>
    <p>{{ console.log(password) }}</p>

    </div>
</template>

<script>
    import { Alert } from 'bootstrap';
import Header from './../components/Header'
    import axios from 'axios'

    export default {
    name: 'Login',

    data () {
        return {
            username: '',
            password: '',
        }
    },

    components: {
        Header,
    },
    methods: {
        async login() {
            const apiUrl = process.env.VUE_APP_API_BASE_URL;
            const path = apiUrl + '/login';

            const requestData = {
                username: this.username,
                password: this.password,
            };

            axios

                .post(path, requestData, { withCredentials: true })

                .then((response) => {
                    if (response.status === 200 && response.data.success) {
                        // Redirect the user to the home page
                        this.$router.push({ name: 'Home' });
                    }
                })
                .catch((error) => {
                    if (error.response) {
                        console.error(error);
                        // The request was made, and the server responded with a non-2xx status code
                        // Handle the error based on the HTTP status code and error message
                        const status = error.response.status;
                        const message = error.response.data.error_message;
                        alert(`Error! Status: ${status}, Message: ${message}`);
                        this.loading = false; // Set loading to false in case of an error
                    } else if (error.request) {
                        console.error(error);
                        // The request was made, but no response was received
                        alert('Error! No response received from the server. Please try again or contact support for assistance.');
                        this.loading = false; // Set loading to false in case of an error
                    } else {
                        console.error(error);
                        // Something else happened while setting up the request
                        alert(`Oops! Something went wrong while fetch your expenses. Please try again or contact support for assistance.`);
                        this.loading = false; // Set loading to false in case of an error
                    }
                });
        },
        clearAllSessions() {
            try {
                const apiUrl = process.env.VUE_APP_API_BASE_URL;

                const path = apiUrl + '/logout';

                axios.get(path, { withCredentials: true });
                
            }   catch (error) {
                console.error(error);
                alert(`Oops! Something went wrong. Please try again or contact support for assistance. Error message: ${error}`);
            }
        }
    },
    created() {
        this.clearAllSessions()
    }

    }
</script>

<style scoped>

.input {
    width: 100%;
}
</style>