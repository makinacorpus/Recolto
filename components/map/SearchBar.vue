<template>
  <div class="flex justify-center items-center gap-2 max-w-full">
    <USelectMenu
      select-class="dark:bg-slate-700"
      class="grow"
      size="xl"
      v-model="currentAddress"
      :searchable=searchAddress
      option-attribute="name"
      searchable-placeholder="Veuillez saisir au moins 3 lettres"
      selected-icon="i-heroicons-map-pin"
      icon="i-heroicons-magnifying-glass-20-solid"
      variant="outline"
    >
      <template #label>
        <span v-if="currentAddress?.properties" class="truncate max-w-[calc(100vw-12rem)] md:max-w-[15rem] lg:max-w-[20rem]">
          {{ currentAddress?.properties?.label }}
        </span>
        <span v-else class="truncate"> {{ t("search.address") }}</span>
      </template>
      <template #option="{ option: searchResults }">
        <span class="truncate">
          {{ searchResults.properties?.label }}
        </span>
      </template>
      <template #option-empty>
        {{ t("search.no_results") }}
      </template>
    </USelectMenu>
    <UButton
      v-if="geolocationApi"
      icon="i-heroicons-viewfinder-circle-solid"
      :class="{
        'text-red-800': geolocateError,
        'text-sky-500': geolocated,
      }"
      v-bind:title=geolocTooltip
      size="xl"
      :loading="geolocating"
      color="white"
      @click="fetchGeolocation"
    />
  </div>
</template>

<script setup lang="ts">
import { ApiAddress } from "~/declaration";

const { t } = useI18n();

const emit = defineEmits<{
  (e: 'new-location', to: { latlng: L.LatLngExpression, accuracy?: number }): void
}>()

const currentAddress = ref<ApiAddress>()
const searchAddress = async (addressToSearch: string) => {
  if (addressToSearch.length >= 3) {
    const response = await fetch(`https://api-adresse.data.gouv.fr/search/?q=${addressToSearch}&limit=3`);
    const res = await response.json();
    return res.features;
  }
  return [];
}
watch(currentAddress, (newAddress) => {
  if (newAddress) {
    emit('new-location', {
      latlng: [newAddress?.geometry.coordinates[1], newAddress?.geometry.coordinates[0]],
    })
  }
})

const geolocationApi = navigator.geolocation
const geolocating = ref(false)
const geolocateError = ref(false)
const geolocated = ref(false)
const geolocTooltip = t("search.geoloc_tooltip");
const fetchGeolocation = () => {
  if (!geolocationApi) {
    return
  }

  geolocating.value = true
  geolocateError.value = false
  geolocated.value = false

  geolocationApi.getCurrentPosition(
    (position) => {
      geolocating.value = false
      geolocated.value = true
      emit('new-location', {
        latlng: [position.coords.latitude, position.coords.longitude],
        accuracy: position.coords.accuracy
      })
    },
    () => {
      geolocating.value = false
      geolocateError.value = true
    }
  )

}
</script>