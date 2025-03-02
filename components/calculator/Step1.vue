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
          v-for="option of roofTypeList"
          :key="option.name"
          input-class="border-purple text-purple dark:border-slate-700 dark:text-slate-700 dark:bg-slate-700"
          v-model="selectedRoofType"
          :value="option.name"
          :label="t(option.label)"
          @update:model-value="onRoofTypeSelection()"
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
          {{ (props.roofSurface).toLocaleString(locale) }}&nbsp;m²
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
          v-model="hasSewageSystem"
          :ui="{
            active: 'bg-purple-900 dark:bg-slate-700',
            inactive: 'bg-gray-700 dark:bg-slate-500'
          }"
        />
        <label for="sewageSystem" class="ml-2 font-semibold text-base">
          {{
            hasSewageSystem ? t("yes") : t("no")
          }}
        </label>
      </div>
    </SubStep>
  </div>
  <div class="flex flex-row mt-2">
    <UButton
      v-if="roofSurface"
      icon="i-heroicons-paint-brush-20-solid"
      color="white"
      variant="outline"
      :trailing="false"
      @click="$emit('drawRoof', { area: 'roof' })"
      class="sm:h-12 sm:w-48 mx-auto my-2 flex justify-center items-center"
      :ui="{ variant: { outline: 'shadow-sm bg-transparent text-white-900 dark:text-white ring-1 ring-inset ring-white dark:ring-white-400 focus:ring-2 focus:ring-purple dark:focus:ring-white hover:bg-purple' }}"
    >
      {{ t("calculator.redraw") }}
    </UButton>
    <UButton
      @click="$emit('next')"
      class="sm:h-12 sm:w-56 mx-auto my-2 bg-purple border border-white flex justify-center items-center disabled:bg-purple-300 ring-purple hover:bg-purple-900 dark:bg-purple dark:text-white dark:hover:bg-purple-900"
      :disabled="!props.roofSurface"
      :title="!props.roofSurface ? 'Vous devez sélectionner une adresse' : ''"
    >
      {{ t("calculator.next_step") }}
    </UButton>
  </div>
</template>

<script lang="ts">
import { RoofType } from '~/declaration';

export const roofTypeList: RoofType[] = [
  { label: 'step1.slate', name: "ardoise", coeff: 0.8 },
  { label: 'step1.tile', name: "tuile", coeff: 0.9 },
  { label: 'step1.flat', name: "plat", coeff: 0.6 },
  { label: 'step1.planted', name: "vegetal", coeff: 0.4 },
];
</script>

<script setup lang="ts">
import SearchBar from '../map/SearchBar.vue';
import SubStep from './SubStep.vue';

const { t, locale } = useI18n();

const emit = defineEmits([
  "newCenter",
  "select",
  "drawRoof",
  "next",
]);

const roofType = defineModel<RoofType>('roofType', {required: true})
const selectedRoofType = ref(roofType.value.name)

const hasSewageSystem = defineModel<boolean>('hasSewageSystem', {required: true})
const props = defineProps<{
  roofSurface?: number,
}>();

const onRoofTypeSelection = () => {
  roofType.value = roofTypeList.find((option) => option.name === selectedRoofType.value) ?? roofTypeList[0]
}
</script>
