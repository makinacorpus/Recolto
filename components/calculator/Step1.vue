<template>
  <div class="md:mb-2">
    <div class="bg-purple p-2 md:p-4 rounded-2xl mb-2 md:mb-4 relative">
      <h2
        class="absolute font-semibold -top-2 -left-2 w-8 h-8 text-center rounded-full bg-purple border border-white"
      >
        1
      </h2>
      <h3 class="text-center text-sm md:text-base">Où habitez-vous ?</h3>
      <p class="mt-2 italic text-base/5 hidden md:block">
        Cela permet de récupérer le tarif de l'eau de votre commune.
      </p>
    </div>

    <USelectMenu
      class="flex flex-col w-full"
      select-class="h-12 dark:bg-slate-700"
      :model-value="props.currentAddress"
      @update:model-value="onUpdate($event)"
      @change="emit('search')"
      :searchable=onSearchAddress
      option-attribute="name"
      searchable-placeholder="Veuillez saisir au moins les 3 premières lettres"
      selected-icon="i-heroicons-map-pin"
      icon="i-heroicons-magnifying-glass-20-solid"
      variant="outline"
    >
      <template #label>
      <span v-if="props.currentAddress?.properties" class="truncate">
        {{ props.currentAddress?.properties?.name }}, {{ props.currentAddress?.properties?.postcode }}, {{
          props.currentAddress?.properties?.city
        }}
      </span>
        <span v-else class="truncate">Cherchez votre adresse…</span>
      </template>
      <template #option="{ option: searchResults }">
        <div class="truncate">
          {{ searchResults.properties?.name }}, {{ searchResults.properties?.postcode }}, {{
            searchResults.properties?.city
          }}
        </div>
      </template>
      <template #option-empty>
        Aucun résultat trouvé
      </template>
    </USelectMenu>

    <div class="mt-4" v-if="currentAddress">
      <div class="bg-purple p-2 md:p-4 rounded-2xl mb-2 md:mb-4 relative">
        <h2
          class="absolute font-semibold -top-2 -left-2 w-8 h-8 text-center rounded-full bg-purple shadow-xl border border-white"
        >
          2
        </h2>
        <h3 class="text-center text-sm md:text-base">
          Quel est votre type de toiture ?
        </h3>
        <p class="mt-2 italic text-base/5 hidden sm:block">
          Certains matériaux ou formes de toit perdent ± d’eau selon le volume qu’il tombe. Un coefficient de perte est pris en compte.
        </p>
      </div>
      <div class="mx-4 mb-4">
        <div class="flex flex-row">
          <URadio
            class="w-1/3 text-white font-semibold"
            v-for="typeRoof of typeOfRoofWithCoeff"
            :key="typeRoof.name"
            input-class="border-purple text-purple dark:border-slate-700 dark:text-slate-700 dark:bg-slate-700"
            :model-value="selectedTypeRoof.value"
            v-bind="typeRoof"
            @update:model-value="emit('update:selectedTypeRoof', { name: typeRoof.name , value: $event })"
            :ui="{ label: 'font-semibold text-white text-base' }"
          />
        </div>
      </div>

      <div class="bg-purple p-2 md:p-4 rounded-2xl mb-2 md:mb-4 relative">
        <h2
          class="absolute font-semibold -top-2 -left-2 w-8 h-8 text-center rounded-full bg-purple shadow-xl border border-white"
        >
          3
        </h2>
        <h3 class="text-center text-sm md:text-base">
          Dessiner la pente utile de votre toit
        </h3>

        <p class="mt-2 italic text-base/5 hidden sm:block">
          En fonction de l’implantation de vos gouttières, dessinez la ou les pentes qui desserviront votre récupérateur d’eau.
        </p>
      </div>
      <div v-if="!props.roofSurface">
        <UButton
          icon="i-heroicons-paint-brush-20-solid"
          color="white"
          variant="outline"
          :trailing="false"
          @click="$emit('drawRoof', { area: 'roof'})"
          class="h-8 w-32 md:h-12 md:w-48 mx-auto my-2 bg-purple flex justify-center items-center hover:bg-purple-900 focus:ring-2"
        >
          Dessiner
        </UButton>
      </div>
      <div v-else class="flex flex-wrap my-2 md:mt-6 md:mb-4 mx-2">
        <p class="w-2/3 text-base md:text-lg font-semibold">Surface de pente utile</p>
        <p class="w-1/3 text-lg md:text-xl font-bold flex justify-end self-center">
          {{ (props.roofSurface).toLocaleString("fr-FR") }} m²
        </p>
      </div>

      <div class="bg-purple p-2 md:p-4 rounded-2xl mb-2 md:mb-4 relative">
        <h2
          class="absolute font-semibold -top-2 -left-2 w-8 h-8 text-center rounded-full bg-purple shadow-xl border border-white"
        >
          4
        </h2>
        <h3 class="text-center text-sm md:text-base">
          Votre logement est-il raccordé au tout-à-l'égout ?
        </h3>
      </div>
      <div class="md:mx-4 md:mb-4">
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
              selectedSewageSystem ? "Oui" : "Non"
            }}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type ApiAdresse } from "~/declaration";

const emit = defineEmits([
  "search",
  "update:currentAddress",
  "update:selectedTypeRoof",
  "update:selectedSewageSystem",
  "select",
  "drawRoof",
]);

const props = defineProps<{
  roofSurface?: number,
  currentAddress: string,
  selectedTypeRoof: { name: string, value: number },
  selectedSewageSystem: boolean,
}>();

const onUpdate = (event: ApiAdresse) => {
  emit("update:currentAddress", event);
  emit("select", event);
};

const typeOfRoofWithCoeff = [
  { label: "Ardoise", name: "ardoise", value: 0.8 }, // "slate"
  { label: "Tuile", name: "tuile", value: 0.9 }, // "tile"
  { label: "Plat", name: "plat", value: 0.6 }, // "flat"
];

async function onSearchAddress (addressToSearch: string) {
  const LIMIT = 3;
  if (addressToSearch.length >= 3) {
    const response = await fetch(`https://api-adresse.data.gouv.fr/search/?q=${addressToSearch}&limit=${LIMIT}`);
    const res = await response.json();
    return res.features;
  }
  return [];
}

</script>
