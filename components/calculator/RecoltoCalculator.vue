<template>
  <div
    class="w-full max-w-full md:w-[28rem] md:max-w-[28rem] lg:w-[32rem] lg:max-w-[32rem] text-white p-4 md:p-6 bg-primary/80 rounded-t-md md:rounded-md"
  >
    <div class="flex flex-col">
      <!-- Step navigation removed -->

      <Step1
        v-if="currentStep === 0"
        :roof-surface="roofSurface"
        v-model:roof-type="roofType"
        v-model:has-sewage-system="selectedSewageSystem"
        @new-center="$emit('newCenter', $event)"
        @draw-roof="$emit('drawRoof', $event)"
      />
      <Step2
        v-else-if="currentStep === 1"
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
      />

      <Step3
        v-else-if="currentStep === 2"
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
};

</script>
