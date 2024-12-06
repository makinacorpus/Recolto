<template>
  <div class="bg-purple p-4 rounded-2xl mb-4 relative">
    <h2
      class="absolute font-semibold -top-2 -left-2 w-8 h-8 text-center rounded-full bg-purple shadow-xl border border-white"
    >
      5
    </h2>
    <h3 class="text-center text-sm md:text-base">Quelles sont vos usages de l'eau ?</h3>
    <p class="mt-2 italic text-base/5 hidden sm:block">
      La connaissance de vos habitudes de consommation permet d'affiner la taille de votre récupérateur d'eau.
    </p>
  </div>

  <UButton
    @click.self="usageToggle['surfaceGarden'] = !usageToggle['surfaceGarden']"
    class="bg-cool rounded-lg border-2 w-full flex flex-col relative mb-2 overflow-hidden curved-corner-garden dark:bg-cool dark:text-white"
    :class="{
      'hover:bg-purple-300/50 dark:hover:bg-purple-300/50': usageToggle['surfaceGarden'],
      'hover:bg-purple-900 dark:hover:bg-purple-900': !usageToggle['surfaceGarden'],
    }"
  >
    <UIcon
      v-if="usageToggle['surfaceGarden']"
      name="i-heroicons-check-circle"
      class="absolute top-0 right-0 w-8 h-8"
    />
    <div
      class="flex text-lg my-2"
      @click.self="usageToggle['surfaceGarden'] = !usageToggle['surfaceGarden']"
    >
      Arrosage du jardin
    </div>
    <div v-if="usageToggle['surfaceGarden']" class="flex flex-row w-11/12 items-center my-2">
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
        <p> m²</p>
      </div>
    </div>
  </UButton>
  <UButton
    @click.self="usageToggle['surfaceVegetable'] = !usageToggle['surfaceVegetable']"
    class="bg-cool rounded-lg border-2 w-full flex flex-col relative mb-2 overflow-hidden curved-corner-vegetable dark:bg-cool dark:text-white"
    :class="{
      'hover:bg-purple-300/50 dark:hover:bg-purple-300/50': usageToggle['surfaceVegetable'],
      'hover:bg-purple-900 dark:hover:bg-purple-900': !usageToggle['surfaceVegetable'],
    }"
  >
    <UIcon
      v-if="usageToggle['surfaceVegetable']"
      name="i-heroicons-check-circle"
      class="absolute top-0 right-0 w-8 h-8"
    />
    <div
      class="flex text-lg my-2"
      @click.self="usageToggle['surfaceVegetable'] = !usageToggle['surfaceVegetable']"
    >
      Arrosage du potager
    </div>
    <div v-if="usageToggle['surfaceVegetable']" class="flex flex-row w-11/12 items-center my-2">
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
        <p> m²</p>
      </div>
    </div>
  </UButton>
  <UButton
    @click.self="usageToggle['exteriorMaintenance'] = !usageToggle['exteriorMaintenance']"
    class="bg-cool rounded-lg border-2 w-full flex flex-col relative mb-2 dark:bg-cool dark:text-white "
    :class="{
      'hover:bg-purple-300/50 dark:hover:bg-purple-300/50': usageToggle['exteriorMaintenance'],
      'hover:bg-purple-900 dark:hover:bg-purple-900': !usageToggle['exteriorMaintenance'],
    }"
  >
    <UIcon
      v-if="usageToggle['exteriorMaintenance']"
      name="i-heroicons-check-circle"
      class="absolute top-0 right-0 w-8 h-8"
    />
    <div
      class="flex text-lg my-2"
      @click.self="usageToggle['exteriorMaintenance'] = !usageToggle['exteriorMaintenance']"
    >
      <p
        class="w-full"
        @click.self="usageToggle['exteriorMaintenance'] = !usageToggle['exteriorMaintenance']"
      >
        Autres usages
      </p>
      <UPopover
        class="hidden md:ml-2 md:w-1/6 md:block md:self-center" mode="hover"
        :ui="{width: 'max-w-md', background: 'bg-purple dark:bg-gray-900'}"
      >
        <UIcon name="i-heroicons-information-circle" class="w-6 h-6" />
        <template #panel>
          <p class="text-sm m-1">
            Par exemple : pour l'arrossage de vos plantes intérieures, le lavage des sols, le nettoyage d'équipement ou d'outil…
          </p>
        </template>
      </UPopover>
    </div>
    <div v-if="usageToggle['exteriorMaintenance']" class="flex flex-row w-11/12 items-center my-2">
      <div
        class="w-full flex items-center justify-center"
      >
        <UInput
          inputClass="h-10 dark:bg-slate-700"
          type="number"
          v-model="exteriorMaintenance"
        />
        <p> L/an</p>
      </div>
    </div>
  </UButton>

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
</template>

<script setup lang="ts">

import { watch, Ref } from "vue";

const emit = defineEmits(["compute", "drawWaterUsage"]);

const props = defineProps<{
  surfaceGardenByDraw: number,
  surfaceVegetableByDraw: number,
  forceResetInput: null | { area: "garden" | "vegetable", newValue: number },
}>();

const surfaceGarden: Ref<number> = ref(props.surfaceGardenByDraw);
const surfaceVegetable: Ref<number> = ref(props.surfaceVegetableByDraw);
const exteriorMaintenance: Ref<number> = ref(0);

const usageToggle: Ref<{
  surfaceGarden: boolean,
  surfaceVegetable: boolean,
  exteriorMaintenance: boolean
}> = ref({
  surfaceGarden: false,
  surfaceVegetable: false,
  exteriorMaintenance: false,
});

function triggerCompute () {
  emit("compute", {
    surfaceGarden: usageToggle.value.surfaceGarden ? surfaceGarden.value : 0,
    surfaceVegetable: usageToggle.value.surfaceVegetable ? surfaceVegetable.value : 0,
    exteriorMaintenance: usageToggle.value.exteriorMaintenance ? exteriorMaintenance.value : 0,
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
