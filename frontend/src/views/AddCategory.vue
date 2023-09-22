<template>
  
    <div class="add-new-category-container">
  
      <!-- '.sector' class just applies a 'margin-bottom', and it is defined globally in 'App.vue', to make consistent spacing between sectors/sections -->
      <Header class="sector" pageTitle="Add New Category"></Header>
  
      <!-- .prevent modifier is used to prevent the default behavior of the form submission, which is to reload the page. -->
        <v-form @submit.prevent="addNewCategory" class="formTest">
    
              <v-text-field v-model="category" name="category-input" id="category-input" placeholder="Enter Category Name"
              autofocus label="New Category Title" prepend-icon="mdi-account-box" class="input" clearable>
              </v-text-field>
              
              <v-btn class="" type="submit" id="button">Add Category</v-btn>
            
      </v-form>
            
    </div>
  
  
  </template>
  
  <script>
    import axios from 'axios'
    import Header from './../components/Header'
    
    export default {
        name: 'AddNewCategory',
        data () {
            return {
                category:'',
            }
        },
        components: {
          Header,
        },
        methods: {
  
            addNewCategory() {

                const apiUrl = process.env.VUE_APP_API_BASE_URL;

                const path = apiUrl + '/new-contact';
  
                axios
                    .post(path, {
                        category: this.category,
                    }, { withCredentials: true })
                    .then((response) => {
                        
                        if (response.data.userNotLogged) {
                            this.$router.push({ name: 'login' });
                            return
                        }
  
                        // Handle success response
                        const newCategory = response.data.newCategory;
                        
                        alert(`Success! ${newCategory} has been added to your categories`);
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
        
    }
  </script>
  
  <style scoped>
  
  .add-new-category-container {
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

    .add-new-category-container {
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