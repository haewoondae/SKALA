<template>
  <div class="m-3">
    <div v-for="(option, index) in props.options" :key="index" class="form-check">
      <input 
        class="form-check-input" 
        type="radio" 
        :name="id" 
        :id="id + index" 
        v-model="modelValue" 
        :value="option.value" 
        :disabled="props.disabled" 
      />
      <label class="form-check-label" :for="id + index">
        {{ option.label }}
      </label>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineModel } from "vue";

// 컴포넌트 props 정의
const props = defineProps({
  options: Array,
  disabled: Boolean,
});

// v-model을 위한 데이터
const modelValue = defineModel();

// 고유 ID 생성
const id = crypto.randomUUID();
</script>