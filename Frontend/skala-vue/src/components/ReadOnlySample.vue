<template>
    <div>
    <p>이름: {{ user.name }}</p>
    <p>나이: {{ user.age }}</p>
    <!-- 클릭 시 콘솔 경고, 변경 안됨 -->
    <p>원본 이름: {{ original.name }}</p>
    <p>원본 나이: {{ original.age }}</p>

    <button @click="original.age++">오리지널 - 한 살 더</button>
    <button @click="user.age++">리드온리 - 한 살 더</button>

    </div>
</template>

<script setup>
import { reactive, readonly } from 'vue'

const original = reactive({ name: '홍길동', age: 20 })
const user = readonly(original)
</script>