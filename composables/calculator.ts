import { CalculatorResult } from "~/declaration";

export interface CopernicusData {
  years: Record<string, number>,
  months: Record<string, number>,
}

const coeffWaterUsage = {
  garden: 20, // L/m²/an
  vegetable: 450, // L/m²/an
  // For toilets, we can consider the following statistics:
  //   with a single button flush, 10L / flush
  //   with a double button flush, 5L / flush
  //   On average, a person flushes 4 times a day.
  toilets: 14600, // 4 * 10 * 365, L/personne/an
  // Typically, a washing machine consumes 75 L per use and is used on average :
  //   2 times a week for 1 or 2 people (i.e. 21.5L / day)
  //   4 times a week for a family of 3 or 4 (i.e. 43L / day)
  //   6 times a week for more (i.e. 64L / day).
  washingMachine: {
    '1_to_2': 7847.5, // 21.5 * 365 L/personne/an
    '3_to_4': 15695, // 43 * 365 L/personne/an
    '5_or_more': 23360, // 64 * 365 L/personne/an
  },
};

const system_efficiency = 0.9 // System efficiency ratio
const fromMonth = "04"; // Avril
const toMonth = "10"; // October

/**
 * Calculator of the capacity for a (rain)water collector
 *
 * Need several inputs :
 * * roof surface area, in square meter
 * * water price for 1000 L
 * * copernicus data for the related roof geographic zone
 * * garden / vegetable garden yearly water use
 *
 * Return an object :
 * * total quantity of water recoverable for the last known year
 * * total quantity of water recoverable for each month of the last known year
 * * saving for the last known year if a collector was already installed
 * * water needs, computed for the period 1st, april > 31st, october
 * * ideal capacity of a water collector
 *
 */
export function computeWaterCollectorCapacity (
  roofSurfaceArea: number,
  waterPrice: { price: number, year: number, division: "national" | "departemental" | "communal" },
  copernicusData: CopernicusData,
  gardenSurfaceArea: number,
  vegetableSurfaceArea: number,
  exteriorMaintenance: number,
  toiletsConnected: boolean,
  washingMachineConnected: boolean,
  residentNumber: number,
  reserveDays: number = 30,
): CalculatorResult {

  const result = {
    waterPrice, // price : €/m3
    lastKnownYear: "2023",
    waterRecoverableQuantity: {}, // (mm * m²) => L
    savingForLastKnownYear: 0, // (L / 1000 * €/m3) => €/m3/year  (depends on waterNeeds)
    idealCapacity: 0, // L + L/year => L/year (depends on waterRecoverableQuantityForLastKnownYear + waterNeeds)
    waterNeeds: 0,  // m² * L/m²/year => L/year
    copernicusData, // (mm/m²)
    roofSurfaceArea, // m²
    gardenSurfaceArea, // m²
    vegetableSurfaceArea, // m²
    toiletsConnected,
    washingMachineConnected,
    residentNumber,
    evolutionStockWater: [], // L
    consumptionByTapWater: [], // L
    driestYear: "",
    wettestYear: "",
  };
  const yearsFromCopernicus = Object.keys(copernicusData.years).sort();

  // Get the last known year
  result.lastKnownYear = yearsFromCopernicus[yearsFromCopernicus.length - 1];

  const waterRecoverableQuantityForLastKnownYear = Math.round(copernicusData.years[result.lastKnownYear] * roofSurfaceArea * system_efficiency); // (mm * m²) => L

  result.waterNeeds = computeWaterNeeds(
    gardenSurfaceArea,
    vegetableSurfaceArea,
    exteriorMaintenance,
    toiletsConnected,
    washingMachineConnected,
    residentNumber
  )

  result.idealCapacity = Math.round((waterRecoverableQuantityForLastKnownYear + result.waterNeeds) / 2 * (reserveDays / 365));

  // Amount saved
  result.savingForLastKnownYear = Number(((result.waterNeeds / 1000) * waterPrice.price).toFixed(2));

  const dataGraph = prepareDataForGraph(
    copernicusData,
    result.idealCapacity,
    result.roofSurfaceArea,
    result.lastKnownYear,
    result.waterNeeds,
  );

  return { ...result, ...dataGraph };
}

export function prepareDataForGraph (
  copernicusData: CopernicusData,
  idealCapacity: number,
  roofSurfaceArea: number,
  lastKnownYear: string,
  waterNeeds: number,
  scenario = "recently",
) {

  const sumByYearBetweenWantedMonth = Object.entries(copernicusData.months).reduce((acc, [yearMonth, val]) => {
    const [year, month] = yearMonth.split("-");
    acc[year] = acc[year] ?? 0;
    if (month >= fromMonth && month <= toMonth) {
      acc[year] += val;
    }
    return acc;
  }, {} as Record<string, number>);

  // Get years for max and min precipitation
  const yearsMinMaxPrecipitation = Object.entries(sumByYearBetweenWantedMonth).reduce((acc, [year, total]) => {
    if (!acc.minPrecipitation.year) {
      acc.minPrecipitation = { year, precipitation: total };
    } else {
      if (total < acc.minPrecipitation.precipitation) {
        acc.minPrecipitation = { year, precipitation: total };
      }
    }
    if (!acc.maxPrecipitation.year) {
      acc.maxPrecipitation = { year, precipitation: total };
    } else {
      if (acc.maxPrecipitation.precipitation < total) {
        acc.maxPrecipitation = { year, precipitation: total };
      }
    }
    return acc;
  }, { minPrecipitation: { year: "", precipitation: -1 }, maxPrecipitation: { year: "", precipitation: -1 } } as {
    minPrecipitation: { year: string, precipitation: number },
    maxPrecipitation: { year: string, precipitation: number },
  });

  const years = {
    driestYear: yearsMinMaxPrecipitation.minPrecipitation.year,
    wettestYear: yearsMinMaxPrecipitation.maxPrecipitation.year,
  };

  if (scenario === "recently") {
    // Get data for last known year by month (Precipitation)
    const waterForLastKnownYearByMonths = Object.keys(copernicusData.months)
      .filter(currentKey => currentKey.startsWith(lastKnownYear));

    // Computed data according to roof by month for the last know year
    const waterRecoverableQuantityForLastKnownYearByMonth = waterForLastKnownYearByMonths.reduce((
      acc: Record<string, number>,
      month,
    ) => {
      acc[month] = Math.round(copernicusData.months[month] * roofSurfaceArea);
      return acc;
    }, {});

    return {
      ...years,
      ...prepareDataLineEvolution(
        waterForLastKnownYearByMonths,
        copernicusData,
        roofSurfaceArea,
        idealCapacity,
        waterNeeds,
      ),
      waterRecoverableQuantity: waterRecoverableQuantityForLastKnownYearByMonth,
    };
  }
  if (scenario === "driest") {
    // Get data for the driest known year by month (Precipitation)
    const waterForDriestYear = Object.keys(copernicusData.months)
      .filter(currentKey => currentKey.startsWith(yearsMinMaxPrecipitation.minPrecipitation.year));

    // Computed data according to roof by month for the driest year
    const waterRecoverableQuantityForDriestYearByMonth = waterForDriestYear.reduce((
      acc: Record<string, number>,
      currentKey,
    ) => {
      acc[currentKey] = Math.round(copernicusData.months[currentKey] * roofSurfaceArea);
      return acc;
    }, {});

    return {
      ...years,
      ...prepareDataLineEvolution(
        waterForDriestYear,
        copernicusData,
        roofSurfaceArea,
        idealCapacity,
        waterNeeds,
      ),
      waterRecoverableQuantity: waterRecoverableQuantityForDriestYearByMonth,
    };
  }
  if (scenario === "wettest") {
    // Get data for the wettest known year by month (Precipitation)
    const waterForWettestYear = Object.keys(copernicusData.months)
      .filter(currentKey => currentKey.startsWith(yearsMinMaxPrecipitation.maxPrecipitation.year));

    // Computed data according to roof by month for the wettest year
    const waterRecoverableQuantityForWettestYearByMonth = waterForWettestYear.reduce((
      acc: Record<string, number>,
      currentKey,
    ) => {
      acc[currentKey] = Math.round(copernicusData.months[currentKey] * roofSurfaceArea);
      return acc;
    }, {});

    return {
      ...years,
      ...prepareDataLineEvolution(
        waterForWettestYear,
        copernicusData,
        roofSurfaceArea,
        idealCapacity,
        waterNeeds,
      ),
      waterRecoverableQuantity: waterRecoverableQuantityForWettestYearByMonth,
    };
  }
}

const prepareDataLineEvolution = (
  waterForCurrentYearByMonth: string[],
  copernicusData: CopernicusData,
  roofSurfaceArea: number,
  idealCapacity: number,
  waterNeeds: number,
) => {
  // Regroup conso + precipitation data
  const consoAndPrecipitationByMonth = waterForCurrentYearByMonth.reduce((acc, key, currentIndex) => {
    if (currentIndex < 3 || currentIndex > 9) {
      acc.push({ "precipitation": Math.round(copernicusData.months[key] * roofSurfaceArea), "consumption": 0 });
    } else {
      acc.push({
        "precipitation": Math.round(copernicusData.months[key] * roofSurfaceArea),
        "consumption": Math.round(waterNeeds / 7),
      });
    }
    return acc;
  }, [] as { "precipitation": number, "consumption": number }[]);

  // Evolution storage water
  const evolutionStockWater = consoAndPrecipitationByMonth.reduce((acc, elem, index) => {
    let currentVolume = Math.min(elem.precipitation + (acc[index - 1] ?? 0), idealCapacity);
    currentVolume = Math.max(currentVolume - elem.consumption, 0);
    acc.push(currentVolume);
    return acc;
  }, [] as number[]);

  // If water stock not enough, how many liter of water user will use?
  const consumptionByTapWater = consoAndPrecipitationByMonth.reduce((acc, elem, index) => {
    let currentVolume = Math.max(elem.precipitation + (acc[index - 1] ?? 0), 0);
    currentVolume = Math.abs(Math.min(0, currentVolume - elem.consumption));
    acc.push(currentVolume);
    return acc;
  }, [] as number[]);
  return {
    consumptionByTapWater,
    evolutionStockWater,
  };
};

const computeWaterNeeds = (
  gardenSurfaceArea: number,
  vegetableSurfaceArea: number,
  exteriorMaintenance: number,
  toiletsConnected: boolean,
  washingMachineConnected: boolean,
  residentNumber: number,
) => {
  let waterNeeds = gardenSurfaceArea * coeffWaterUsage.garden + vegetableSurfaceArea * coeffWaterUsage.vegetable + exteriorMaintenance;

  (residentNumber > 0 && toiletsConnected) || (waterNeeds += residentNumber * coeffWaterUsage.toilets);

  if (residentNumber > 0 && washingMachineConnected) {
    if (residentNumber <= 2) {
      waterNeeds += coeffWaterUsage.washingMachine["1_to_2"];
    } else if (residentNumber <= 4) {
      waterNeeds += coeffWaterUsage.washingMachine["3_to_4"];
    } else {
      waterNeeds += coeffWaterUsage.washingMachine["5_or_more"];
    }
  }

  return waterNeeds;
}
