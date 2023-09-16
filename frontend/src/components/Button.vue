<template>
    <button @click="onClick()" class="" ><span class="material-symbols-outlined ">
    edit_calendar
    expand_more
    </span></button>
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

<style scoped>
    .material-symbols-outlined {
        font-variation-settings:
            'FILL' 0,
            'wght' 400,
            'GRAD' 0,
            'opsz' 24
    }

    button {
        background-color: var(--accent); 
        border: none;   
        color: white;
        padding: 6px 6px 3px 6px;
        text-align: center;
        text-decoration: none;
    }
    button:hover {
        background-color: var(--primary);
    }
</style>
