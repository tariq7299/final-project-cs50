<template>
    <div>

        <nav class="navbar bg-body-tertiary fixed-top">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">GoldGardyn</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
                <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
                    <div class="offcanvas-header">
                        <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Offcanvas</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                    </div>
                    <div class="offcanvas-body">
                        <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                        <li class="nav-item">
                            <a class="nav-link active" aria-current="page" href="#">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Link</a>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Dropdown
                            </a>
                            <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li><a class="dropdown-item" href="#">Something else here</a></li>
                            </ul>
                        </li>
                        </ul>
                        <form class="d-flex mt-3" role="search">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                        <button class="btn btn-outline-success" type="submit">Search</button>
                        </form>
                    </div>
                </div>
                
            </div>
        </nav>

        <!-- 'sticky-header' will make the the indented elemnts stick at the top-->
        <div class="sticky-header">
            
            <!-- This contains the page title only -->
            <Header pageTitle="Expenses"/>

            <!--Contains the wallet info if the current user (things like 'balance', 'credit', 'debt')  -->
            <CurrentViewSummary></CurrentViewSummary>
            <div class="view-by">

                <input type="radio" class="radio-input" value="option1" name="view-by" id="view-by-month">
                <label class="radio-label" for="view-by-month">View by Month</label>

                <input type="radio" class="radio-input" value="option2" name="view-by" id="view-by-day" checked>
                <label class="radio-label" for="view-by-day">View by Day</label>

            </div>
            
            <!-- This contains :
                - input for year
                - input for month
                - Also it is resposible for fetching monthly expenses from server that belonged to the iputted time frame by the cirrent user
             -->
            <MonthTimeFrame @userChoseMonthTimeFrame="extractMonthlyExpenses"></MonthTimeFrame>
            
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

    export default {
        name: "Home",
        components: {
            Header,
            CurrentViewSummary,
            MonthTimeFrame,
            Days,
            MonthTotal,
            AddExpenses,
        },
        data() {
            return {
                // This is emmited from <MonthTimeFrame> component, it represents the total expenses of the current user
                totalMonthlyExpenses: '0',
                // This is emmited from <MonthTimeFrame> component, it represents the monthly expenses details of current user
                monthlyExpenses: [],
            }
        },
        methods: {
            // THis is will extract the monthly expenses details, that emmited from <MonthTimeFrame> child component
            extractMonthlyExpenses(monthlyExpenses) {
                this.monthlyExpenses = monthlyExpenses.monthlyExpenses
                this.totalMonthlyExpenses = monthlyExpenses.totalMonthlyExpenses
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

    .sticky-header {
    position: sticky;
    top: 4rem;
    }

    .sticky-bottom {
    position: fixed;
    bottom: 0;
    }

    .navbar-brand {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
    }

    .view-by {
        width: 80vw;
        max-width: 600px;
        display: inline-flex;
        overflow: hidden;
        /* border-radius: 15px; */
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
        width: 50%;
    }

    .radio-label:not(:last-of-type) {
        border-right: 1px solid var(--background);
    }

    .radio-input:checked + .radio-label {
        background: var(--primary);
    }

</style>
