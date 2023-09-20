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
# If you will authinticate users using 'Seesion-qthuitication' technique, You have to set theses two environment variables in flask backend, as this is necessary becasue this app uses CORS
SESSION_TYPE = 'filesystem'
SESSION_COOKIE_SECURE = True 
SESSION_COOKIE_SAMESITE = 'None' 
{ withCredentials: true } # Alos include this in every axios request sent from frontend (Vue js) to backend (Flask)

npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Vue Configuration Reference](https://cli.vuejs.org/config/).
See [Flask Configuration Reference](https://flask.palletsprojects.com/en/2.3.x/config/)



## Notes on vuetify in this project

- After adding vuetify, it actually overrides all the default styles of HTML elements !. so lets say for example there is a default `padding` in `<button>` tags, However after adding vuetify, it removes this `padding`, so you have to specify a custom `padding` by you in `<style>`, all of that apply to every element in the whole app.
## Some notes on branches
- First of all !, all of those branches is not fully working but rather it is some different versions of implementing some components and parts of the code   

### 'router-link' branch
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

### 'monthTimeFrameBranch' branch
*files to check **or** files that is relative*
- 'MonthTimeFrame'
- 'routes.py'

*What this branch does*
In this branch I used different ways to view years and months, by using different methods to fetch spendings data in "methods" found in 'MonthTimeFrame.vue', that is different than what I am using right now in main branch, that is the only distict thing   

*How to see the changes*
- Visit Home page, look at the years and months selecet inputs
- Understand what is going on in "MonthTimeFrame.vue' and axios requests that sent back and fourth to the flask server in 'routes.py'
- All the main changes can be found in 'methods:' in 'MonthTimeFrame'
### 'monthTimeFrameBranch' branch
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

