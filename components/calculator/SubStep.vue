<template>
  <div class="bg-purple p-2 md:p-4 rounded-2xl mb-2 md:mb-4 relative">
    <h2
      class="absolute font-semibold -top-2 -left-2 w-8 h-8 text-center rounded-full bg-purple shadow-xl border border-white"
    >
      {{ number }}
    </h2>
    <h3 class="text-center text-sm md:text-base">
      {{ title }}
    </h3>
    <p v-if="$slots.subtitle" class="mt-2 italic text-base/5 hidden sm:block">
      <slot name="subtitle"></slot>
    </p>
  </div>
  <div class="mx-4 mb-4">
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  number: number,
  title: string,
}>();
</script>