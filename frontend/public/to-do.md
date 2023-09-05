# GLOBAL
- Remove to-do.md from remote

# Backend 
=========

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

## run.py
- How to find a way to the server url dynamic in the frontend ??, like every time I want to make a axios request I won't have to type the exactly localhost...:5000, because sometimes the port number changes !
## routes.py
- filter each currency to be viewed as currency like in finance problem from CS50 usd() function
# Frontend
==========

## GLOBAL
- Add login and register page
- Add nav bar to every view

## Home.vue
- Make the nav bar stick at top by bootstrap not plain css
- What is '/@/component'

## CurrentViewSummary
- 

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
- 

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