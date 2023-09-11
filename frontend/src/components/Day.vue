<template>
    <div class="center">
        
        <!-- I have used vue binding directives "" :data-bs-target='"#" + uniqueId' "", in 'accordion' boostrap compoennet, becasue in order for each accordion to collapse and expand when you click on it, Each 'data-bs-target' property in <button> of accordion should point to a unique 'id' down in accordion body, so I have made some adjustments and apllied the v-for loop of vue to uniqlyt assing variables to each accordion !-->
        <div class="accordion" id="accordionExample">
            <div class="accordion-item">
                <h2 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target='"#" + uniqueId' aria-expanded="true" aria-controls="collapseOne">
                    {{ dayDate }} - Total Amount: {{ totalAmount }}
                </button>
                </h2>
                <div :id="uniqueId" class="accordion-collapse collapse show" >
                <div class="accordion-body">
                    <div class="" v-for="expense in expenses" :key="expense.spending_id">
                        <p>Amount: {{ expense.amount_spent }} - Category: {{ expense.category }}</p>
                    </div>
                </div>
                </div>
            </div>
            
        </div>        
    </div>
  </template>

<script>
    export default {
        name: 'Day',
        props: {
            dayDate: String,
            expenses: Array,
            totalAmount: Number
        },
        computed: {
            uniqueId() {
                return "collapse" + this.dayDate.substring(4, 6);
            }
        }
    }
</script>

<style scoped>
    .center {
        margin: auto;
    }

</style>

