<template>
    <div>

        <NavBar></NavBar>
        <div class="view-container" >
    
            <FlashMessage type="success" title="Success" :text="alertMessage" v-show="successAlertFound"></FlashMessage>
        <FlashMessage type="error" title="Error" :text="alertMessage" v-show="errorAlertFound"></FlashMessage>

    
    
            <Header class="sector" pageTitle="Log In"></Header>
    
            <v-form @submit.prevent="login" class="formTest">
    
            <v-text-field v-model="username" class="input" id="user-name" name="user-name" placeholder="Type a username for you account..." label="username" type="text" prepend-icon="mdi-account" variant="outlined">
            </v-text-field>
    
            <v-text-field v-model="password" class="input" id="password" name="password" placeholder="Type a password for your account..." label="Password" type="password" prepend-icon="mdi-lock" variant="outlined" autocomplete="false">
            </v-text-field>
    
            <v-btn class="" type="submit">Log in</v-btn>
            
        </v-form>
    
        </div>
    </div>
</template>

<script>
    import Header from './../components/Header'
    import axios from 'axios'

    export default {
    name: 'Login',

    data () {
        return {
            successAlertFound: false,
            errorAlertFound: false,
            alertMessage: '',
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
                        this.successAlertFound = false
                        this.errorAlertFound = true
                        this.alertMessage = error.response.data.error_message
                    } else if (error.request) {
                        console.error(error);
                        // The request was made, but no response was received
                        this.successAlertFound = false
                        this.errorAlertFound = true
                        // The request was made, but no response was received
                        this.alertMessage = 'Error! No response received from the server. Please try again or contact support for assistance.'
                    } else {
                        this.successAlertFound = false
                        this.errorAlertFound = true
                        this.alertMessage = `Oops! Something went wrong while adding the expense. Please try again or contact support for assistance.`
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
        },
        showAlertMessageAfterRouting() {
            if (this.$route.params.status === 'success') {
        this.errorAlertFound = false
        this.successAlertFound=true;
        return this.alertMessage = this.$route.params.message   
    }
        }
    },
    created() {
        this.clearAllSessions();
    },
    mounted() {
        this.showAlertMessageAfterRouting();
    }

    }
</script>

<style scoped>

.input {
    width: 100%;
}

</style>