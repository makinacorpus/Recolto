<template>
  <div class="flex flex-col h-full">
    <header class="bg-[url('/assets/header_recolto.jpg')] bg-cover h-12 md:h-24">
      <div
        class="flex justify-between items-center mx-auto p-2 md:p-4"
      >
        <NuxtLink to="/">
          <img
            class="max-w-xs h-8 md:h-12"
            src="/assets/logo_recolto_blanc.png"
            alt="Logo de Récolt'Ô"

          />
        </NuxtLink>
        <div>
          <UButton
            title="About"
            icon="i-heroicons-information-circle-20-solid"
            size="xl"
            :ui="{ rounded: 'rounded-full', icon: {base: 'bg-white'}}"
            color="black"
            variant="ghost"
            square
            @click="isAboutModalOpen = true"
          />
          <NuxtLink v-for="locale in availableLocales"
            :key="locale.code" 
            :to="switchLocalePath(locale.code)"
            class="[vertical-align:super]">
            {{ locale.name }}
          </NuxtLink>
        </div>
        
      </div>
    </header>
    <div class="flex-grow flex">
      <slot />
    </div>
  </div>
  <UModal v-model="isAboutModalOpen" :ui="{wrapper: 'relative z-[1004]'}">
    <div class="p-10">
      <UButton
        size="xl"
        :ui="{ rounded: 'rounded-full' }"
        square
        color="gray"
        variant="ghost"
        icon="i-heroicons-x-mark-20-solid"
        class="absolute right-1 top-1"
        @click="isAboutModalOpen = false"
      />
      <p class="font-bold mb-4">
        Ce site est une démo du logiciel <a href="https://recolto.fr/" target="_blank" class="underline">Recolt'Ô</a>.
      </p>

      <p class="mb-4">
        Le code source du logiciel est disponible
        sur <a href="https://github.com/makinacorpus/Recolto" target="_blank" class="underline">son dépôt github</a> sous licence MIT.
      </p>

      <p class="mb-4">
        Ce projet est une initiative de <a class="underline" href="https://makina-corpus.com/territoires" target="_blank">Makina Corpus Territoires</a>.
      </p>
      <a href="https://makina-corpus.com" target="_blank">
        <img
          class="mx-auto max-w-xs w-32"
          src="/assets/MC_Territoires_LOGO_Carre_Quadri.svg"
          alt="Logo de Makina Corpus Territoires"
        />
      </a>
    </div>
  </UModal>
</template>

<script setup lang="ts">
const isAboutModalOpen = ref(false);
const { locale, locales } = useI18n()
const switchLocalePath = useSwitchLocalePath()

const availableLocales = computed(() => {
  return locales.value.filter(i => i.code !== locale.value)
})
</script>

