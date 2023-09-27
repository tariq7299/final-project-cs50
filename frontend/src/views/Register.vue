<template>
     <div>
      <NavBar></NavBar>

      <div class="view-container">
  
        <FlashMessage type="success" title="Success" :text="alertMessage" v-show="successAlertFound"></FlashMessage>
        <FlashMessage type="error" title="Error" :text="alertMessage" v-show="errorAlertFound"></FlashMessage>

          
      
      <Header class="sector" pageTitle="Register"></Header>
  
      <v-form @submit.prevent="registerUser" class="formTest">
  
          <v-text-field v-model="firstName" autofocus class="input" id="first-name" name="first-name" placeholder="Type your first name..." label="First Name" type="text" prepend-icon="mdi-account" variant="outlined" >
          </v-text-field>
  
          <v-text-field v-model="lastName" class="input" id="last-name" name="last-name" placeholder="Type your last name..." label="Last Name" type="text" prepend-icon="mdi-account" variant="outlined">
          </v-text-field>
  
          <v-text-field v-model="username" class="input" id="user-name" name="user-name" placeholder="Type a username for you account..." label="username" type="text" prepend-icon="mdi-badge-account" variant="outlined">
          </v-text-field>
  
          <v-text-field v-model="email" class="input" id="email" name="email" placeholder="Type your email..." label="Email" type="email" prepend-icon="mdi-at" variant="outlined">
          </v-text-field>
  
          <v-text-field v-model="password" class="input" id="password" name="password" placeholder="Type a password for your account..." label="Password" type="password" prepend-icon="mdi-lock" variant="outlined" autocomplete="false">
          </v-text-field>
  
          <v-text-field v-model="passwordConfirm" class="input" id="confirm-password" name="confirm-password" placeholder="Type your password again..." label="Confirm password" type="password" prepend-icon="mdi-lock" variant="outlined" autocomplete="false">
          </v-text-field>
  
          
          <v-btn class="" type="submit">Register</v-btn>
          
      </v-form>
      <p class="login-link">Already have an account? <a :href="loginUrl">Log in</a> </p>
      </div>
    </div>

</template>

<script>
    import Header from './../components/Header'
    import axios from 'axios'

    export default {
    name: 'Register',

    data () {
        return {                
            successAlertFound: false,
            errorAlertFound: false,
            alertMessage: '',
            firstName: '',
            lastName: '',
            username: '',
            email: '',
            password: '',
            passwordConfirm: '',
            alertMessage: '',
            showSuccessALert: false

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
                passwordConfirm: this.passwordConfirm,
            };

            axios

                .post(path, requestData, { withCredentials: true })

                .then((response) => {
                    if (response.status === 200 && response.data.success) {
                        // Redirect the user to the home page
                        this.$router.push({ name: 'login', params: {status: 'success', message:'Account has been created, Please Login !' } });
                        // alert('Success ! Account has been created, Please Login !');
                    }
                })
                .catch((error) => {
                    if (error.response) {

                        // The request was made, and the server responded with a non-2xx status code
                        // Handle the error based on the HTTP status code and error message

                        this.successAlertFound = false
                        this.errorAlertFound = true;
                        this.alertMessage = error.response.data.error_message

                        // alert(`Error! Status: ${status}, Message: ${message}`);
                    } else if (error.request) {
                        // The request was made, but no response was received
                        this.successAlertFound = false
                        this.errorAlertFound = true
                        // The request was made, but no response was received
                        this.alertMessage = 'Error! No response received from the server. Please try again or contact support for assistance.'
                    } else {
                        // Something else happened while setting up the request
                        this.successAlertFound = false
                        this.errorAlertFound = true
                        this.alertMessage = `Oops! Something went wrong while adding the expense. Please try again or contact support for assistance.`
                    }
                });
        }
    },
    computed: {
        loginUrl(){
        const frontendUrl = process.env.FORNTEND_BASE_URL;
        return frontendUrl + '/login';
      },
    }

    }
</script>

<style scoped>

.input {
    width: 100%;
}

.login-link {
    padding: 50px; 
}

</style>