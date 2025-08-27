<template>
    <div>
        <!-- Message Input -->
        <input v-model="message" placeholder="Type something">
        <p>Message: {{ message }}</p>

        <!-- Name Input -->
        <input v-model="name" placeholder="Type your name">

        <!-- Checkbox and Radio Inputs -->
        <input type="checkbox" v-model="isChecked">

        <input type="radio" name="gender" value="male" v-model="selected">
        <input type="radio" name="gender" value="female" v-model="selected">

        <select v-model="selected">
            <option value="Y">Yes</option>
            <option value="N">No</option>
        </select>
    </div>
</template>

<script setup>
import { ref } from 'vue';


const message = ref("");
</script>
