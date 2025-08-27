<template>
    <div>
    <button @click="showInputBox"> 입력창 열기</button>
    <div v-if="isVisible">
        <input ref="inputRef" placeholder=" 이름 입력 " />
    </div>
    </div>
</template>


<script setup>
import { ref, nextTick} from 'vue'

const isVisible = ref(false)
const inputRef = ref(null)

// async 를 사용하지 않으면 에러가 발생
async function showInputBox() {
    isVisible.value = true

    await nextTick()
    inputRef.value?.focus()
}

// function showInputBox() {
//     isVisible.value = true

//     // sleep을 줘서 해결
//     setTimeout(() => {
//         inputRef.value?.focus()
//     }, 10)
// }

</script>