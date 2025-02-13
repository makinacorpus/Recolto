<template>
  <SubStep
    :number="4"
    :title="t('step2.substep4')"
  >
    <template v-slot:subtitle>
      {{ t("step2.usage_info") }}
    </template>
    <UsageAccordion :title="t('step2.garden_irrigation')" class="curved-corner-garden">
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
          inputClass="h-10 dark:bg-slate-700 "
          type="number"
          v-model="surfaceGarden"
          @blur="removeDraw('garden')"
        />
        <p>&nbsp;m²</p>
      </div>
    </UsageAccordion>
    <UsageAccordion :title="t('step2.veg_garden_irrigation')" class="curved-corner-vegetable">
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
          inputClass="h-10 dark:bg-slate-700"
          type="number"
          v-model="surfaceVegetable"
          @blur="removeDraw('vegetable')"
        />
        <p>&nbsp;m²</p>
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
              inputClass="h-10 dark:bg-slate-700"
              type="number"
              v-model="residentNumber"
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
          inputClass="h-10 dark:bg-slate-700"
          type="number"
          v-model="exteriorMaintenance"
        />
        <p>&nbsp;{{ t("L_per_year") }}</p>
      </div>
    </UsageAccordion>

    <UButton
      icon="i-heroicons-calculator"
      size="xl"
      color="white"
      variant="outline"
      :trailing="false"
      @click="triggerCompute"
      class="h-12 w-48 mx-auto my-4 bg-purple border border-white flex justify-center items-center disabled:bg-purple-300 ring-purple hover:bg-purple-900"
    >
      {{ t("step2.compute") }}
    </UButton>
  </SubStep>
</template>

<script setup lang="ts">

import SubStep from "./SubStep.vue";
import UsageAccordion from "./UsageAccordion.vue";

const { t } = useI18n();

const emit = defineEmits(["compute", "drawWaterUsage"]);

const props = defineProps<{
  surfaceGardenByDraw: number,
  surfaceVegetableByDraw: number,
  forceResetInput: null | { area: "garden" | "vegetable", newValue: number },
}>();

const surfaceGarden: Ref<number> = ref(props.surfaceGardenByDraw);
const surfaceVegetable: Ref<number> = ref(props.surfaceVegetableByDraw);
const exteriorMaintenance: Ref<number> = ref(0);

const toiletsConnected = ref(false);
const washingMachineConnected = ref(false);
const residentNumber = ref(0)

function triggerCompute () {
  emit("compute", {
    surfaceGarden: surfaceGarden.value,
    surfaceVegetable: surfaceVegetable.value,
    exteriorMaintenance: exteriorMaintenance.value,
    toiletsConnected: toiletsConnected.value,
    washingMachineConnected: washingMachineConnected.value,
    residentNumber: residentNumber.value,
  });
}

const removeDraw = (area: "garden" | "vegetable") => {
  if (props.surfaceGardenByDraw > 0 && props.surfaceGardenByDraw !== surfaceGarden.value) {
    emit("drawWaterUsage", { area: area, action: "clear" });
  }
  if (props.surfaceVegetableByDraw > 0 && props.surfaceVegetableByDraw !== surfaceVegetable.value) {
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

watch(() => props.surfaceGardenByDraw, () => {
  // Avoid to override input value when user update manually surfaceGarden
  if (props.surfaceGardenByDraw > 0) {
    surfaceGarden.value = props.surfaceGardenByDraw;
  }
});

watch(() => props.surfaceVegetableByDraw, () => {
  // Avoid to override input value when user update manually surfaceVegetable
  if (props.surfaceVegetableByDraw > 0) {
    surfaceVegetable.value = props.surfaceVegetableByDraw;
  }
});
</script>

<style scoped>

.curved-corner-garden:before, .curved-corner-vegetable:before {
  content: "";
  display: block;
  width: 25%;
  height: 120%;
  position: absolute;
  border-radius: 32%;
  top: 0;
  left: 0;
}

@media (min-width: 768px) {
  .curved-corner-garden:before, .curved-corner-vegetable:before {
    content: "";
    display: block;
    width: 25%;
    height: 150%;
    position: absolute;
    border-radius: 32%;
    top: 0;
    left: 0;
  }
}

.curved-corner-garden:before {
  box-shadow: -50px -50px 0 0 #6ce868;
}

.curved-corner-vegetable:before {
  box-shadow: -50px -50px 0 0 #f47e27;
}
</style>
