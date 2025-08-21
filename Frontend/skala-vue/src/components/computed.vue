<template>
    
    <label>이름:
        <input type="text" v-model="firstName" />
    </label>

    <label>성:
        <input type="text" v-model="lastName" />
    </label>

    <div> {{ getFullName() }}, {{ fullName }}</div>
</template>

<script setup>
import { ref, computed } from 'vue'

const firstName = ref(' ')
const lastName = ref(' ')

// 이렇게 하면 입력값을 넣어도 변화가 없음
//const fullName = `${lastName.value} ${firstName.value}`

// fullName 을 얻는 함수
function getFullName() {
    return `${lastName.value} ${firstName.value}`
}

// computed 를 사용
const fullName = computed(() => `${lastName.value} ${firstName.value}`)

//두 방법 모두 효과는 같음
//함수는 호출마다 실행
//computed는 의존 값 변경 시에만 실행
//이 코드에서는 동일한 결과를 얻음
</script>
