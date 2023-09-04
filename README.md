# finale-project

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


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

