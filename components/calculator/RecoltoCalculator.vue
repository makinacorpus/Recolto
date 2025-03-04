<template>
  <div
    class="w-full max-w-full md:w-[28rem] md:max-w-[28rem] lg:w-[32rem] lg:max-w-[32rem] text-white p-4 md:p-6 bg-primary/80 rounded-t-md md:rounded-md"
  >
    <div class="flex flex-col">
      <header class="mb-4 hidden md:block">
        <h2 class="text-center mb-4">
          {{ t("calculator.steps") }}
        </h2>

        <div class="grid grid-cols-3 justify-items-stretch">
          <button
            v-for="(step, index) in steps"
            :key="step.value"
            @click="changeStep(index)"
            class="min-w-full w-full md:w-24 text-xs md:text-base text-center mx-auto rounded-xl p-2 disabled:text-gray disabled:bg-gray disabled:cursor-not-allowed flex flex-col items-center content-end"
            :class="{
              'bg-white text-purple font-semibold dark:bg-slate-700 dark:text-white': currentStep === index,
            }"
            :disabled="currentStep < index "
          >
            <svg
              v-if="step.icon === 'faucet_drip'"
              :class="[
                currentStep === index ? 'stroke-purple dark:stroke-white' : 'stroke-white dark:stroke-white'
              ]"
              class="w-6 h-6 m-auto"
              xmlns="http://www.w3.org/2000/svg"
              height="8em"
              viewBox="0 0 512 512"
              fill="transparent"
              stroke-width="1.8rem"
            ><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
              <path
                d="M224 0c17.7 0 32 14.3 32 32V44l96-12c17.7 0 32 14.3 32 32s-14.3 32-32 32L256 84l-31-3.9-1-.1-1 .1L192 84 96 96C78.3 96 64 81.7 64 64s14.3-32 32-32l96 12V32c0-17.7 14.3-32 32-32zM0 224c0-17.7 14.3-32 32-32h96l22.6-22.6c6-6 14.1-9.4 22.6-9.4H192V116.2l32-4 32 4V160h18.7c8.5 0 16.6 3.4 22.6 9.4L320 192h32c88.4 0 160 71.6 160 160c0 17.7-14.3 32-32 32H416c-17.7 0-32-14.3-32-32s-14.3-32-32-32H315.9c-20.2 29-53.9 48-91.9 48s-71.7-19-91.9-48H32c-17.7 0-32-14.3-32-32V224zM436.8 423.4c1.9-4.5 6.3-7.4 11.2-7.4s9.2 2.9 11.2 7.4l18.2 42.4c1.8 4.1 2.7 8.6 2.7 13.1V480c0 17.7-14.3 32-32 32s-32-14.3-32-32v-1.2c0-4.5 .9-8.9 2.7-13.1l18.2-42.4z"
              />
            </svg>
            <UIcon
              v-else
              :name="step.icon"
              class="h-6 w-6"
            />
            <span>{{ step.label }}</span>
          </button>
        </div>
      </header>

      <Step1
        v-if="currentStep === 0"
        :roof-surface="roofSurface"
        v-model:roof-type="roofType"
        v-model:has-sewage-system="selectedSewageSystem"
        @next="changeStep(1)"
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
        @previous="changeStep(0)"
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
        @previous="changeStep(1)"
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

const steps = [
  {
    value: 1,
    label: t("calculator.roof"),
    icon: "i-heroicons-home",
  }, {
    value: 2,
    label: t("calculator.habits"),
    icon: "faucet_drip",
  }, {
    value: 3,
    label: t("calculator.results"),
    icon: "i-heroicons-chart-bar-square",
  },
];

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
