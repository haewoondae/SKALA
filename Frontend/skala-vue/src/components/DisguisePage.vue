<template>
    <div>
        <h1>둔갑술 시전!</h1>
        <p> 홍길동이 <strong>{{ target }}</strong>(으)로 변신했습니다!</p>
    </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'

const route = useRoute()
const router = useRouter()
const target = ref('???')

onMounted(() => {
    if (route.query.target) {
        target.value = route.query.target
        // 브라우저 URL에서 query 부분 제거 (제거 안하면 사용자가 다른 target을 입력할 수 있음)
        router.replace({ query: {} })
}
})
</script>
