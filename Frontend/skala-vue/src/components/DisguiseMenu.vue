<template>
    <div>
        <h1> 둔갑술 선택 메뉴</h1>
        <button @click="goToDisguise('호랑이')">호랑이로 둔갑</button>
        <button @click="goToDisguise('도깨비')">도깨비로 둔갑</button>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goToDisguise(target) {
    console.log(target)
    // "/disguise?target=호랑이" 형태로 경로 전환
    router.push(`/disguise-target?target=${target}`)
}
</script>