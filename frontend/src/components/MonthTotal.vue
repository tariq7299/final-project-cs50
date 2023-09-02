<template>
    <div>
        <h1>{{ year }}</h1>
        <h1>{{ month }}</h1>
    </div>
</template>

<script>
export default {
    name: "MonthTotal",

    props: {
        year: Number,
        month: String,
    }
}
</script>

<style>

</style>