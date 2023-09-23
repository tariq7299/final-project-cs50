
<template>
  <div class="add-expenses">

    <!-- '.sector' class just applies a 'margin-bottom', and it is defined globally in 'App.vue', to make consistent spacing between sectors/sections -->
    <Header class="sector" pageTitle="Add Expenses"></Header>

    <!-- .prevent modifier is used to prevent the default behavior of the form submission, which is to reload the page. -->
      <v-form @submit.prevent="addExpense" class="formTest">
  
        <!-- 
            "@click:clear" : This becasue the clear symbol of the v-text-field doesn't clear the input of user, so i had to manually clear it by @click event 
            I couldn't set "label:'Date'", and I had to use v-binf on it :label="formattedDate", because if I used the latter method "label" will block ':value="formattedDate"' from appearing in the input field !
        -->
        <v-text-field class="expense-input"  :model-value="formattedDate" clearable prepend-icon="mdi-calendar" placeholder="For example : 2023-02-07" @click:clear="selectedDate = null" @keydown.delete="handleDelete" :label="formattedDate"> 
  
          <!-- 
            I have used v-model="menu" and :close-on-content-click="false" in order to prevent the datePicker from disappearing after I click on a date, as this is the default behavior of 'v-menu' nested elements. However, this default behavior is interfering with the functionality of the datepicker.
           -->
          <v-menu activator="parent" v-model="menu" :close-on-content-click="false" height="550" class="veutify-menu">
  
            <!--@click:save="menu = false" @click:cancel="menu = false" : Are used to a make v-menu closes only when I press 'OK' or 'CANCEL'   -->
            <v-date-picker v-model="selectedDate" @click:save="menu = false" @click:cancel="menu = false"></v-date-picker>
  
          </v-menu>
  
        </v-text-field >
  
            <v-text-field v-model="amountSpent" name="amount-spent" id="amount_spent" placeholder="Enter Amount"
            autofocus label="Amount Spended" clearable prepend-icon="mdi-cash" class="expense-input">
            </v-text-field>


            <div class="contacts-drop-down-wrapper">      

              <v-select v-model="selectedCategoryId" name="category" id="category" label="Category" prepend-icon="mdi-notification-clear-all" :items="categories" item-title="category_name" item-value="category_id" class="expense-input" clearable>
              </v-select>

              <div class="new-category-btn-wrapper">
                  <router-link to="/add-category"><v-btn class="new-category-btn"><span>Add New</span></v-btn></router-link> 
              </div>
              
          </div>


            <v-text-field v-model="expenseNote" name="expense-note" id="expense-note" placeholder="Type a note"
            label="Note" clearable prepend-icon="mdi-note" class="expense-input">
            </v-text-field>
            
            <v-btn class="" type="submit" id="button">Add Expense</v-btn>
          
    </v-form>
          
  </div>


</template>

<script>
  import axios from 'axios'
  import Header from './../components/Header'

  // Some important notes about that JS file found inside !
  import './../../public/passive-event-notoriousBug.js';

  // import { FunctionalCalendar } from 'vue-functional-calendar';
  import { VDatePicker } from 'vuetify/labs/VDatePicker'
  import { format } from 'date-fns';

  export default {
      name: 'AddExpense',
      data () {
          return {
              amountSpent:'',
              categories: [],
              selectedCategoryId: null,
              calendarData: {},
              expenseNote: null,
              selectedDate: new Date(),
              menu: false,
          }
      },
    //   data: () => ({
    //   selectedDate: null,
    //   menu: false,
    // }),
      components: {
        VDatePicker,
        Header,
      },
      methods: {

          async  fetchYearsAndMonths () {
              try {
                      const apiUrl = process.env.VUE_APP_API_BASE_URL;

                      const path = apiUrl + '/get_calendar';

                      const response = await axios.get(path, { withCredentials: true });

                    if (response.data.userNotLogged) {
                      this.$router.push({ name: 'login' });
                      return
                    }

                      this.categories = response.data.categories

                  }   catch (error) {
                      console.error('Error fetching data:', error);
                  }
              },

         
          addExpense() {

                const apiUrl = process.env.VUE_APP_API_BASE_URL;

                const path = apiUrl + '/add_expenses';

              axios
                  .post(path, {
                      selectedYear: this.selectedYear,
                      selectedMonth: this.selectedMonth,
                      selectedDay: this.selectedDay,
                      amountSpent: this.amountSpent,
                      categoryId: this.selectedCategoryId,
                      expenseNote: this.expenseNote
                  }, { withCredentials: true })
                  .then((response) => {

                    if (response.data.userNotLogged) {
                      this.$router.push({ name: 'login' });
                      return
                    }
                      // Handle success response
                      const submitedAmountSpent = response.data.submitedAmountSpent;
                      const submitedCategory = response.data.submitedCategoryName;
                      
                      alert(`Success! ${submitedAmountSpent} has been added to your ${submitedCategory} expenses.`);
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
        }

  },
      created() {
          this.fetchYearsAndMonths()
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
    
    #category{
        font-size: small;
        flex: 1 1 auto;
    }

    .new-category-btn-wrapper {
        padding: 10px 0 10px 0;
        flex:0 1 auto;
        
    }
    
    .new-category-btn span {
        font-size: 10px;
        white-space: normal;
        word-wrap: break-word;
        font-weight: 600;
        color: green;
        /* width: 100px; */
    }
</style>