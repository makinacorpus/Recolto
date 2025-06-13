<template>
  <div class="flex flex-col gap-4 text-white p-4 md:p-6 bg-primary/80 rounded-md">
    <Step1
      :roof-surface="roofSurface"
      v-model:roof-type="roofType"
      v-model:has-sewage-system="selectedSewageSystem"
      @new-center="$emit('newCenter', $event)"
      @draw-roof="$emit('drawRoof', $event)"
    />
    <Step2
      v-model:surface-garden="surfaceGarden"
      v-model:surface-vegetable="surfaceVegetable"
      v-model:other-needs="otherNeeds"
      v-model:toilets-connected="toiletsConnected"
      v-model:washing-machine-connected="washingMachineConnected"
      v-model:resident-number="residentNumber"
      :surface-garden-drawn="surfaceGardenDrawn"
      :surface-vegetable-drawn="surfaceVegetableDrawn"
      :force-reset-input="forceResetInput"
      @draw-water-usage="$emit('drawWaterUsage', $event)"
    />
    <Step3
      :roof-surface="roofSurface"
      :roof-absorbtion-coeff="roofType.coeff"
      :roof-center="roofCenter"
      :garden-surface="surfaceGarden"
      :vegetable-surface="surfaceVegetable"
      :other-needs="otherNeeds"
      :toilets-connected="toiletsConnected"
      :washing-machine-connected="washingMachineConnected"
      :resident-number="residentNumber"
      :has-sewage-system="selectedSewageSystem"
    />
  </div>
</template>

<script setup lang="ts">
import L from 'leaflet'
import { RoofType } from '~/declaration'
import Step1, { roofTypeList } from './calculator/Step1.vue'
import Step2 from './calculator/Step2.vue'
import Step3 from './calculator/Step3.vue'

const emit = defineEmits([
  'drawRoof',
  'drawWaterUsage',
  'newCenter'
])

const props = defineProps<{
  roofSurface: number
  roofCenter?: L.LatLng | L.LatLngLiteral
  surfaceGardenDrawn: number
  surfaceVegetableDrawn: number
  forceResetInput: null | { area: 'garden' | 'vegetable'; newValue: number }
}>()

const roofType = ref<RoofType>(roofTypeList[0])
const selectedSewageSystem = ref(true)
const surfaceGarden = ref(0)
const surfaceVegetable = ref(0)
const otherNeeds = ref(0)
const toiletsConnected = ref(false)
const washingMachineConnected = ref(false)
const residentNumber = ref(0)
</script>

<style scoped>
.bg-purple { @apply bg-purple-700; }
</style>
