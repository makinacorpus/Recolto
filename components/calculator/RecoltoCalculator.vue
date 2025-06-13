<template>
  <div
    class="w-full text-white p-4 md:p-6 bg-primary/80 rounded-t-md md:rounded-md"
  >
    <div class="flex flex-col">

      <div ref="step1Ref" id="step1">
        <Step1
          :roof-surface="roofSurface"
          v-model:roof-type="roofType"
          v-model:has-sewage-system="selectedSewageSystem"
          @next="changeStep(1)"
          @new-center="$emit('newCenter', $event)"
          @draw-roof="$emit('drawRoof', $event)"
        />
      </div>

      <div ref="step2Ref" id="step2">
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
          @next="changeStep(2)"
          @previous="changeStep(0)"
        />
      </div>

      <div ref="step3Ref" id="step3">
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
          @previous="changeStep(1)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RoofType } from "~/declaration";
import Step1, { roofTypeList } from "./Step1.vue";
import Step2 from "./Step2.vue";
import Step3 from "./Step3.vue";

const { t } = useI18n();

const emit = defineEmits([
  "drawRoof",
  "drawWaterUsage",
  "disableDraw",
  "newCenter",
]);


const currentStep = defineModel<number>('currentStep', {required: true})
const roofType = ref<RoofType>(roofTypeList[0])
const selectedSewageSystem = ref<boolean>(true)
const surfaceGarden = ref<number>(0)
const surfaceVegetable = ref<number>(0)
const otherNeeds = ref<number>(0)
const toiletsConnected = ref<boolean>(false)
const washingMachineConnected = ref<boolean>(false)
const residentNumber = ref<number>(0)

const step1Ref = ref<HTMLElement | null>(null)
const step2Ref = ref<HTMLElement | null>(null)
const step3Ref = ref<HTMLElement | null>(null)

defineProps<{
  // step 1
  roofSurface: number,
  roofCenter?: L.LatLng | L.LatLngLiteral,
  // step 2
  surfaceGardenDrawn: number,
  surfaceVegetableDrawn: number,
  forceResetInput: null | { area: "garden" | "vegetable", newValue: number },
}>();

const changeStep = (step: number) => {
  currentStep.value = step
  emit("disableDraw");

  if (step === 0) {
    step1Ref.value?.scrollIntoView({ behavior: 'smooth' })
  }
  if (step === 1) {
    step2Ref.value?.scrollIntoView({ behavior: 'smooth' })
  }
  if (step === 2) {
    step3Ref.value?.scrollIntoView({ behavior: 'smooth' })
  }
};

</script>
