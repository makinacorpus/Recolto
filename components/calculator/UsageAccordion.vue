<template>
  <UButton
    @click.self="toggle = !toggle"
    class="bg-cool rounded-lg border-2 w-full flex flex-col relative mb-2 overflow-hidden dark:bg-cool dark:text-white"
    :class="{
      'hover:bg-purple-300/50 dark:hover:bg-purple-300/50': toggle,
      'hover:bg-purple-900 dark:hover:bg-purple-900': !toggle,
    }"
  >
    <UIcon
      v-if="toggle"
      name="i-heroicons-check-circle"
      class="absolute top-0 right-0 w-8 h-8"
    />
    <div
      class="flex text-lg my-2"
    >
      <p
        class="w-full"
        @click.self="toggle = !toggle"
      >
      {{ title }}
      </p>
      <InformationTooltip v-if="$slots.help" class="hidden md:ml-2 md:w-1/6 md:block md:self-center">
        <p class="text-sm m-1">
          <slot name="help"></slot>
        </p>
      </InformationTooltip>
    </div>

    <div v-if="toggle" class="flex flex-row w-11/12 items-center my-2">
      <slot/>
    </div>

  </UButton>
</template>

<script setup lang="ts">
import InformationTooltip from './InformationTooltip.vue';

defineProps<{
  title: string,
}>();

const toggle = ref(false)
</script>