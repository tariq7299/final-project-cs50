<template>
    <div class="alert">
        <v-alert :type="type" :title="title" :text="text" variant="tonal">
        </v-alert>
    </div>
</template>

<script>
    export default {
        name: 'FlashMessage',
        props: {
            text: String,
            type: String,
            title: String
        }
    }
</script>

<style scoped>
.alert {
    padding: 1rem 0 ;
}

</style>