<template>
  <button @click="onClick()" class="btn btn-warning">Choose another Month</button>
</template>

<script>
export default {
    name: 'Button',
    methods: {
        onClick() {
            this.$emit('btnClicked')
        }
    }
}
</script>

<style>

</style>