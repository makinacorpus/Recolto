<template>
  <UPopover
    mode="hover"
    :ui="{
      width: 'max-w-md',
      background: 'bg-purple dark:bg-gray-900',
    }"
  >
    <UIcon name="i-heroicons-information-circle" class="w-6 h-6 " />
    <template #panel>
      <div class="p-2 text-sm">
        <slot />
      </div>
    </template>
  </UPopover>
</template>