<template>
    <h1>댓글 달기</h1>
    <!-- <input v-model.trim="comment"> </input>  -->
    <input v-model.trim="comment"> </input> 
    <button @click="addComment">추가</button>
    <ol>
        <li v-for="(item, index) in comments" :key="index">{{ item }}</li>
    </ol>
</template>

<script setup>
import { ref } from "vue"

const comments = ref([])
const comment = ref('' )

function addComment() {
    if (inputComment.value != '')
        comments.value.push(inputComment.value)
        inputComment.value = ''
}
</script>




