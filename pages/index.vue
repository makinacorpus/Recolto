<template>
  <div class="flex-grow relative">
    <recolto-calculator
      class="absolute bottom-0 left-0 right-0 md:top-[10px] md:left-[10px] md:right-[unset] md:bottom-[unset] z-[1002] overflow-auto"
      :class="{
        'md:min-h-[30rem]': currentStepIndex === 0 && !selectedAddress,
        'md:max-h-[95%] scrolling-auto overflow-auto': selectedAddress,
        'h-[30rem] md:h-[95%] scrolling-auto overflow-auto': currentStepIndex === 2
      }"

      :roof-surface="data.roofSurface"
      :result="result"
      :force-reset-input="forceResetInput"
      v-model:currentStepIndex="currentStepIndex"
      v-model:selectedAddress="selectedAddress"
      v-model:selectedTypeRoof="selectedTypeRoof"
      v-model:selectedSewageSystem="selectedSewageSystem"
      :surface-garden-by-draw="surfaceGardenByDraw"
      :surface-vegetable-by-draw="surfaceVegetableByDraw"
      :loading="loading"

      @compute="onCompute"
      @draw-roof="allowDrawMap($event)"
      @draw-water-usage="allowDrawMap($event)"
      @editable-map="drawEnabled = null"
      @update-result="updateResultCalculator($event)"
    />
    <recolto-map
      :center="selectedAddress"
      :draw-enabled="drawEnabled"

      @polygon:created="onPolygonCreated"
      @polygon:edited="onPolygonEdited"
      @polygon:deleted="onPolygonDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import L from "leaflet";
import RecoltoMap from "../components/map/RecoltoMap.vue";
import RecoltoCalculator from "../components/calculator/RecoltoCalculator.vue";
import { type ApiAdresse } from "~/declaration";
import { prepareDataForGraph, CopernicusData } from "~/composables/calculator";

definePageMeta({
  layout: "app",
});

/**
 * General data for the computation
 */
const data = ref<{
  centroid?: L.LatLngExpression,
  surfaceGarden: number,
  surfaceVegetable: number,
  exteriorMaintenance: number,
  roofSurface: number,
}>({
  surfaceGarden: 0,
  surfaceVegetable: 0,
  exteriorMaintenance: 0,
  roofSurface: 0,
});

const surfaceGardenByDraw = ref(0);
const surfaceVegetableByDraw = ref(0);
/**
 * Force input to 0 when user remove all area via action deleted
 * (To prevent conflict when user update value manually in input)
 */
const forceResetInput: Ref<null | {
  area: "garden" | "vegetable",
  newValue: number
}> = ref(null);

const currentStepIndex = ref(0);

const drawEnabled: Ref<null | { area: "roof" | "garden" | "vegetable" | "allUsage", action?: "draw" | "clear" }> = ref(
  null);

/**
 * Allow to active leaflet draw
 * According to the area, user can draw or clear layer in map
 */
const allowDrawMap = (data: { area: "roof" | "garden" | "vegetable" | "allUsage", action?: "draw" | "clear" }) => {
  if (data.action === "clear" && data.area === "garden") {
    // Reset value when user update manually surfaceGarden
    surfaceGardenByDraw.value = 0;
  }
  if (data.action === "clear" && data.area === "vegetable") {
    // Reset value when user update manually surfaceVegetable
    surfaceVegetableByDraw.value = 0;
  }
  if (data.action === "clear" && data.area === "allUsage") {
    // Reset value when user change step
    surfaceGardenByDraw.value = 0;
    surfaceVegetableByDraw.value = 0;
  }
  drawEnabled.value = data;
};

/**
 *
 * Address management
 *
 */
const selectedAddress = ref<ApiAdresse | undefined>(undefined);

/**
 *
 * Map management
 *
 */

/**
 * Manage data when a polygon is created on the map
 */
function onPolygonCreated (geodesicArea: number, centroid: L.LatLngExpression, area: string) {
  if (area === "roof") {
    data.value.centroid = centroid;
    // Force number of float to prevent behavior from JS engine
    data.value.roofSurface = Number(geodesicArea.toFixed(2));
    // Deprecated
    // data.value.weightedRoofSurface = Math.round(data.value.roofSurface * 120) / 100;
    // maxStepIndex.value = 1;
  }
  if (area === "garden") {
    // Force number for float to prevent behavior from JS engine
    surfaceGardenByDraw.value = Number((surfaceGardenByDraw.value + geodesicArea).toFixed(2));
  }
  if (area === "vegetable") {
    // Force number for float to prevent behavior from JS engine
    surfaceVegetableByDraw.value = Number((surfaceVegetableByDraw.value + geodesicArea).toFixed(2));
  }
}

/**
 * Manage data when a polygon is edited on the map
 */
function onPolygonEdited (totalGeodesicArea: number, area: string) {
  if (area === "roof") {
    // Force number for float to prevent behavior from JS engine
    data.value.roofSurface = Number(totalGeodesicArea.toFixed(2));
    // maxStepIndex.value = 2;
  }
  if (area === "garden") {
    // Force number for float to prevent behavior from JS engine
    surfaceGardenByDraw.value = Number(totalGeodesicArea.toFixed(2));
  }
  if (area === "vegetable") {
    // Force number for float to prevent behavior from JS engine
    surfaceVegetableByDraw.value = Number(totalGeodesicArea.toFixed(2));
  }
}

/**
 * Manage data when a polygon is deleted on the map
 */
const onPolygonDeleted = (geodesicArea: number, area: string) => {
  // Reminder: it is impossible to delete a roof layer
  if (area === "garden") {
    // Force number for float to prevent behavior from JS engine
    surfaceGardenByDraw.value = Number((surfaceGardenByDraw.value - geodesicArea).toFixed(2));
    forceResetInput.value = {
      area: "garden",
      newValue: Number((surfaceGardenByDraw.value - geodesicArea).toFixed(2)),
    };
  }
  if (area === "vegetable") {
    // Force number for float to prevent behavior from JS engine
    surfaceVegetableByDraw.value = Number((surfaceVegetableByDraw.value - geodesicArea).toFixed(2));
    forceResetInput.value = {
      area: "vegetable",
      newValue: Number((surfaceVegetableByDraw.value - geodesicArea).toFixed(2)),
    };
  }
};


/**
 *
 * Computation for the water retrievable
 *
 */
const loading = ref(false);
const result = ref<{
  waterPrice: { price: number, year: number, division: "national" | "departemental" | "communal" }, // price : €/m3
  lastKnownYear: string,
  waterRecoverableQuantity: Record<string, number>, // mm * m² => L
  savingForLastKnownYear?: number, // €/m3/year
  idealCapacity: number, // L/year
  waterNeeds: number, // L/year
  copernicusData: CopernicusData, // (mm/m²)
  roofSurfaceArea: number, // m²
  gardenSurfaceArea: number, // m²
  vegetableSurfaceArea: number, // m²
  evolutionStockWater: number[], // L
  consumptionByTapWater: number[], // L
  driestYear: string,
  wettestYear: string,
} | null>(null);

const selectedTypeRoof = ref({ name: "ardoise", value: 0.8 });
const selectedSewageSystem = ref(true); // Raccordement Tout-à-l'égout

/**
 *  Default price (€/m³)
 *  If house is link to sewageSystem "assainissement"
 *  default value from https://www.services.eaufrance.fr/chiffres/1
 */
const defaultPriceWater = (): { price: number, year: number, division: "national" | "departemental" | "communal" } => {
  // Eau potable + Assainissement collectif
  if (selectedSewageSystem.value) return {
    price: 4.34,
    year: 2023,
    division: "national",
  };
  // Eau potable
  return {
    price: 2.13,
    year: 2023,
    division: "national",
  };
};

async function onCompute (usageData: {
  surfaceGarden: number,
  surfaceVegetable: number,
  exteriorMaintenance: number,
}) {
  loading.value = true;
  data.value.surfaceGarden = usageData.surfaceGarden || 0;
  data.value.surfaceVegetable = usageData.surfaceVegetable || 0;
  data.value.exteriorMaintenance = usageData.exteriorMaintenance || 0;

  currentStepIndex.value++;

  /**
   * Load all area coordinates
   */
  const centroidsCoordinatesResponse = await fetch("/data/centroid_coordinates_all.json");
  const centroidsCoordinates: { lng: number, lat: number, gid: number }[] = await centroidsCoordinatesResponse.json();

  /**
   * Get nearest centroid coordinate
   */
  let nearestCentroidCoordinates: { lng: number, lat: number, gid: number } | null = null;
  let shortestDistance: number | null = null;
  centroidsCoordinates.forEach(currentPoint => {
    // Error ts caused by key "lon" instead of "lng"
    // Todo: Can we updated centroid_coordinates_all.json?
    const currentDistance = L.CRS.Earth.distance(data.value.centroid as L.LatLngExpression, currentPoint);
    if (shortestDistance === null || currentDistance < shortestDistance) {
      shortestDistance = currentDistance;
      nearestCentroidCoordinates = currentPoint;
    }
  });

  /**
   * Retrieve the file related to the nearest centroid
   *
   * Unit is millimeter by square meter, mm/m²
   */
    // Todo: Can nearestCentroidCoordinates be null?
  const copernicusDataResponse = await fetch("/data/copernicus/" + nearestCentroidCoordinates.gid + ".json");
  const copernicusData = await copernicusDataResponse.json();

  /**
   * Todo:
   * Waiting for last release (last year available = 2018) to use API rather than json file.
   */


  let waterPrice = defaultPriceWater();
  const codeInsee = selectedAddress.value?.properties?.citycode;

  if (codeInsee) {
    let department = codeInsee.substring(0, 2);

    if (department === "97") {
      // Exclusive for DROM-COM
      department = codeInsee.substring(0, 3);
    }
    const resWaterPriceCommune = await getWaterPriceCommune(codeInsee, department, selectedSewageSystem.value);
    if (resWaterPriceCommune) {
      waterPrice = resWaterPriceCommune;
    } else {
      const resWaterPriceDpt = await getWaterPriceDepartement(department, selectedSewageSystem.value);
      if (resWaterPriceDpt) {
        waterPrice = resWaterPriceDpt;
      }
    }
  }

  /**
   * Compute data
   */
  result.value = computeWaterCollectorCapacity(
    data.value.roofSurface * selectedTypeRoof.value.value,
    waterPrice,
    copernicusData,
    Number(data.value.surfaceGarden),
    Number(data.value.surfaceVegetable),
    Number(data.value.exteriorMaintenance),
  );

  loading.value = false;
}

const getWaterPriceCommune = async (codeInsee: string, departement: string, isSewageSystem: boolean) => {
  let res = null;
  try {
    const resPriceWaterByCity = await fetch(`/data/prix_eau_communes_2022/${departement}.json`);
    const priceWaterByCity = await resPriceWaterByCity.json();
    if (codeInsee && priceWaterByCity[codeInsee]) {
      if (isSewageSystem) {
        res = {
          price: Number(priceWaterByCity[codeInsee].priceTotal_value.toFixed(2)),
          year: priceWaterByCity[codeInsee].priceTotal_year,
          division: "communal" as "national" | "departemental" | "communal",
        };
      } else {
        res = {
          price: Number(priceWaterByCity[codeInsee].priceEp_value.toFixed(2)),
          year: priceWaterByCity[codeInsee].priceEp_year,
          division: "communal" as "national" | "departemental" | "communal",
        };
      }
    }
  } catch (error) {
    console.warn("Impossible de récupérer les données pour les communes.");
  }
  return res;
};

const getWaterPriceDepartement = async (departement: string, isSewageSystem: boolean) => {
  let res = null;
  try {
    const resPriceWaterByDepartment = await fetch(`/data/prix_eau_depts_2022.json`);
    const priceWaterByDepartment = await resPriceWaterByDepartment.json();
    if (priceWaterByDepartment[departement]) {
      if (isSewageSystem) {
        res = {
          price: Number(priceWaterByDepartment[departement].priceTotal_value.toFixed(2)),
          year: priceWaterByDepartment[departement].priceTotal_year,
          division: "departemental" as "national" | "departemental" | "communal",
        };
      } else {
        res = {
          price: Number(priceWaterByDepartment[departement].priceEp_value.toFixed(2)),
          year: priceWaterByDepartment[departement].priceEp_year,
          division: "departemental" as "national" | "departemental" | "communal",
        };
      }
    }
  } catch (error) {
    console.warn("Impossible de récupérer les données pour les départments.");
  }
  return res;
};

// Compute only if user toggle of scenario
const updateResultCalculator = (scenario = "recently") => {
  if (result.value) {
    result.value = {
      ...result.value, ...prepareDataForGraph(
        result.value.copernicusData,
        result.value.idealCapacity,
        result.value.roofSurfaceArea,
        result.value.lastKnownYear,
        result.value.waterNeeds,
        scenario,
      ),
    };
  }
};

useHead({
  title: "Récolt'Ô | Calculateur",
});
</script>

