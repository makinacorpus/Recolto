<template>
  <SubStep
    :number="5"
    :title="t('step3.estimation')"
  >
    <div class="-mx-2">
      <div v-if="result && !loading" class="flex flex-wrap">
        <div class="w-2/3 text-md lg:text-lg font-semibold mb-2 self-center">
          <div class="flex">
            <p class="w-auto md:w-5/6">{{ t("step3.optimal_volume") }}</p>
            <InformationTooltip class="hidden md:ml-2 md:w-1/6 md:block md:self-center">
                <p v-html='t("step3.optimal_volume_info")'></p>
            </InformationTooltip>
          </div>
        </div>
        <div class="w-1/3 text-xl md:text-2xl font-bold flex justify-end self-center">
          {{ idealCapacity }} L
        </div>

        <div class="w-2/3 text-md lg:text-lg font-semibold mb-2 self-center">
          {{ t("step3.estim_saving") }}
        </div>
        <div class="w-1/3 text-xl md:text-2xl font-bold flex justify-end self-center">
          {{ (result?.savingForLastKnownYear ?? '').toLocaleString(locale.value) }} {{ t("euro_per_year")}}
        </div>

        <hr class="border border-t border-purple w-full my-2">

        <div class="w-2/3 text-sm lg:text-base font-semibold mb-2 self-center">
          <div class="flex">
            <p class="w-auto md:w-5/6">
              {{ t("step3.water_price") }} {{ getDivisionForWaterPrice }} {{ t("in") }} {{
                result.waterPrice.year
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
          {{ (result.waterPrice.price).toLocaleString(locale.value) }} €/m³
        </div>

        <div class="w-2/3 text-sm lg:text-base font-semibold mb-2 self-center">
          {{ t("step3.needs") }}
        </div>
        <div class="w-1/3 text-base md:text-lg font-bold flex justify-end self-center">
          {{ waterNeeds }}&nbsp;{{ t("L_per_year") }}
        </div>
      </div>
      <div v-if="!result && !loading">
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

      <div v-if="result && !loading" class="w-full">
        <h3
          class="font-semibold text-center text-white"
        >
          {{ t("step3.needs_analysis") }}
        </h3>
        <div class="flex w-full gap-1 sm:gap-2">
          <UButton
            variant="outline"
            :trailing="false"
            @click="selectedScenario('recently')"
            class="my-3 md:my-2 bg-purple border border-white flex justify-center items-center text-white disabled:bg-purple-300 ring-purple hover:bg-purple-900 dark:bg-purple dark:text-white dark:hover:bg-purple-900 flex-1 px-0.5"
            :class="{'bg-purple-200 text-purple hover:bg-purple-200 dark:bg-purple-200 dark:text-purple dark:hover:bg-purple-200': graphToDisplay === 'recently'}"
          >
            <div class="flex flex-col text-xs md:text-base">
              <span>{{ t("step3.last_known") }}</span>
              <span>{{ props.result?.lastKnownYear }}</span>
            </div>
          </UButton>
          <UButton
            variant="outline"
            :trailing="false"
            @click="selectedScenario('driest')"
            class="my-3 md:my-2 bg-purple border border-white flex justify-center items-center text-white disabled:bg-purple-300 ring-purple hover:bg-purple-900 dark:bg-purple dark:text-white dark:hover:bg-purple-900 flex-1 px-0.5"
            :class="{'bg-purple-200 text-purple hover:bg-purple-200 dark:bg-purple-200 dark:text-purple dark:hover:bg-purple-200': graphToDisplay === 'driest'}"
          >
            <div class="flex flex-col text-xs md:text-base">
              <span>{{ t("step3.driest") }}</span>
              <span>{{ props.result?.driestYear }}</span>
            </div>
          </UButton>
          <UButton
            variant="outline"
            :trailing="false"
            @click="selectedScenario('wettest')"
            class="my-3 md:my-2 bg-purple border border-white flex justify-center items-center text-white disabled:bg-purple-300 ring-purple hover:bg-purple-900 dark:bg-purple dark:text-white dark:hover:bg-purple-900 flex-1 px-0.5"
            :class="{'bg-purple-200 text-purple hover:bg-purple-200 dark:bg-purple-200 dark:text-purple dark:hover:bg-purple-200': graphToDisplay === 'wettest'}"
          >
            <div class="flex flex-col text-xs md:text-base">
              <span>{{ t("step3.wettest") }}</span>
              <span>{{ props.result?.wettestYear }}</span>
            </div>
          </UButton>
        </div>
      </div>

      <div
        id="refChart"
      />

      <div v-if="result && !loading" class="text-xs font-medium">
        <p>
          Cette estimation se base sur les données
          <a
            href="https://meteo.data.gouv.fr/"
            target="_blank"
            rel="noopener"
          >
            Météo France
          </a>
          de 1960 à {{ result.lastKnownYear }}.
        </p>
      </div>
    </div>
  </SubStep>
</template>

<script setup lang="ts">
import Plotly from "plotly.js-dist-min";
import InformationTooltip from "./InformationTooltip.vue";
import SubStep from "./SubStep.vue";
import { CalculatorResult } from "~/declaration";

const { t, locale } = useI18n();

const emit = defineEmits([
  "updateResult",
]);

const props = defineProps<{
  loading: boolean,
  result?: CalculatorResult,
}>();

const graphToDisplay: Ref<"recently" | "driest" | "wettest"> = ref("recently");
const idealCapacity = computed<string>(() => {
  if (props.result) {
    const realIdealCapacity = props.result.idealCapacity;
    const roundedIeadCapacity =  Math.ceil(realIdealCapacity / 100) * 100;
    return roundedIeadCapacity.toLocaleString(locale.value);
  }
  return '';
})
const getDivisionForWaterPrice = computed(() => {
  const division = props.result?.waterPrice.division;
  if (division === "communal") return t("step3.commune_level");
  if (division === "departemental") return t("step3.dept_level");
  return t("step3.national_level");
});

const selectedScenario = (scenario: "recently" | "driest" | "wettest") => {
  graphToDisplay.value = scenario;
  emit("updateResult", scenario);
};

const waterNeeds = computed<string>(() => {
  if (!props.result) {
    return ''
  }
  return (props.result.waterNeeds.indoor + props.result.waterNeeds.other + props.result.waterNeeds.outdoor).toLocaleString(locale.value);
})
const drawGraph = () => {
  if (props.result?.waterNeeds && props.result.waterRecoverableQuantity) {
    let waterRecovery = {
      x: ["Janv", "Févr", "Mars", "Avril", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
      y: Object.values(props.result.waterRecoverableQuantity),
      hovertemplate: "%{y:,} L<extra></extra>",
      type: "bar",
      name: `Précipitations enregistrées`,
      marker: {
        color: graphToDisplay.value === "recently" ? "#29235c" : graphToDisplay.value === "driest" ? "#af6708" : "#085421",
        opacity: 0.8,
      },
    };

    const waterNeeded = {
      x: waterRecovery.x,
      y: Object.values(props.result.evolutionNeededWater),
      hovertemplate: "%{y:,} L<extra></extra>",
      type: "bar",
      name: "Besoin en eau par mois",
      marker: { color: "#009fe3" },
    };

    const evolutionStockWater = {
      x: waterRecovery.x,
      y: props.result?.evolutionStockWater,
      hovertemplate: "%{y:,} L<extra></extra>",
      type: "scatter",
      name: "Évolution du stockage au sein du récupérateur",
      marker: { color: "#9b093e", size: 6, opacity: 0.8 },
      line: { dash: "dot", shape: "spline", width: 2.5 },
    };

    const evolutionUseTapWater = {
      x: waterRecovery.x,
      y: props.result?.consumptionByTapWater,
      hovertemplate: "%{y:,} L<extra></extra>",
      type: "scatter",
      name: "Usage de l'eau courante pour palier à l'insuffisance du récupérateur",
      marker: { color: "#9b8309", size: 6, opacity: 0.8 },
      line: { dash: "dot", shape: "spline", width: 2.5 },
    };

    const maxY = Math.max(
      ...Object.values(props.result.waterRecoverableQuantity),
      ...Object.values(props.result.evolutionNeededWater),
      ...props.result.evolutionStockWater,
      ...props.result.consumptionByTapWater
    );

    const layout = {
      font: { size: 12 },
      xaxis: {
        tickangle: -40,
        tickfont: { size: 12 },
      },
      yaxis: {
        range: [0, maxY * 1.1],
        tickfont: { size: 12 },
        tickformat: ",d",
        autorange: true,
        ticksuffix: " L",
      },
      barmode: "group",
      bargap: 0.2,
      separators: "  .",
      bargroupgap: 0.15,
      showlegend: true,
      legend: { orientation: "h", x: 0, y: -0.2 },
      height: 400,
      margin: { l: 80, r: 80, b: 50, t: 40, pad: 2 },
    };

    return { data: [waterRecovery, waterNeeded, evolutionStockWater, evolutionUseTapWater], layout };
  }
  return null;
};


watch(() => props.result, () => {
  const res = drawGraph();
  if (res) {
    const refChart = document.getElementById("refChart");
    Plotly.react(refChart!, res.data, res.layout, {
      showTips: false,
      modeBarButtonsToRemove: ["zoom2d", "zoomIn2d", "zoomOut2d", "pan2d", "select2d", "lasso2d", "toImage", "autoScale2d"],
      displaylogo: false,
    });
  }
});
</script>
