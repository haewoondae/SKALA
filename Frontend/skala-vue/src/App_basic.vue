<template>
  <h1>안녕하세요</h1>
    <input id="input" placeholder="Enter a message"></input>
    <p id="message">parrot: </p>
</template>




<script setup>
import { ref } from 'vue';

const input = ref('');
</script>

