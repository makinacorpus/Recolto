<template>
  <div class="z-[1000] flex items-center gap-2">
    <USelectMenu
      class="flex flex-col grow"
      select-class="dark:bg-slate-700"
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
      <span v-if="currentAddress?.properties" class="truncate">
        {{ currentAddress?.properties?.label }}
      </span>
        <span v-else class="truncate">Cherchez une adresse…</span>
      </template>
      <template #option="{ option: searchResults }">
        <div class="truncate">
          {{ searchResults.properties?.label }}
        </div>
      </template>
      <template #option-empty>
        Aucun résultat trouvé
      </template>
    </USelectMenu>
    <UButton
      v-if="geolocationApi"
      icon="i-heroicons-signal"
      :class="{
        'text-red-800': geolocateError,
        'text-sky-500': geolocated,
      }"
      title="Zoomer sur ma position"
      size="xl"
      :loading="geolocating"
      color="white"
      @click="fetchGeolocation"
    />
  </div>
</template>

<script setup lang="ts">
import { ApiAddress } from "~/declaration";

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