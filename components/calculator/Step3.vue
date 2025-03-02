<template>
  <SubStep
    :number="5"
    :title="t('step3.estimation')"
  >
    <div class="-mx-2">
      <div v-if="!loading" class="flex flex-wrap">
        <div class="w-2/3 text-md lg:text-lg font-semibold mb-2 self-center">
          <div class="flex">
            <p class="w-auto md:w-5/6">{{ t("step3.optimal_volume") }}</p>
            <InformationTooltip class="hidden md:ml-2 md:w-1/6 md:block md:self-center">
                <p v-html='t("step3.optimal_volume_info")'></p>
            </InformationTooltip>
          </div>
        </div>
        <div class="w-1/3 text-xl md:text-2xl font-bold flex justify-end self-center">
          {{ idealCapacity?.toLocaleString(locale) ?? '-' }} L
        </div>

        <div class="w-2/3 text-md lg:text-lg font-semibold mb-2 self-center">
          {{ t("step3.estim_saving") }}
        </div>
        <div class="w-1/3 text-xl md:text-2xl font-bold flex justify-end self-center">
          {{ savingPerYear.toLocaleString(locale) }} {{ t("euro_per_year")}}
        </div>

        <hr class="border border-t border-purple w-full my-2">

        <div class="w-2/3 text-sm lg:text-base font-semibold mb-2 self-center">
          <div class="flex">
            <p class="w-auto md:w-5/6">
              {{ t("step3.water_price") }} {{ t('step3.water_price_division.' + (waterPrice?.division ?? 'national')) }} {{ t("in") }} {{
                waterPrice?.year
              }}
            </p>

            <InformationTooltip class="hidden md:ml-2 md:w-1/6 md:block md:self-center">
              <p class="text-sm m-1">
                {{ t("step3.water_price_info") }}
                <a href="https://services.eaufrance.fr/carte-interactive" target="_blank" rel="noopener" class="underline" >services.eaufrance.fr</a>
              </p>
            </InformationTooltip>
          </div>
        </div>
        <div class="w-1/3 text-base md:text-lg font-bold flex justify-end self-center">
          {{ (waterPrice?.price ?? '-').toLocaleString(locale) }} €/m³
        </div>

        <div class="w-2/3 text-sm lg:text-base font-semibold mb-2 self-center">
          {{ t("step3.needs") }}
        </div>
        <div class="w-1/3 text-base md:text-lg font-bold flex justify-end self-center">
          {{ waterNeedsPerYear.toLocaleString(locale) }}&nbsp;{{ t("L_per_year") }}
        </div>
      </div>
      <div v-if="!loading && !idealCapacity">
        {{ t("step3.estimation_failure") }}
      </div>
      <div v-if="loading">
        <div class="flex items-center space-x-4 mt-2">
          <USkeleton class="h-12 w-12" :ui="{ rounded: 'rounded-full' }" />
          <div class="space-y-2">
            <USkeleton class="h-4 w-[250px]" />
            <USkeleton class="h-4 w-[200px]" />
          </div>
        </div>
        <div class="flex items-center space-x-4 mt-2">
          <USkeleton class="h-12 w-12" :ui="{ rounded: 'rounded-full' }" />
          <div class="space-y-2">
            <USkeleton class="h-4 w-[250px]" />
            <USkeleton class="h-4 w-[200px]" />
          </div>
        </div>
      </div>

      <hr class="border border-t border-purple w-full my-2">

      <div v-if="!loading" class="w-full">
        <h3
          class="font-semibold text-center text-white"
        >
          {{ t("step3.needs_analysis") }}
        </h3>
        <div class="flex w-full gap-1 sm:gap-2">
          <UButton
            variant="outline"
            :trailing="false"
            @click="selectedScenario = 'nearest'"
            class="my-3 md:my-2 bg-purple border border-white flex justify-center items-center text-white disabled:bg-purple-300 ring-purple hover:bg-purple-900 dark:bg-purple dark:text-white dark:hover:bg-purple-900 flex-1 px-0.5"
            :class="{'bg-purple-200 text-purple hover:bg-purple-200 dark:bg-purple-200 dark:text-purple dark:hover:bg-purple-200': selectedScenario === 'nearest'}"
          >
            <div class="flex flex-col text-xs md:text-base">
              <span>{{ t("step3.last_known") }}</span>
              <span>{{ rainDataYearsInfo?.nearest }}</span>
            </div>
          </UButton>
          <UButton
            variant="outline"
            :trailing="false"
            @click="selectedScenario = 'driest'"
            class="my-3 md:my-2 bg-purple border border-white flex justify-center items-center text-white disabled:bg-purple-300 ring-purple hover:bg-purple-900 dark:bg-purple dark:text-white dark:hover:bg-purple-900 flex-1 px-0.5"
            :class="{'bg-purple-200 text-purple hover:bg-purple-200 dark:bg-purple-200 dark:text-purple dark:hover:bg-purple-200': selectedScenario === 'driest'}"
          >
            <div class="flex flex-col text-xs md:text-base">
              <span>{{ t("step3.driest") }}</span>
              <span>{{ rainDataYearsInfo?.driest }}</span>
            </div>
          </UButton>
          <UButton
            variant="outline"
            :trailing="false"
            @click="selectedScenario = 'wettest'"
            class="my-3 md:my-2 bg-purple border border-white flex justify-center items-center text-white disabled:bg-purple-300 ring-purple hover:bg-purple-900 dark:bg-purple dark:text-white dark:hover:bg-purple-900 flex-1 px-0.5"
            :class="{'bg-purple-200 text-purple hover:bg-purple-200 dark:bg-purple-200 dark:text-purple dark:hover:bg-purple-200': selectedScenario === 'wettest'}"
          >
            <div class="flex flex-col text-xs md:text-base">
              <span>{{ t("step3.wettest") }}</span>
              <span>{{ rainDataYearsInfo?.wettest }}</span>
            </div>
          </UButton>
        </div>
      </div>
      <Step3Chart
        v-if="!loading"
        :scenario="selectedScenario"
        :roof-potential-water-collect="chartData?.roofPotentialWaterCollect"
        :water-collector-level="chartData?.waterCollectorLevel"
        :water-needs="chartData?.waterNeeds"
      />
      <div v-if="!loading" class="text-xs font-medium">
        <p>
          Cette estimation se base sur les données
          <a
            href="https://meteo.data.gouv.fr/"
            target="_blank"
            rel="noopener"
          >
            Météo France
          </a>
          de 1960 à {{ rainDataYearsInfo?.nearest }}.
        </p>
      </div>
    </div>
  </SubStep>
</template>

<script setup lang="ts">
import L from "leaflet";
import InformationTooltip from "./InformationTooltip.vue";
import Step3Chart from "./Step3Chart.vue";
import SubStep from "./SubStep.vue";
import { RainData, WaterPrice, WaterNeedsByMonth, PrecipitationScenario, RoofType } from "~/declaration";
import { getWaterCollectorEvolutionPerMonth } from "~/utils/waterCollectorCapacity";

const { t, locale } = useI18n();

const props = defineProps<{
  roofSurface: number,
  roofAbsorbtionCoeff: number,
  roofCenter?: L.LatLng | L.LatLngLiteral,
  gardenSurface: number,
  vegetableSurface: number,
  otherNeeds: number,
  toiletsConnected: boolean,
  washingMachineConnected: boolean,
  residentNumber: number,
  hasSewageSystem: boolean,
}>();

const loading = ref(true);
const rainData = ref<RainData>();
const waterPrice = ref<WaterPrice>();
const waterNeeds = ref<WaterNeedsByMonth>();
const idealCapacity = ref<number>();

watch(props, async (props) => {
  loading.value = true;

  if (!props.roofCenter) {
    throw 'No centroid !'
  }

  rainData.value = await getRainData(props.roofCenter)
  waterPrice.value = await getWaterPrice(props.roofCenter, props.hasSewageSystem)

  waterNeeds.value = getWaterNeedsByMonth(
    props.gardenSurface,
    props.vegetableSurface,
    props.otherNeeds,
    props.toiletsConnected,
    props.washingMachineConnected,
    props.residentNumber,
  );

  idealCapacity.value = estimateWaterCollectorCapacity(
    waterNeeds.value,
    rainData.value,
    props.roofSurface,
    props.roofAbsorbtionCoeff
  )

  loading.value = false;
}, {immediate: true})

const selectedScenario = ref<PrecipitationScenario>("nearest")
const rainDataYearsInfo = computed(() => rainData.value ? getRainDataYearsInfo(rainData.value) : undefined)

const chartData = computed(() => {
  if (idealCapacity.value
  && waterNeeds.value
  && rainDataYearsInfo.value?.[selectedScenario.value]
  && rainData.value
) {
    const yearRainData = getYearRainData(
      rainDataYearsInfo.value[selectedScenario.value] as string,
      rainData.value
    )
    return {
      waterNeeds: waterNeeds.value,
      ...getWaterCollectorEvolutionPerMonth(
        idealCapacity.value,
        waterNeeds.value,
        yearRainData,
        props.roofSurface,
        props.roofAbsorbtionCoeff
      )
    }
  }
})

const waterNeedsPerYear = computed(() => {
  if (!waterNeeds.value) {
    return '-'
  }
  const needs = waterNeeds.value.reduce((a, b) => a + b, 0)
  return Math.round(needs / 100) * 100
})

const savingPerYear = computed(() => {
  if (!chartData.value?.rainWaterConsumption || !waterPrice.value) {
    return '-'
  }
  const savings = chartData.value?.rainWaterConsumption.reduce((a, b) => a + b, 0) * waterPrice.value.price / 1000
  return Math.round(savings)
})

</script>
