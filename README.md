# finale-project

## Project setup

```
vue create app # THis CLI command will init the project, and create all the necessary folders
vue add vutify # THis will add vutify library, as i used some of its componenets
npm install
npm install --save-dev dotenv-webpack # To be able to use env variables in vue
```

### Compiles and hot-reloads for development
```
# Due to the fact that this app uses CORS, you must set these three environment variables in the flask backend if you plan to authenticate users using the "Session-Authentication " approach.

SESSION_TYPE = 'filesystem'
SESSION_COOKIE_SECURE = True 
SESSION_COOKIE_SAMESITE = 'None' 

{ withCredentials: true } # Also include this in every axios request sent from frontend (Vue js) to backend (Flask)

npm run serve

```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Vue Configuration Reference](https://cli.vuejs.org/config/).
See [Flask Configuration Reference](https://flask.palletsprojects.com/en/2.3.x/config/)


# GoldGardyn The financial Progressive web app
## Video Demo:  [<URL HERE>](https://youtu.be/3CKUVbKEDsA)
## Description
- The application is called **GoldGardyn** and it's a finance app with two main functionalities:
    1. It calculates the user's expenses and spendings.
    2. It stores all the debts and credits of the user between him and other people/contacts.
- The main reason for creating this app is to help my brother, who is a small business owner. He needed an app or a spreadsheet to store and organize all his financial information, which he can access from any device. This inspired me to create this financial app. To make it more mobile-friendly and optimized for mobile phones, I decided to make it a Progressive Web App (PWA).
- The app is a Single Page Application (SPA) that uses Client-Side Rendering (CSR).
- Although the app is currently missing some features and needs some code cleaning, I'm aware of these issues and plan to continue developing and maintaining the app until it reaches a satisfactory point. After that, I will deploy it and continue maintaining it.
- In order to run the app you have to run the flask backend in port 8082, (or adjust the the `VUE_APP_API_BASE_URL` in .env found in *frontend/* folder), also run the frontend on port 8080 (or adjust the `FORNTEND_BASE_URL` found .env )

## Technologies Used
- Backend:
    - Flask
    - SQLite with SQLAlchemy as the ORM
    - Sessions for authentication
    - Implemented CSRF tokens for added security in validating user inputs
- Frontend:
    - Vue3
    - Vue Router
    - Vuetify
    - Bootstrap

## File and Folder Structure
- Backend:
  - The backend uses the Flask microframework.
  - Instead of using Flask's templating engine (Jinja), I used Vue3 to build the user interface.
  - Flask is used as an API to fetch data stored in my database.
  - Inside the `backend/` folder:
      - `app/` folder: Contains several files:
          - `queries/`: Contains any database queries used in `routes.py`. It holds two files:
            - `expenses_queries.py`: Holds the queries related to user expenses.
            - `users_queries.py`: Holds all the queries related to the user itself and his info, like `name`, `email`, etc.
          - `__init__.py`: Contains some initial configuration of my Flask app, like registering blueprints, CORS, and Session().
          - `helpers.py`: Contains some helper functions.
          - `models.py`: Contains the models of all my database tables.
          - `routes.py`: Contains all the routes of my app (All GET, POST requests coming from the client side).
      - Outside of `app/` but still inside `backend/`:
        - `run.py`: Responsible for running my app.
        - `test.py`: My lab, where it holds any code that I want to test or experiment with before actually implementing it into my app.

## Frontend Structure
- `public/` folder: Contains several files:
    - `index.html`: The main HTML file.
    - `additionalComments.md`: Contains additional comments about the project.
    - `passive-event-notoriousBug.js`: A JavaScript file that contains a function found on the internet that fixes a notorious bug.
- `src/` folder: Contains several sub-folders and files:
    - `components/` folder: Contains all of the frontend Vue.js components used in the app. Here's a quick overview of the main components:
        - `ChooseTimeFrame.vue`: Displays an accordion that shows a list of months and years that contain expenses. It fetches the expenses data in the most recent month of the most recent year (if the user didn't choose a month, if they did, then it will fetch the expenses data of the chosen month).
        - `MonthTimeFrame.vue`: Displays the current selected year and month of expenses, and a button that will show the accordion of `ChooseMonthTimeFrame.vue`.
        - `Day.vue`: Represents a particular day that contains user data. Each day is represented as a Bootstrap Accordion.
        - `Days.vue`: A parent component of `Day.vue`. It makes the days that contain user data more versatile and flexible to be reused in other components/views.
        - `Header.vue`: Contains the page title and is used in every view.
    - `views/` folder: Contains all of the frontend Vue.js views, which are navigated using Vue Router. Here's an overview of each view and its functionality:
        - `AddCategory.vue`: Contains a form that enables users to create a new custom-named category of expenses, instead of using default categories.
        - `AddExpenses.vue`: Contains a form that enables users to add a new expense on a particular date and choose a category to store that expense under.
        - `AddNewContact.vue`: Contains a form that enables users to add new contacts. These contacts will be used when users add transactions between themselves and these contacts.
        - `Contacts.vue`: Displays all transactions of all contacts.
        - `ContactHistory.vue`: Displays all past transactions that occurred between the user and this contact.
        - `Home.vue`: The home page of the app. It displays two main things: The user's wallet (his debt, credit, net balance) and his/her expenses.

# Notes on Vuetify in this Project
- After adding Vuetify, it overrides all the default styles of HTML elements. For example, there is a default `padding` in `<button>` tags. However, after adding Vuetify, this `padding` is removed. Therefore, you have to specify a custom `padding` in `<style>`. This applies to every element in the entire app.

# Some notes on branches
- First of all !, all of those branches is not fully working but rather it is some different versions of implementing some components and parts of the code   

## 'router-link' branch
*files to check **or** files that is relative*
- 'Home.vue'
- 'routes.js' 
- 'AddExpense'
- 'routes.py'
- 'MonthTimeFrame'

*What this branch does*
In this branch I have used `<router-link>` that belongs to vue js, by passing some varialbes in the defined route, and on the other side of route I extracted those variables from URL and used them in the page code

*How to see the changes*
- Just visit 'Add Expenses' link at the bottom of page in Home view  
- Understand what is going on in "AddExpense.vue" and 'Home.vue' and 'routes.js'

## 'monthTimeFrameBranch' branch
*files to check **or** files that is relative*
- 'MonthTimeFrame'
- 'routes.py'

*What this branch does*
In this branch I used different ways to view years and months, by using different methods to fetch spendings data in "methods" found in 'MonthTimeFrame.vue', that is different than what I am using right now in main branch, that is the only distict thing   

*How to see the changes*
- Visit Home page, look at the years and months selecet inputs
- Understand what is going on in "MonthTimeFrame.vue' and axios requests that sent back and fourth to the flask server in 'routes.py'
- All the main changes can be found in 'methods:' in 'MonthTimeFrame'
## 'monthTimeFrameBranch' branch
*files to check **or** files that is relative*
- 'MonthTimeFrame'
- 'routes.py'

*What this branch does*
In this branch I used different ways to view years and months, by using different methods to fetch spendings data in "methods" found in 'MonthTimeFrame.vue', that is different than what I am using right now in main branch, that is the only distict thing   

*How to see the changes*
- Visit Home page, look at the years and months selecet inputs
- Understand what is going on in "MonthTimeFrame.vue' and axios requests that sent back and fourth to the flask server in 'routes.py'
- All the main changes can be found in 'methods:' in 'MonthTimeFrame'  

## 'ChooseTimeFrame' branch 

*files to check **or** files that is relative*
- ChooseTimeFrame.veu

*What this branch does*
- I have written the years accordion in a different way, so I didn't use `v-show`, and `<TransitionGroup>`
- THere is a bug that I couldn't fix in that branch and that I occures when you try to click on/choose a month, and it actually works fine and preview the clkicked months's expenses, However, you have to diuble click it in order to apply styling and change its color.
I found out later after many mooons, that the `<input type="radio">` of months are confliction with `v-model` of veu.  
So when you click VEU js takes control and actually do his job, but fails in adding `checked` attribute to the seleced month radio input !.  

- Also in 'main' branch I have used a different method in styling and Implementing the accordion 

*How to see the changes*
- Visit Home page, and look at years and months accordion and try chooseing different year or a month, you will aslo notice that you have to double click the month in order to change its color.

## 'UserWallet' branch 

*files to check **or** files that is relative*
- routes.py (user_wallet())
- CurrentViewSummary.vue
- models.py (class UsersWallet)

*What this branch does*
- It is a different implementation of how I fetch users wallet info (things like balance, debt, credit)
- So in that 'UserWallet' branch i used to store each of wallet info as a column in db then I have discovered -hopfully- a better way !, and that by calculating the debt snd credit from transactions table, And also, I have removed the UsersWallet model/table comletely !.
- Also a note about 'balance' column that I have removed this functionality from my app, so now there is no balance or the ability to make users enter a balance  fornow (I wll add it later ISA) 


*How to see the changes*
- Visit Home page and look at currentViewSummary div
- Also you can go to routes.py, and then look at user_wallet()
- Also you can visit models.py and look at Class UsersWallet

