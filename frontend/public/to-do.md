# GLOBAL
- Remove to-do.md from remote
- Connect to api that gets the value of current dollar **OR** make the user write the doller currency when he opens the app !
- Enable users to view any money as Egp or $
-  

# Backend 
=========
## GLOBAL
- Create to main versions of your codebase ! one that is dependednt on functions (functional programming) and another one that is dependent on objects (OOP)
- Make a function in helpers for "response_object", (That can create responses objects)
- USE 'PUT' and 'DELETE' instead of 'POST' in appropriate stiuations.
## models.py
- Add indexes to databases to make querieas it faster
- Make name in users table as first name and last name
- add password hash to users table 
- Explain lazy=True
- Understand more db.relationship
- Find a better way to import datetime module in models.py
- Removes the zeros in Wed, 13 Sep 2023 00:00:00 GMT ?? from the column of USerSpendings
- Change "item_type" to "category" @#
- Make sure string(64) nummbers is corerect for each column
- Add a new column to USerSpendings whcih contain the total spenf¥ding of each day !, if it was too hard then try to creat a compnent called <Day> then inside day there is {{ total daily spendingas }} and all the days spendings child components whxuh contint the daily spendings details
- Add History table which view all the history of transactions !
- Populate UserSpendings with some samole rows with coulumns called 'catogory' insterad of "item_type"
- Change the date columns to be datetime().now() and not datetime.now().date() to be able to sort it later !
- Consider adding a column called "Currency" "UsersDebts and UsersCredits" to enable users to store value of money indifferent currencires
- Consider removing "wallet_id" from UsersWallets as serves the purpose as "user_id"
- Change the UserSpendinds to UsersExpenses, annd also each coulmn with 'spending' title to 'expense' ..etc


## run.py
- How to find a way to the server url dynamic in the frontend ??, like every time I want to make a axios request I won't have to type the exactly localhost...:5000, because sometimes the port number changes !
## routes.py
- filter each currency to be viewed as currency like in finance problem from CS50 usd() function
- Ask GPT if there a better names for the routing functions in routes.py
- Handle affexpnse() error usererrors/amliciousUsers/...etc
- change every "spending" to "expense"
- Write comments in routing functions

## helpers.py
- Write comments for calendar days functions 
# Frontend
==========

## GLOBAL
- Add login and register page
- Add nav bar to every view
- Apply egp() to each currency in the whole app
- add Loading indicatior in every fetch request happens in any page ! (I actually have made a working one in 'CurrentViewSummary' )
- Use Environment Variables: Instead of hardcoding the API endpoint path (http://127.0.0.1:8083/userWallet), consider using environment variables to make your code more configurable and to easily switch between different API endpoints for development, testing, and production environments.
- Use Caching or Memoization: If you frequently fetch the same data and it doesn't change often, you could consider implementing caching or memoization techniques to reduce unnecessary API requests.
- Use Reusable Axios Instance: Depending on your project, you may want to create a reusable Axios instance with default configurations (e.g., base URL, headers) instead of configuring Axios in every component. This can help centralize your API configuration and simplify maintenance.
- Code organization: It’s generally a good idea to keep your code organized and modular. In this case, you could consider moving the code for fetching the user’s wallet data into a separate module or service, and then importing that module into your component. This would make your component code cleaner and easier to read, and would also make it easier to reuse the code for fetching the user’s wallet data in other parts of your application.
-       -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        Explaint the previous lines ??
- Use Vuex to 'store' your app states and globalize it
- Write parent container for your vue html and some rows and columns
- Style the nav bar
- Main font `Avenir, Helvetica, Arial, sans-serif;` not imported correctly !, ANd I think the reason becasue of the google font <link>, that I messed Up !!

## Home.vue
- Make the nav bar stick at top by bootstrap not plain css
- What is '/@/component'
- link inide nav bar elements, and correct pages of app
- Create a component for "view-by" div
- Also create a compoenent for nav bar
- Make nav-bar and and 'view-by' and 'TimeFrame' and 'ChooseTimeFrame' as sticky (Use import VueStickyElement from "vue-sticky-element";) and use (Vuex, as you will relly not able to achive a sticky elements in view without global state of Veux) 

## CurrentViewSummary
- Enable the users to store a second currency in balance and debt and credit
- Handle error in fetchUserWallet() like you did in 'AddExpenses()' in AddEspenes.vue

## routes.vue
- Change routes.vue to index.js
## MonthTimeFram
- Remove async and await from mounted() {} @#
- Choose the last/current year of User's spendings by default from the select input
- Change the years drop down and make more user friendly
- Remove the input argument 'selectYear' fetchMonths(selectYear), and instead rely on v-model version of "selectedYear" @#
- Change the "MonthTimeFrame" to somthing good
- Make the  most recent month and most_recent_year be calculated in backend
- Create a total_daily_spendings
- AFter I finish the app I want to chnage the how the user chooses a month, by implementing the following steps :
        1- Restructure/Rebuild the MonthTimeFrame to be the same except for that it will lnow be resposible for just fetching expenses time frame and adate and just displaying the year and current month ina <button> tag
        2- Whem user presses on the button the will direct him to a view via router-link, where he can select a year and a month (Acordion)
        3- Then that view emmits the selectedYear and selectedMonth to parent of MonthTimeFrame
        4- Finally monthTiime Frame will emit the seleced time and expenses to parent of Home (all of that in the old way)
        - Note: Use Veux to make your life much easer !
        - Note: This is a Hint, of what MonthTimeFrame might look like:
                        // MonthTimeFrame.vue
                        <template>
                                <div>
                                        <router-link to="/ChooseTimeFrame">
                                                <button>2023 Sep</button>
                                        </router-link>
                                </div>
                        </template>
## SpendingsDays
- Enable Users to view there expenses/spendings in different currencies !

## AddExpense
- Create a num pad instead of phone num pad
- Clear days <sleelct> after user changes month 
- Add an alert after user adds/submits an expenses
- 



                                # TOMMOROOE
                                -----------

- Remove 00:00 GMT
- Style the Home page a little biy
- Create the Add new Expense

                                # TOMMOROOE
                                -----------

- Security Considerations: Be cautious about displaying too much technical information to the user, as it could potentially expose sensitive information or be exploited by malicious users. Ensure that the error message does not leak sensitive data.

