<template>
    <div class=" text-center home-view">
        
        <!--Contains the wallet info if the current user (things like 'balance', 'credit', 'debt')  -->
        <CurrentViewSummary></CurrentViewSummary>
        
        <!-- This contains the page title only -->
        <Header class="title" pageTitle="Expenses"/>
        
        <!-- This contains :
            - input for year
            - input for month
            - Also it is resposible for fetching monthly expenses from server that belonged to the iputted time frame by the cirrent user
        -->

        <!-- 'sticky-header' will make the the indented elemnts stick at the top-->
        <div class="sticky-header">

            <div class="row sector">
                <div class="col-12">
                    <div class= "view-by ">
                        <input type="radio" class="radio-input" value="option1" name="view-by" id="view-by-month">
                        <label class="radio-label" for="view-by-month">View by Month</label>
                        <input type="radio" class="radio-input" value="option2" name="view-by" id="view-by-day" checked>
                        <label class="radio-label" for="view-by-day">View by Day</label>
                    </div>

                </div>    
            </div>

            <MonthTimeFrame @userChoseMonthTimeFrame="extractMonthlyExpenses" @toggelChooseTimeFrame="toggelChooseTimeFrame" ></MonthTimeFrame>
            

            <!-- This holds the total Expenses of the choosen month -->

            <MonthTotal :totalMonthlyExpenses="totalMonthlyExpenses"></MonthTotal>

        </div>
        
        <!-- THis contains a child components called 'Day' which each one of them contains the daily expenses details -->
        <Days :groupedExpensesByDay="groupedExpensesByDay" ></Days>

        <!-- This will route the user to 'AddExpenses' view enable users to add new expenses  -->
        <div class="router-link">

            <router-link class="bottom-fixed" to="addExpenses" >Add Expenses<span class="material-symbols-outlined">add_box</span></router-link>
        </div>
    </div>

</template>

<script>

    import Header from './../components/Header'
    import CurrentViewSummary from './../components/CurrentViewSummary'
    import MonthTimeFrame from '@/components/MonthTimeFrame.vue';
    import Days from '@/components/Days.vue';
    import MonthTotal from '@/components/MonthTotal.vue';
    import AddExpenses from './AddExpenses.vue';
    import ChooseTimeFrame from '@/components/ChooseTimeFrame.vue';


    export default {
        name: "Home",
        components: {
            Header,
            CurrentViewSummary,
            MonthTimeFrame,
            Days,
            MonthTotal,
            AddExpenses,
            ChooseTimeFrame,
        },
        data() {
            return {
                // This is emmited from <MonthTimeFrame> component, it represents the total expenses of the current user
                totalMonthlyExpenses: '0',
                // This is emmited from <MonthTimeFrame> component, it represents the monthly expenses details of current user
                monthlyExpenses: [],
                showChooseTimeFrame: false,
            }
        },
        methods: {
            // THis is will extract the monthly expenses details, that emmited from <MonthTimeFrame> child component
            extractMonthlyExpenses(monthlyExpenses) {
                this.monthlyExpenses = monthlyExpenses.monthlyExpenses
                this.totalMonthlyExpenses = monthlyExpenses.totalMonthlyExpenses
            },
            toggelChooseTimeFrame () {
                this.showChooseTimeFrame = !this.showChooseTimeFrame
            }
        },
        computed: {
            // This is computed property, which actully groups thr monthly expenses by day (So each day date will be an object that holds inside it a list [] of monthly expenses details and total amount spend in the month as object {})
            groupedExpensesByDay() {
                return this.monthlyExpenses.reduce((acc, expenses) => {
                if (!acc[expenses.date]) {
                    acc[expenses.date] = {
                    expenses: [],
                    totalAmount: 0
                    };
                }
                
                acc[expenses.date].expenses.push(expenses);
                acc[expenses.date].totalAmount += expenses.amount_spent;
                
                return acc;
                }, {});
            }
        } 
    }
</script>

<style >

    .home-view {
        width: 80vw;
        max-width: 800px;
        margin: auto;
    }

    .main-header {
        font-family: 'Roboto Slab', serif;
        font-weight: 300;
        letter-spacing: 0.35rem;
    }

    .money-header {
        font-family: 'Roboto Slab', serif;
        font-weight: 500;
        font-size: 20px;
    }

    .secondary-header {
        font-family: 'Roboto Slab', serif;
        font-weight: 400;
        font-size: 23px;
    }

    .secondary-header2 {
        font-family: 'Roboto Slab', serif;
        font-weight: 400;
        font-size: 16px;
        font-style: italic;
    }
    .sticky-header {
        position: sticky;
        top: 3.8rem;
        background: var(--background);
        padding-top: 1rem;
        z-index: 1019;
    }

    /* There is **TWO** methods to make '<router-link>Add Expenses</router-link>' become in the center of both containers, 'home-view', and 'body' (As it is 'position: fixed', so its margins will not be subjected to any parent except 'body', And you want it also to be in the center of 'home-view' too and not only 'body' to make it look good !)
    
        1- Create a parent div (.router-link in our case) to  '<router-link>Add Expenses</router-link>', and then apply 'display: flex' and 'align-items: center' and 'justify-content: center' (I choose this method)

        2- Don't create ab additional parent div, and instead make 'home-view' as 'position: relative' and then give '<router-link>Add Expenses</router-link>' --> 

            "left: 50%;
            transform: translate(-50%, -50%);"
        
    */
    /* That to make 'add-expense' */
    .router-link {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .bottom-fixed {
        margin: auto;
        position: fixed;
        bottom: 10px;
        padding: 10px 20px;
        background-color: var(--accent);
        color: white;
        text-align: center;
        /* This removes the default underline below links */
        text-decoration: none;
        border-radius: 100px;
        transition: background-color 0.3s ease;
        display: inline-flex;
        justify-content: space-around;
        width: 200px;
        z-index: 9999;
        }

    .bottom-fixed:hover {
        background-color: green;
    }

    /*  */

    .navbar-brand {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
    }

    

    .view-by {
        display: inline-flex;
        width: 100%;
        overflow: hidden;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.25);
        
    }

    .radio-input {
        display: none;
    }

    .radio-label {
        text-align: center;
        padding: 3px 14px;
        font-size: 13px;
        font-family: sans-serif;
        color: var(--accent);
        background: var(--secondary);
        cursor: pointer;
        transition: background 0.1s;
        width: 100%;
    }

    .radio-label:not(:last-of-type) {
        border-right: 1px solid var(--background);
    }

    .radio-input:checked + .radio-label {
        background: var(--primary);
    }

    .jeke {
        width: 100%;
        /* border: 1px solid black; */
    }

</style>
