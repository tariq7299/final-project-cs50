<template>

    <div class="view-container">
        
    
    <Header class="sector" pageTitle="Register"></Header>

    <v-form @submit.prevent="registerUser" class="formTest">

        <v-text-field v-model="firstName" autofocus class="input" id="first-name" name="first-name" placeholder="Type your first name..." label="First Name" type="text" prepend-icon="mdi-account" variant="outlined" >
        </v-text-field>

        <v-text-field v-model="lastName" class="input" id="last-name" name="last-name" placeholder="Type your last name..." label="Last Name" type="text" prepend-icon="mdi-account" variant="outlined">
        </v-text-field>

        <v-text-field v-model="username" class="input" id="user-name" name="user-name" placeholder="Type a username for you account..." label="username" type="text" prepend-icon="mdi-account" variant="outlined">
        </v-text-field>

        <v-text-field v-model="email" class="input" id="email" name="email" placeholder="Type your email..." label="Email" type="email" prepend-icon="mdi-account" variant="outlined">
        </v-text-field>

        <v-text-field v-model="password" class="input" id="password" name="password" placeholder="Type a password for your account..." label="Password" type="password" prepend-icon="mdi-account" variant="outlined" autocomplete="false">
        </v-text-field>

        <v-text-field v-model="passwordConfirm" class="input" id="confirm-password" name="confirm-password" placeholder="Type your password again..." label="Confirm password" type="password" prepend-icon="mdi-account" variant="outlined" autocomplete="false">
        </v-text-field>

        
        <v-btn class="" type="submit">Register</v-btn>
        
    </v-form>
    <p>{{ console.log(firstName) }}</p>
    <p>{{ console.log(lastName) }}</p>
    <p>{{ console.log(username) }}</p>
    <p>{{ console.log(email) }}</p>
    <p>{{ console.log(password) }}</p>
    <p>{{ console.log(passwordConfirm) }}</p>

    </div>
</template>

<script>
    import Header from './../components/Header'
    import axios from 'axios'

    export default {
    name: 'Register',

    data () {
        return {
            firstName: '',
            lastName: '',
            username: '',
            email: '',
            password: '',
            passwordConfirm: '',

        }
    },

    components: {
        Header,
    },
    methods: {
        async registerUser() {
            const apiUrl = process.env.VUE_APP_API_BASE_URL;
            const path = apiUrl + '/register_user';

            const requestData = {
                firstName: this.firstName,
                lastName: this.lastName,
                username: this.username,
                email: this.email,
                password: this.password,
                passwordConfirm: this.passwordConfirm
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

        }
    }

    }
</script>

<style scoped>

.input {
    width: 100%;
}
</style>