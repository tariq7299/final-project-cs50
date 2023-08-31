<template>
    <div>
        <h1>{{ title }}</h1>        
    </div>
</template>

<script>
    import UserFinance from './UserFinance'
    import axios from 'axios'

    export default {
        name: "Header",
        components: {
        },
        props: {
            title: String,
        },
    }
</script>

<style>

</style>