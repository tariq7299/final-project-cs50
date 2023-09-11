<template>
    <div class="main-header row">
        <h1>{{ pageTitle }}</h1>        
    </div>
</template>

<script>
    export default {
        name: "Header",
        components: {
        },
        props: {
            pageTitle: String,
        },
    }
</script>

<style>
    .page-title {

        font-family: 'Roboto Slab', serif;
        font-weight: 300;
        letter-spacing: 0.35rem;
    } 
</style>