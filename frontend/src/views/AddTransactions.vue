
<template>
   <div>
      <NavBar></NavBar>

      <div class="add-expenses">
  
        <div class="alert" v-show="successAlertFound" >
              <v-alert type="success" title="Success" :text="alertMessage" variant="tonal">
              </v-alert>
          </div>
          <div class="alert" v-show="errorAlertFound">
              <v-alert type="error" title="Error" :text="alertMessage" variant="tonal">
              </v-alert>
          </div>
  
    
        <!-- '.sector' class just applies a 'margin-bottom', and it is defined globally in 'App.vue', to make consistent spacing between sectors/sections -->
        <Header class="sector" pageTitle="Add Transactions"></Header>
    
        <!-- .prevent modifier is used to prevent the default behavior of the form submission, which is to reload the page. -->
          <v-form @submit.prevent="addTransaction" class="formTest">
      
              <!-- 
                  "@click:clear" : This becasue the clear symbol of the v-text-field doesn't clear the input of user, so i had to manually clear it by @click event 
                  I couldn't set "label:'Date'", and I had to use v-binf on it :label="formattedDate", because if I used the latter method "label" will block ':value="formattedDate"' from appearing in the input field !
              -->
              <v-text-field class="expense-input"  :model-value="formattedDate" clearable prepend-icon="mdi-calendar" placeholder="For example : 2023-02-07" @click:clear="selectedDate = null" @keydown.delete="handleDelete" label="Transaction Date"> 
          
                  <!-- 
                  I have used v-model="menu" and :close-on-content-click="false" in order to prevent the datePicker from disappearing after I click on a date, as this is the default behavior of 'v-menu' nested elements. However, this default behavior is interfering with the functionality of the datepicker.
                  -->
                  <v-menu activator="parent" v-model="menu" :close-on-content-click="false" height="550" class="veutify-menu">
          
                  <!--@click:save="menu = false" @click:cancel="menu = false" : Are used to a make v-menu closes only when I press 'OK' or 'CANCEL'   -->
                  <v-date-picker v-model="selectedDate" @click:save="menu = false" @click:cancel="menu = false"></v-date-picker>
          
                  </v-menu>
          
              </v-text-field>
  
              <v-text-field v-model="amount" name="amount-spent" id="amount_spent" placeholder="Enter Amount"
              autofocus label="Deal Amount" prepend-icon="mdi-cash" class="expense-input" clearable>
              </v-text-field>
  
  
                  <div class="contacts-drop-down-wrapper">       
                               
                          <v-select v-model="selectedContact" name="contact" id="contact" label="Contact" prepend-icon="mdi-account-box" :items="contacts" item-title="contact_name" item-value="contact_phone" class="expense-input" clearable :hint="phoneNumber">
                          </v-select>
  
                      <div class="new-contact-btn-wrapper">
                          <router-link to="/add-new-contact"><v-btn class="new-contact-bnt"><span>Add New</span></v-btn></router-link> 
                      </div>
                  </div>

                    <v-radio-group v-model="debtOrCredit" class="debt-credit-container" inline  >
                       <v-row>
                         <v-col cols="12" sm="6" align="start" class="pa-0">
                           <v-radio value="-" color="red" class="radio-button " >
                             <template v-slot:label>
                               <div><strong class="text-error">Debt</strong> (I need to pay to)</div>
                             </template>
                           </v-radio>
                         </v-col>
                         <v-col cols="12" sm="6" align="start" class="pa-0">
                           <v-radio value="+" color="green" class="radio-button" >
                           <template v-slot:label>
                             <div><strong class="text-success">Credit</strong> (I need to collect)</div>
                           </template>
                         </v-radio>
                         </v-col>
                       </v-row>
                    </v-radio-group>

              <v-text-field v-model="transactionNote" name="expense-note" id="expense-note" placeholder="Type a note" label="Note" prepend-icon="mdi-note" class="expense-input" type="text">
              </v-text-field>
              
              <v-btn class="" type="submit" id="button">Add Transaction</v-btn>
              
        </v-form>
  
      </div>
    
    </div>
  
  </template>
  
  <script scoped>
    import axios from 'axios'
    import Header from './../components/Header'
  
    // Some important notes about that JS file found inside !
    import './../../public/passive-event-notoriousBug.js';
  
    import { VDatePicker } from 'vuetify/labs/VDatePicker'
    import { format } from 'date-fns';
  
    export default {
        name: 'AddTransactions',
        data () {
            return {
                successAlertFound: false,
                errorAlertFound: false,
                alertMessage: '',
                amount:'',
                contacts: [],
                selectedContact: '',
                calendarData: {},
                transactionNote: null,
                selectedDate: new Date(),
                menu: false,
                debtOrCredit: ''
            }
        },
        components: {
          VDatePicker,
          Header,
        },
        methods: {
  
            async  fetchContacts () {
                try {

                        const apiUrl = process.env.VUE_APP_API_BASE_URL;

                        const path = apiUrl + '/new-transactions';

                        const response = await axios.get(path, { withCredentials: true });
                        
                        if (response.data.userNotLogged) {
                            this.$router.push({ name: 'login' });
                            return
                        }
  
                        this.contacts = response.data.contacts
  
                    }   catch (error) {
                        console.error('Error fetching data:', error);
                    }
                },
  
           
            addTransaction() {

                const apiUrl = process.env.VUE_APP_API_BASE_URL;

                const path = apiUrl + '/new-transactions';
  
                axios
                    .post(path, {
                      successAlertFound: false,
                      errorAlertFound: false,
                      alertMessage: '',
                        selectedYear: this.selectedYear,
                        selectedMonth: this.selectedMonth,
                        selectedDay: this.selectedDay,
                        submittedAmount: this.amount,
                        singedAmount: this.singedAmount,
                        newContactPhone: this.selectedContact,
                        transactionNote: this.transactionNote
                        
                    }, { withCredentials: true })
                    .then((response) => {

                        if (response.data.userNotLogged) {
                            this.$router.push({ name: 'login' });
                            return
                        }
  
                        // Handle success response
                        const submittedAmount = response.data.submittedAmount;
                        const submittedContactName = response.data.submittedContactName;

                        this.errorAlertFound = false
                        this.successAlertFound = true

                        if (this.singedAmount.includes('-')) {
                          this.alertMessage = `Transaction successfull ! A debt of value ${this.amount} owed to ${submittedContactName}has been added to your aacount`
                        } else {
                          this.alertMessage = `Transaction successfull ! A credit of value ${this.amount} owed to you by ${submittedContactName} has been added to your aacount`
                        }
                        
                    })
                    .catch((error) => {
                        if (error.response) {
                            // The request was made, and the server responded with a non-2xx status code
                            // Handle the error based on the HTTP status code and error message
                            this.successAlertFound = false
                            this.errorAlertFound = true
                            this.alertMessage = error.response.data.error_message
                        } else if (error.request) {
                            // The request was made, but no response was received
                            this.successAlertFound = false
                            this.errorAlertFound = true
                            this.alertMessage = 'Error! No response received from the server. Please try again or contact support for assistance.'
                        } else {
                            // Something else happened while setting up the request
                            this.successAlertFound = false
                            this.errorAlertFound = true
                            this.alertMessage = `Oops! Something went wrong while adding the expense. Please try again or contact support for assistance.`
                        }
                    });
            },
            handleDelete() {
        this.selectedDate = null;
        
      },
        },
        computed: {
  
          formattedDate () {
            const formattedDate = this.selectedDate ? format(this.selectedDate, 'EEEE, dd MMM, yyyy') : format(new Date(), 'EEEE, dd MMM, yyyy')
          return formattedDate
          },

          selectedYear () {
           
            return this.selectedDate ? this.selectedDate.getFullYear() : ''
          },
          selectedMonth () {
           
            return this.selectedDate ? this.selectedDate.getMonth()+1 : ''
          },
          selectedDay () {
            
            return this.selectedDate ? this.selectedDate.getDate() : ''
          },
          phoneNumber () {
            return this.selectedContact ? 'Phone Number - ' + this.selectedContact : ''
          },
          singedAmount() {
            
            return this.debtOrCredit + this.amount
          }
  
    },
        created() {
            this.fetchContacts()
        },
    }
  </script>
  
  <style>
  
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

  .contacts-drop-down-wrapper {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 10px

  }

  
    .expense-input {
        width: 100%;
    }
    
    #contact{
        font-size: small;
        flex: 1 1 auto;
    }

    .new-contact-btn-wrapper {
        padding: 10px 0 10px 0;
        flex:0 1 auto;
        
    }
    
    .new-contact-bnt span {
        font-size: 10px;
        white-space: normal;
        word-wrap: break-word;
        font-weight: 600;
        color: green;
        /* width: 100px; */
    }

   
    .debt-credit-container{
      width: 70%;
    }

  
  </style>