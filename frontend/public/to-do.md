# GLOBAL
- Remove to-do.md from remote
- Connect to api that gets the value of current dollar **OR** make the user write the doller currency when he opens the app !
- Enable users to view any money as Egp or $
-  Cretaet a branch from commit 64c090ceaab857dc7ab86a17fad62da4644a3e4a and call it 'accordion v-1.0, double click  bug'
- Replace alerts() with more user friendly notification !
- Access mobiles kits (like, NOTIFICATIONS, STORAGE, CAMERA....etc)
- Rebuild and populate all dbs

- Add a SYSTEMATIC APPROACH TO : 
        1- fixed margins acrros sectors
        2- Components driven engineering
        3- In styling (like for example: there is global styles, and styles under each component, and scoped styles under each view, adn there is a place in every view for @media for differet screen sizes)
        4- Orgnized folders and files in both front and back (like for example, search online on how to orgnize vue files like I did with flask files)
        5- How are the versions (Branches) of my web app depend on (like I want to make a shitt ton of versions each with major structrue changes, like for ex using Nuxt.js, maybe using CSS only, maybe another with OOP only, mayb another with functional programming only, mayb another with a design pattern implemented.......etc), and do'nt forget the notes and comments on every branch in README
        6- Alos maybe there are side branches that emmites from the main branhches (like diffreent implementation of parts in the main branch)
        7- 


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
- Create a notes column for User Expenses, and connect it to frontend
- Add Email column to USers db model
- Add CheckContstraint to all tables that don't have one

## run.py
- How to find a way to the server url dynamic in the frontend ??, like every time I want to make a axios request I won't have to type the exactly localhost...:5000, because sometimes the port number changes !
## routes.py
- filter each currency to be viewed as currency like in finance problem from CS50 usd() function
- Ask GPT if there a better names for the routing functions in routes.py
- Handle affexpnse() error usererrors/amliciousUsers/...etc
- change every "spending" to "expense"
- Write comments in routing functions
- Handle valdition form errors in server side from 'AddExpenses'
- Create a diffrent file for each group of routes related to each other, and make each a BlueBrint
- Add egp() and amount/100 and amount*100 to '/contacts'
- Order expeneses by ID not by date, when you send them to server
- Change the get_calendar function and route name
- Chnage all the functions and routes names that are not appropriate

## Add Expenses route
- Give the default categories of the app and add to them the created ones user created

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
- Create a layout.vue/base.vue component that will be used glabally across all of your views and components
- Create Make every part of the web app as a compoennet that can be ssinged and custmized through props and data, to fit in every view ! 
- Add responsive to every page

## Home.vue
- Make the nav bar stick at top by bootstrap not plain css
- What is '/@/component'
- link inide nav bar elements, and correct pages of app
- Create a component for "view-by" div
- Also create a compoenent for nav bar
- Make nav-bar and and 'view-by' and 'TimeFrame' and 'ChooseTimeFrame' as sticky (Use import VueStickyElement from "vue-sticky-element";) and use (Vuex, as you will relly not able to achive a sticky elements in view without global state of Veux) 
- Make "Debit" and 'Credit' clickbale and each direct me to custom view by debt or custom view by credit

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

- animate show years and months select
- Also animate the changing of Month on "2023-Nov", whenever user chooses a month, also maybe change the background color of '2023-Nov'
- Expenses entered by user appear as expense*100, !!!, so we need to fix this (Try to enter an expense)
## SpendingsDays
- Enable Users to view there expenses/spendings in different currencies !

## AddExpense
- Create a num pad instead of phone num pad
- Clear days <sleelct> after user changes month 
- Add an alert after user adds/submits an expenses
- Rebuild AddExpense frontend from groundup using Plain CHAD CSS
- Handle form vaidation via HTML in frontend
- Style the frontend --- COLORS  NICEER-ICONS BETTER-BUTTON
- Enable user to add new category
-  Make the add expense button not floating but instead a part of the pview, to not obstruct any expenses
- Prevent default after submitting and clear all inputs, after user submits as it doesn't get cleared automatically
- Get the value of date in add expense as a whole date object thatincludes actual time, and store it in db  in server side
## ChooseTimeFrame
- Add the total expense beside each month name
- Animate the arrow when user clicks on the already opened accordion !
- CLean chooseTimeFraem in fronend and also all its functions from server

## Contacts
- Make the "Custom View" radio button as dropdown list 'Debtors, Creditors'

## Add Transactions
- Change input icons
- CHange classes names in add transactions
- Make the app take date includeing seconds and minutes and hourse, and don't extract month ...etc

## Add new Contract
- Assign appropriate classes names and IDS and names ....

                                # TOMMOROOE
                                -----------

- Remove 00:00 GMT
- Style the Home page a little biy
- Create the Add new Expense

                                # TOMMOROOE
                                -----------

- Security Considerations: Be cautious about displaying too much technical information to the user, as it could potentially expose sensitive information or be exploited by malicious users. Ensure that the error message does not leak sensitive data.

