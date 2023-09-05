<template>
    <div>
        <div class="sticky-header">
            <nav class="navbar bg-body-tertiary fixed-top">
            <div class="container-fluid">
            <a class="navbar-brand" href="#">goldgardyn</a>
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
            <Header title="Spending"/>
    
            <CurrentViewSummary></CurrentViewSummary>
    
            <MonthTimeFrame @userChoseMonthTimeFrame="extractMonthlySpendings"></MonthTimeFrame>
    
            <MonthTotal :total_monthly_spendings="total_monthly_spendings"></MonthTotal>
        </div>
        
        <SpendingsDays :monthSpendings="monthSpendings" ></SpendingsDays>

        <!-- you have to JSON.stringify() arrays before passing it to urls !, and then on the other side when you extract this array from the url, you have to JSON.parse() it -->
        <!-- Notice that we didnot do that with  'currentDay' because it is not an array-->
        <router-link class="sticky-bottom" to="addExpense" >Add Expenses</router-link>
    </div>
</template>

<script>
    import Header from './../components/Header'
    import CurrentViewSummary from './../components/CurrentViewSummary'
    import MonthTimeFrame from '@/components/MonthTimeFrame.vue';
    import SpendingsDays from '@/components/SpendingsDays.vue';
    import MonthTotal from '@/components/MonthTotal.vue';
    import AddExpense from './AddExpense.vue';
    export default {
        name: "Home",
        components: {
            Header,
            CurrentViewSummary,
            MonthTimeFrame,
            SpendingsDays,
            MonthTotal,
            AddExpense,
        },
        data() {
            return {

                total_monthly_spendings: null,
                monthSpendings: null,
            }
        },
        methods: {
            extractMonthlySpendings(monthSpendings) {
                this
                this.monthSpendings = monthSpendings.monthSpendings
                this.total_monthly_spendings = monthSpendings.total_monthly_spendings
            }
        },
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

</style>
