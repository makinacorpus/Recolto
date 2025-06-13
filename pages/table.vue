<template>
  <div class="flex flex-col md:flex-row flex-grow h-full">
    <TableForm
      class="w-full md:w-1/2 md:max-w-none z-[1002] overflow-auto md:max-h-full"
      :roof-surface="roofSurface"
      :roof-center="roofCenter"
      :surface-garden-drawn="surfaceGardenDrawn"
      :surface-vegetable-drawn="surfaceVegetableDrawn"
      :force-reset-input="forceResetInput"
      @draw-roof="allowDrawMap($event)"
      @draw-water-usage="allowDrawMap($event)"
      @new-center="center = $event"
    />
    <RecoltoMap
      class="w-full md:w-1/2 h-64 md:h-full"
      :draw-enabled="drawEnabled"
      :center="center"
      @polygon:created="onPolygonCreated"
      @polygon:edited="onPolygonEdited"
      @polygon:deleted="onPolygonDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import L from 'leaflet'
import RecoltoMap from '~/components/map/RecoltoMap.vue'
import TableForm from '~/components/tableCalculator/TableForm.vue'

definePageMeta({
  layout: 'app',
})

const roofCenter = ref<L.LatLng | L.LatLngLiteral>()
const roofSurface = ref(0)

const surfaceGardenDrawn = ref(0)
const surfaceVegetableDrawn = ref(0)

const forceResetInput = ref<null | { area: 'garden' | 'vegetable'; newValue: number }>(null)

const drawEnabled = ref<{ area: 'roof' | 'garden' | 'vegetable' | 'allUsage'; action?: 'draw' | 'clear' }>()

const allowDrawMap = (data?: { area: 'roof' | 'garden' | 'vegetable' | 'allUsage'; action?: 'draw' | 'clear' }) => {
  if (!data) {
    drawEnabled.value = undefined
    return
  }
  if (data.action === 'clear' && data.area === 'garden') {
    surfaceGardenDrawn.value = 0
  }
  if (data.action === 'clear' && data.area === 'vegetable') {
    surfaceVegetableDrawn.value = 0
  }
  if (data.action === 'clear' && data.area === 'allUsage') {
    surfaceGardenDrawn.value = 0
    surfaceVegetableDrawn.value = 0
  }
  drawEnabled.value = data
}

const center = ref<{ latlng: L.LatLng | L.LatLngLiteral; accuracy?: number }>()

function onPolygonCreated(geodesicArea: number, newCentroid: L.LatLng | L.LatLngLiteral, area: string) {
  if (area === 'roof') {
    roofCenter.value = newCentroid
    roofSurface.value = Number(geodesicArea.toFixed(2))
  }
  if (area === 'garden') {
    surfaceGardenDrawn.value = Number((surfaceGardenDrawn.value + geodesicArea).toFixed(2))
  }
  if (area === 'vegetable') {
    surfaceVegetableDrawn.value = Number((surfaceVegetableDrawn.value + geodesicArea).toFixed(2))
  }
}

function onPolygonEdited(totalGeodesicArea: number, area: string) {
  if (area === 'roof') {
    roofSurface.value = Number(totalGeodesicArea.toFixed(2))
  }
  if (area === 'garden') {
    surfaceGardenDrawn.value = Number(totalGeodesicArea.toFixed(2))
  }
  if (area === 'vegetable') {
    surfaceVegetableDrawn.value = Number(totalGeodesicArea.toFixed(2))
  }
}

const onPolygonDeleted = (geodesicArea: number, area: string) => {
  if (area === 'garden') {
    surfaceGardenDrawn.value = Number((surfaceGardenDrawn.value - geodesicArea).toFixed(2))
    forceResetInput.value = {
      area: 'garden',
      newValue: Number((surfaceGardenDrawn.value - geodesicArea).toFixed(2)),
    }
  }
  if (area === 'vegetable') {
    surfaceVegetableDrawn.value = Number((surfaceVegetableDrawn.value - geodesicArea).toFixed(2))
    forceResetInput.value = {
      area: 'vegetable',
      newValue: Number((surfaceVegetableDrawn.value - geodesicArea).toFixed(2)),
    }
  }
}

useHead({
  title: "Récolt'Ô | Table Calculator",
})
</script>
