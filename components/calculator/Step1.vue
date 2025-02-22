<template>
  <div class="md:mb-2">
    <SearchBar
      class="mb-6"
      @new-location="$emit('newCenter', $event)"
    />
    <SubStep
      :number="1"
      :title="t('step1.substep1')"
    >
      <template v-slot:subtitle>
        {{ t("step1.roof_type_info") }}
      </template>
      <div class="flex gap-3 flex-wrap justify-between">
        <URadio
          class="w-fit text-white font-semibold"
          v-for="typeRoof of typeOfRoofWithCoeff"
          :key="typeRoof.name"
          input-class="border-purple text-purple dark:border-slate-700 dark:text-slate-700 dark:bg-slate-700"
          :model-value="selectedTypeRoof.value"
          v-bind="typeRoof"
          @update:model-value="emit('update:selectedTypeRoof', { name: typeRoof.name , value: $event })"
          :ui="{ label: 'font-semibold text-white text-base' }"
        />
      </div>
    </SubStep>
    <SubStep
      :number="2"
      :title="t('step1.substep2')"
    >
      <template v-slot:subtitle>
        {{ t("step1.draw_roof_info") }}
      </template>
      <div v-if="!props.roofSurface">
        <UButton
          icon="i-heroicons-paint-brush-20-solid"
          color="white"
          variant="outline"
          :trailing="false"
          @click="$emit('drawRoof', { area: 'roof'})"
          class="h-8 w-32 md:h-12 md:w-48 mx-auto my-2 bg-purple flex justify-center items-center hover:bg-purple-900 focus:ring-2"
        >
          {{ t("step1.draw_roof") }}
        </UButton>
      </div>
      <div v-else class="flex flex-wrap my-2 md:mt-6 md:mb-4 mx-2">
        <p class="w-2/3 text-base md:text-lg font-semibold">{{ t("step1.useful_surface") }}</p>
        <p class="w-1/3 text-lg md:text-xl font-bold flex justify-end self-center">
          {{ (props.roofSurface).toLocaleString(locale.value) }} m²
        </p>
      </div>
    </SubStep>
    <SubStep
      :number="3"
      :title="t('step1.substep3')"
    >
      <div class="flex flex-row items-center">
        <UToggle
          name="sewageSystem" id="sewageSystem"
          on-icon="i-heroicons-check-20-solid"
          off-icon="i-heroicons-x-mark-20-solid"
          :model-value="selectedSewageSystem"
          :ui="{
            active: 'bg-purple-900 dark:bg-slate-700',
            inactive: 'bg-gray-700 dark:bg-slate-500'
          }"
          @update:model-value="emit('update:selectedSewageSystem', $event )"
        />
        <label for="sewageSystem" class="ml-2 font-semibold text-base">
          {{
            selectedSewageSystem ? t("yes") : t("no")
          }}
        </label>
      </div>
    </SubStep>
  </div>
</template>

<script setup lang="ts">
import { localeHead } from '@nuxtjs/i18n/dist/runtime/routing/head';
import SearchBar from '../map/SearchBar.vue';
import SubStep from './SubStep.vue';

const { t, locale } = useI18n();

const emit = defineEmits([
  "newCenter",
  "update:selectedTypeRoof",
  "update:selectedSewageSystem",
  "select",
  "drawRoof",
]);

const props = defineProps<{
  roofSurface?: number,
  selectedTypeRoof: { name: string, value: number },
  selectedSewageSystem: boolean,
}>();

const typeOfRoofWithCoeff = [
  { label: t("step1.slate"), name: "ardoise", value: 0.8 },
  { label: t("step1.tile"), name: "tuile", value: 0.9 },
  { label: t("step1.flat"), name: "plat", value: 0.6 },
  { label: t("step1.planted"), name: "vegetal", value: 0.4 },
];
</script>
