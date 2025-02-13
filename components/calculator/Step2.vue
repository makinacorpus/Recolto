<template>
  <SubStep
    :number="4"
    title="Quelles sont vos usages de l'eau&nbsp;?"
  >
    <template v-slot:subtitle>
      La connaissance de vos habitudes de consommation permet d'affiner la taille de votre récupérateur d'eau.
    </template>
    <UsageAccordion title="Usages extérieurs">
      <div class="flex flex-col">
        <div class="flex flex-row items-center text-base text-center my-2">
          <p class="mb-2 mx-2 w-3/6">Arrosage du jardin</p>
          <UButton
            color="white"
            label="Dessiner"
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
            </template>
          </UButton>
          <p class="w-1/6">ou</p>
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
        </div>
        <div class="flex flex-row items-center text-base text-center my-2">
          <p class="mb-2 mx-2 w-3/6">Arrosage du potager</p>
          <UButton
            color="white"
            label="Dessiner"
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
            </template>
          </UButton>
          <p class="w-1/6">ou</p>
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
        </div>
      </div>
    </UsageAccordion>
    <UsageAccordion title="Usages intérieurs">
      <div class="flex flex-col items-start text-base text-left">
        <p class="mb-2">Votre récupérateur d'eau sera-t-il rattaché&nbsp;:</p>
        <ul class="list-disc pl-5 mb-4">
          <li>
            <span class="mr-2">À des toilettes&nbsp;?</span>
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
              {{ toiletsConnected ? "Oui" : "Non" }}
            </label>
          </li>
          <li>
            <span class="mr-2">À une machine à laver&nbsp;?</span>
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
              {{ washingMachineConnected ? "Oui" : "Non" }}
            </label>
          </li>
        </ul>
        <div class="inline" for="residentNumber">
          <p class="mb-2">De combien de personnes est composé votre foyer&nbsp;?</p>
          <div
            class="w-full flex items-center justify-center"
          >
            <UInput
              inputClass="h-10 dark:bg-slate-700"
              type="number"
              v-model="residentNumber"
            />
            <p>&nbsp;personnes</p>
          </div>
        </div>
      </div>
    </UsageAccordion>
    <UsageAccordion title="Autres usages">
      <template v-slot:help>
        Par exemple&nbsp;: pour l'arrossage de vos plantes intérieures, le lavage
        des sols, le nettoyage d'équipement ou d'outil…
      </template>
      <div
        class="w-full flex items-center justify-center"
      >
        <UInput
          inputClass="h-10 dark:bg-slate-700"
          type="number"
          v-model="exteriorMaintenance"
        />
        <p>&nbsp;L/an</p>
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
      Calculer
    </UButton>
  </SubStep>
</template>

<script setup lang="ts">

import SubStep from "./SubStep.vue";
import UsageAccordion from "./UsageAccordion.vue";

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
