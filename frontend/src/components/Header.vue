<template>
    <div class="row">
        <h1 class="page-title">{{ pageTitle }}</h1>        
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

<style scoped>
    .page-title {

        font-family: 'Roboto Slab', serif;
        font-weight: 400;
        /* margin: 20rem 0 3rem 0; */
        /* margin-top: 30rem; */
        letter-spacing: 0.35rem;
    }

</style>