<template>
  <div class="m-3">
    <label :for="inputId" class="form-label">{{ props.label }}</label>
    <input v-model="modelValue" :type="props.type" class="form-control" :id="inputId" :placeholder="props.placeholder"  @keyup.enter="sendEvent" />

  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  label: String,
  type: String,
  placeholder: String
});

const emit = defineEmits(["enterKeyPressed"]);
function sendEvent() {
  emit("enterKeyPressed");
}

const modelValue = defineModel();

const inputId = crypto.randomUUID();


</script>