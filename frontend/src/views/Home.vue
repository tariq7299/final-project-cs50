<template>
    <div class="container-fluid text-center  "  >
        <!-- 'sticky-header' will make the the indented elemnts stick at the top-->


            <div class="container-fluid sticky-header ">
                
            <!--Contains the wallet info if the current user (things like 'balance', 'credit', 'debt')  -->
            <CurrentViewSummary></CurrentViewSummary>
            <!-- This contains the page title only -->
            
            <Header class="title" pageTitle="Expenses"/>
            
            <!-- This contains :
                - input for year
                - input for month
                - Also it is resposible for fetching monthly expenses from server that belonged to the iputted time frame by the cirrent user
            -->
            <div class="row view-by-container">
                <div class="col-12">
                    <div class= "view-by">
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
        <router-link class="sticky-bottom" to="addExpenses" >Add Expenses</router-link>

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

<style>
    .test{
        position: -webkit-sticky; /* Safari */
        position: sticky;
        /* top: 4rem; */
        /* margin-top: 30rem; */
        /* background-color: var(--background); */
    }
    

   
    .sticky-header {
    position: -webkit-sticky; /* Safari */
    position: sticky;
    top: 3.5rem;
    /* margin-top: 30rem; */
    background-color: var(--background);
    }

 

    .sticky-bottom {
    position: fixed;
    bottom: 0;
    }

    .navbar-brand {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
    }

    .view-by-container {
        position: relative;
        top: 3rem;
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

</style>
