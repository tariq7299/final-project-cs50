
<template>
    <div class="add-expenses">
  
      <!-- '.sector' class just applies a 'margin-bottom', and it is defined globally in 'App.vue', to make consistent spacing between sectors/sections -->
      <Header class="sector" pageTitle="Add New Contact"></Header>
  
      <!-- .prevent modifier is used to prevent the default behavior of the form submission, which is to reload the page. -->
        <v-form @submit.prevent="addNewContact" class="formTest">
    
          
    
              <v-text-field v-model="contactName" name="amount-spent" id="amount_spent" placeholder="Enter Contact Name"
              autofocus label="Contact Name" prepend-icon="mdi-account-box" class="input" clearable>
              </v-text-field>
              
              <v-text-field v-model="contactPhone" name="expense-note" id="expense-note" placeholder="Enter Contact Phone Number"
              label="Contact Phone" prepend-icon="mdi-card-account-phone" class="input">
              </v-text-field>
              
              <v-btn class="" type="submit" id="button">Add Contact</v-btn>
            
      </v-form>
            
    </div>
  
  
  </template>
  
  <script>
    import axios from 'axios'
    import Header from './../components/Header'
    
    export default {
        name: 'AddNewContact',
        data () {
            return {
                contactName:'',
                contactPhone: '',
            }
        },
      //   data: () => ({
      //   selectedDate: null,
      //   menu: false,
      // }),
        components: {
          Header,
        },
        methods: {
  
            addNewContact() {

                const apiUrl = process.env.VUE_APP_API_BASE_URL;

                const path = apiUrl + '/new-contact';
  
                axios
                    .post(path, {
                        contactName: this.contactName,
                        contactPhone: this.contactPhone
                    })
                    .then((response) => {
  
                        // Handle success response
                        const newContactName = response.data.newContactName;
                        const newContactPhone = response.data.newContactPhone;
                        
                        alert(`Success! ${newContactName} with phone ${newContactPhone} has been added to your contacts`);
                    })
                    .catch((error) => {
                        if (error.response) {
                            // The request was made, and the server responded with a non-2xx status code
                            // Handle the error based on the HTTP status code and error message
                            const status = error.response.status;
                            const message = error.response.data.error_message;
                            alert(`Error! Status: ${status}, Message: ${message}`);
                        } else if (error.request) {
                            // The request was made, but no response was received
                            alert('Error! No response received from the server. Please try again or contact support for assistance.');
                        } else {
                            // Something else happened while setting up the request
                            alert(`Oops! Something went wrong while adding the expense. Please try again or contact support for assistance.`);
                        }
                    });
            },
            handleDelete() {
        this.selectedDate = null;
        
      },
        },
        computed: {
  
          formattedDate () {
            const formattedDate = format(this.selectedDate, 'EEEE, dd MMM, yyyy')
            return formattedDate
          },
  
          selectedYear () {
            return this.selectedDate.getFullYear()
          },
          selectedMonth () {
            return this.selectedDate.getMonth() + 1
          },
          selectedDay () {
            return this.selectedDate.getDate()
          }
  
    },
        created() {
            // this.fetchContacts()
        },
    }
  </script>
  
  <style scoped>
  
  .add-expenses {
    height: 100vh;
    width: 90vw;
    max-width: 800px;
    margin: auto;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: start;
    flex-direction: column;
  }
  
  .formTest{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    
  }
  
    .input{
        width: 100%;
    }
    
    

    /* @media (max-width: 450px) and (orientation: portrait) {

    .add-expenses {
    height: 100vh;
    width: 90vw;
    max-width: 300px;
    margin: auto;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: start;
    flex-direction: column;
  }
    } */
  </style>