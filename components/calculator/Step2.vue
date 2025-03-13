<template>
  <SubStep
    :number="4"
    :title="t('step2.substep4')"
  >
    <template v-slot:subtitle>
      {{ t("step2.usage_info") }}
    </template>
    <UsageAccordion :title="t('step2.exterior_uses')">
      <div class="flex flex-col">
        <p class="mb-2 mx-2 justify-center text-base text-center my-2">
          <span class="garden-icon mx-2">⬤</span>
          {{ t('step2.garden_irrigation') }}
        </p>
        <div class="flex flex-row items-center text-base text-center my-2">
          <UButton
        color="white"
        variant="outline"
        :trailing="false"
        @click="$emit('drawWaterUsage', { area: 'garden', action: 'draw' })"
        class="h-10 w-2/6 text-sm sm:text-base mx-auto bg-purple flex justify-center items-center hover:bg-purple-900 focus:ring-2 z-50"
      >
        <template #leading>
          <UIcon
            class="h-5 w-5 hidden sm:block"
            name="i-heroicons-paint-brush-20-solid"
          />
          {{ t("step2.draw") }}
        </template>
      </UButton>
      <p class="w-1/6">{{ t("or") }}</p>
      <div
        class="w-3/6 flex items-center"
      >
        <UInput
          inputClass="h-10 dark:bg-slate-700 bg-white"
          type="number"
          :color="isErrorSurfaceGarden ? 'red' : 'white'"
          :min="0"
          v-model.number="surfaceGarden"
          @blur="removeDraw('garden')"
        />
        <p>&nbsp;m²</p>
      </div>
        </div>
        <p class="mb-2 mx-2 justify-center items-center text-base text-center my-2">
          <span class="vegetable-icon mx-2">⬤</span>
          {{ t('step2.veg_garden_irrigation') }}
        </p>
        <div class="flex flex-row items-center text-base text-center my-2">
          <UButton
        color="white"
        variant="outline"
        :trailing="false"
        @click="$emit('drawWaterUsage', { area: 'vegetable', action: 'draw' })"
        class="h-10 w-2/6 text-sm sm:text-base mx-auto bg-purple flex justify-center items-center hover:bg-purple-900 focus:ring-2 z-50"
      >
        <template #leading>
          <UIcon
            class="h-5 w-5 hidden sm:block"
            name="i-heroicons-paint-brush-20-solid"
          />
          {{ t("step2.draw") }}
        </template>
      </UButton>
      <p class="w-1/6">{{ t("or") }}</p>
      <div
        class="w-3/6 flex items-center"
      >
        <UInput
          inputClass="h-10 dark:bg-slate-700 bg-white"
          type="number"
          :min="0"
          :color="isErrorSurfaceVegetable ? 'red' : 'white'"
          v-model.number="surfaceVegetable"
          @blur="removeDraw('vegetable')"
        />
        <p>&nbsp;m²</p>
      </div>
        </div>
      </div>
    </UsageAccordion>
    <UsageAccordion :title="t('step2.interior_uses')">
      <div class="flex flex-col items-start text-base text-left">
        <p class="mb-2">{{ t("step2.interior_uses_prompt") }}</p>
        <ul class="list-disc pl-5 mb-4">
          <li>
            <span class="mr-2">{{ t("step2.toilets") }}</span>
            <UToggle
              class="mr-2"
              name="toiletsConnected" id="toiletsConnected"
              on-icon="i-heroicons-check-20-solid"
              off-icon="i-heroicons-x-mark-20-solid"
              v-model="toiletsConnected"
              :ui="{
                active: 'bg-purple-900 dark:bg-slate-700',
                inactive: 'bg-gray-700 dark:bg-slate-500'
              }"
            />
            <label for="toiletsConnected">
              {{ toiletsConnected ? t("yes") : t("no") }}
            </label>
          </li>
          <li>
            <span class="mr-2">{{ t("step2.washing_machine") }}</span>
            <UToggle
              class="mr-2"
              name="washingMachineConnected" id="washingMachineConnected"
              on-icon="i-heroicons-check-20-solid"
              off-icon="i-heroicons-x-mark-20-solid"
              v-model="washingMachineConnected"
              :ui="{
                active: 'bg-purple-900 dark:bg-slate-700',
                inactive: 'bg-gray-700 dark:bg-slate-500'
              }"
            />
            <label for="washingMachineConnected">
              {{ washingMachineConnected ? t("yes") : t("no") }}
            </label>
          </li>
        </ul>
        <div class="inline" for="residentNumber">
          <p class="mb-2">{{ t("step2.occupancy") }}</p>
          <div
            class="w-full flex items-center justify-center"
          >
            <UInput
              inputClass="h-10 dark:bg-slate-700 bg-white"
              type="number"
              :min="0"
              :color="isErrorResidentNumber ? 'red' : 'white'"
              v-model.number="residentNumber"
            />
            <p> {{ t("step2.persons") }}</p>
          </div>
        </div>
      </div>
    </UsageAccordion>
    <UsageAccordion :title="t('step2.other_uses')">
      <template v-slot:help>
        {{ t("step2.other_uses_info") }}
      </template>
      <div
        class="w-full flex items-center justify-center"
      >
        <UInput
          inputClass="h-10 dark:bg-slate-700 bg-white"
          type="number"
          :min="0"
          :color="isErrorExteriorMaintenance ? 'red' : 'white'"
          v-model.number="otherNeeds"
        />
        <p>&nbsp;{{ t("L_per_year") }}</p>
      </div>
    </UsageAccordion>

    <div class="flex flex-row mt-2 justify-between">
      <UButton
        size="xl"
        color="white"
        variant="outline"
        :trailing="false"
        @click="$emit('previous')"
        class="sm:h-12 sm:w-48 my-2 flex justify-center items-center"
        :ui="{ variant: { outline: 'shadow-sm bg-transparent text-white-900 dark:text-white ring-1 ring-inset ring-white dark:ring-white-400 focus:ring-2 focus:ring-purple dark:focus:ring-white hover:bg-purple' }}"
      >
        {{ t("calculator.previous_step") }}
      </UButton>
      <UButton
        icon="i-heroicons-calculator"
        size="xl"
        color="white"
        variant="outline"
        :trailing="false"
        @click="$emit('next')"
        class="sm:h-12 sm:w-48 my-2 bg-purple border border-white flex justify-center items-center disabled:bg-purple-300 ring-purple hover:bg-purple-900"
      >
        {{ t("step2.compute") }}
      </UButton>
    </div>

  </SubStep>
</template>

<script setup lang="ts">

import SubStep from "./SubStep.vue";
import UsageAccordion from "./UsageAccordion.vue";

const { t } = useI18n();

const emit = defineEmits(["next", "drawWaterUsage", "previous"]);

const surfaceGarden = defineModel<number>('surfaceGarden', {required: true})
const surfaceVegetable = defineModel<number>('surfaceVegetable', {required: true})
const otherNeeds = defineModel<number>('otherNeeds', {required: true})
const toiletsConnected = defineModel<boolean>('toiletsConnected', {required: true})
const washingMachineConnected = defineModel<boolean>('washingMachineConnected', {required: true})
const residentNumber = defineModel<number>('residentNumber', {required: true})

const props = defineProps<{
  surfaceGardenDrawn: number,
  surfaceVegetableDrawn: number,
  forceResetInput: null | { area: "garden" | "vegetable", newValue: number },
}>();
const isErrorSurfaceGarden = computed(() => {
  return surfaceGarden.value < 0;
})
const isErrorSurfaceVegetable = computed(() => {
  return surfaceVegetable.value < 0;
})
const isErrorResidentNumber = computed(() => {
  return residentNumber.value < 0;
})
const isErrorExteriorMaintenance = computed(() => {
  return otherNeeds.value < 0;
})
const isNotOk = computed(() => {
  return isErrorExteriorMaintenance.value || isErrorResidentNumber.value || isErrorSurfaceVegetable.value || isErrorSurfaceGarden.value;
})
const removeDraw = (area: "garden" | "vegetable") => {
  if (props.surfaceVegetableDrawn > 0 && props.surfaceVegetableDrawn !== surfaceGarden.value) {
    emit("drawWaterUsage", { area: area, action: "clear" });
  }
  if (props.surfaceGardenDrawn > 0 && props.surfaceGardenDrawn !== surfaceVegetable.value) {
    emit("drawWaterUsage", { area: area, action: "clear" });
  }
};

watch(() => props.forceResetInput, () => {
  // N.B. Indeed newValue is never used, but it is necessary to trigger watch :)
  // Force reset when user removed all area via button
  if (props.forceResetInput?.area === "garden") {
    surfaceGarden.value = 0;
  }
  if (props.forceResetInput?.area === "vegetable") {
    surfaceVegetable.value = 0;
  }
});

watch(() => props.surfaceGardenDrawn, () => {
  // Avoid to override input value when user update manually surfaceGarden
  if (props.surfaceGardenDrawn > 0) {
    surfaceGarden.value = props.surfaceGardenDrawn;
  }
});

watch(() => props.surfaceVegetableDrawn, () => {
  // Avoid to override input value when user update manually surfaceVegetable
  if (props.surfaceVegetableDrawn > 0) {
    surfaceVegetable.value = props.surfaceVegetableDrawn;
  }
});
</script>

<style scoped>

.garden-icon {
  color: #6ce868;
}

.vegetable-icon {
  color: #f47e27;
}
</style>
