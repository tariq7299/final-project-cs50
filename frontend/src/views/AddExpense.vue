
<template>

  <div class="row">
    <form @submit.prevent="submit">
        <div class="col">
            <!-- <h1>{{ calenderDays }}</h1> -->
            <label for="day">Date</label>
            <select v-model="selectedDay" name="day" id="day">
                <!-- We have to JSON.parse(calenderDays) because we have JSON.strigify() it in HOME.vue-->
                <option v-for="day in JSON.parse(calenderDays)" :value="day.day_num" :key="day.day_num">{{ day.day_name }}, {{ day.day_num }}</option>
            </select>
        </div>
        <div class="col">
            <label for="amount-spent">Amount</label>
            <input v-model="amountSpent" name="amount-spent" id="amount_spent" placeholder="Enter Amount"
            autofocus>
        </div>
        <!-- <div class="col">
            <label for="day">Category</label>
            <select v-model="selectedCategory" name="category" id="category">
                <option v-for="(category, index) in categories" :value="category" :key="index">{{ category }}</option>
            </select>
        </div> -->
        <div class="col">
            <button class="btn btn-dark" type="submit" id="button">Add</button>
        </div>
    </form>
  </div>

</template>

<script>
export default {
    name: 'AddExpense',
    data () {
        return {
            selectedDay: this.currentDay,
            amountSpent:'',
        }
    },
    props: ['calenderDays', 'currentDay'],
    created() {
        console.log(JSON.parse(this.calenderDays))
        console.log(this.currentDay)
    }
}
</script>

<style>

</style>