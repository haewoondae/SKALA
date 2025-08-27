<template>

    <label> 키 : <input v-model="height"></input></label>
    <label> 몸무게 : <input v-model="weight"></input></label>

    <div> BMI: {{ bmi.toFixed(2) }}, 판정: {{ bmiMessage }}</div>

</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue';

const height = ref(170);
const weight = ref(60);

const bmi = computed(() => { weight.value / ((height.value / 100) ** 2) });
const bmiMessage = ref('')

watch(bmi, (newBMI) => {
    if (newBMI < 18.5) {
        bmiMessage.value = '저체중'
    } else if (newBMI < 23.0) {
        bmiMessage.value = '정상'
    } else if (newBMI < 25.0) {
        bmiMessage.value = '과체중 - 다이어트 하세요'
    } else {
        bmiMessage.value = '비만 - 다이어트 하세요'
    }
})

onMounted(() => {
    console.log('Component mounted')
})


//미완성
</script>

