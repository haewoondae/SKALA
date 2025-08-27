<template>
    <!-- 주석: 템플릿에서는 .value 를 사용하지 않고 reactive로 하던거처럼 사용 -->
    <div>
        <p>카운트: {{ count }}</p>
        <button @click="count++">증가</button>
        <hr>
        </hr>
        <p>이름: <input v-model="name" /></p>
        <p>활성 상태: {{ name }} - {{ isActive ? '활성' : '비활성' }}</p>
        <button @click="isActive = !isActive">토글</button>
        <hr>
        </hr>
        <p>과일 목록: {{ items.join(', ') }}</p>
        <button @click="items.push('귤')">과일 추가</button>
        <hr>
        </hr>
        <p>인물: {{ person.name }} - {{ person.age }} 세</p>
        <button @click="person.age++">나이 증가</button>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)
const name = ref('홍길동')
const isActive = ref(true)
const items = ref(['사과', '배'])
const person = ref({ name: '홍길동', age: 20 })

</script>