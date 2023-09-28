<template>
     <div class= "view-by sector">

         <input type="radio" class="radio-input" value="option1" name="view-by" id="view-by-month">
        <label class="radio-label" for="view-by-month"><span>Month </span>View<span></span></label>
                          
        <input type="radio" class="radio-input" value="option2" name="view-by" id="view-by-day" checked>
        <label class="radio-label" for="view-by-day"><span>Day </span>View<span></span></label>

        <slot></slot>

     </div>
</template>

<script>
    export default {
        name: 'ViewBy',
    
    }
</script>

<style>

.view-by {
        display: inline-flex;
        width: 100%;
        max-width: 500px;
        overflow: hidden;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.25);
        
    }

    .radio-input {
        display: none;
    }

    .radio-label {
        text-align: center;
        padding: 3px 14px;
        font-size: 13px;
        font-family: sans-serif;
        color: var(--accent);
        background: var(--secondary);
        cursor: pointer;
        transition: background 0.1s;
        width: 100%;
    }

    .radio-label:not(:last-of-type) {
        border-right: 1px solid #fff;
    }

    .radio-input:checked + .radio-label {
        background: var(--primary);
    }

@media (max-width: 450px) and (orientation: portrait) {

.radio-label {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
}
</style>