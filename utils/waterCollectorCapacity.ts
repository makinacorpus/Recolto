/**
 * Constants defintion
 */

import { RainData, RainDataByMonth, WaterByMonth, WaterNeedsByMonth } from "~/declaration"

const WATER_USAGE_GARDEN_L_PER_M2_PER_YEAR = 20 // L/m²/an
const WATER_USAGE_VEGETABLE_L_PER_M2_PER_YEAR = 450 // L/m²/an
const WATER_USAGE_OUTDOOR_MONTH_DISTRIBUTION: WaterNeedsByMonth = [0, 0, 0, 1, 1, 2, 3, 3, 1, 0, 0, 0]

// For toilets, we can consider the following statistics:
//   with a single button flush, 10L / flush
//   with a double button flush, 5L / flush
//   On average, a person flushes 4 times a day.
const WATER_USAGE_TOILET_L_PER_PERSON_PER_YEAR = 14600 // 4 * 10 * 365, L/personne/an

  // Typically, a washing machine consumes 75 L per use and is used on average :
  //   2 times a week for 1 or 2 people (i.e. 21.5L / day)
  //   4 times a week for a family of 3 or 4 (i.e. 43L / day)
  //   6 times a week for more (i.e. 64L / day).
const WATER_USAGE_WASHING_MACHINE_L_PER_PERSON_PER_YEAR = {
  '1_TO_2': 7847.5, // 21.5 * 365 L/personne/an
  '3_TO_4': 15695, // 43 * 365 L/personne/an
  '5_OR_MORE': 23360, // 64 * 365 L/personne/an
}
// indoor needs are evenly distributed throughout the year
const WATER_USAGE_INDOOR_MONTH_DISTRIBUTION: WaterNeedsByMonth = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

const WATER_COLLECTOR_EFFICIENCY = 0.9

export function getWaterNeedsByMonth (
  gardenSurfaceArea: number, // m²
  surfaceVegetable: number, // m²
  otherNeeds: number, // L
  toiletsConnected: boolean,
  washingMachineConnected: boolean,
  residentNumber: number,
): WaterNeedsByMonth {
  const outdoorNeeds = (gardenSurfaceArea * WATER_USAGE_GARDEN_L_PER_M2_PER_YEAR) + (surfaceVegetable * WATER_USAGE_VEGETABLE_L_PER_M2_PER_YEAR)
  const totalOutdoorMonthNeed = WATER_USAGE_OUTDOOR_MONTH_DISTRIBUTION.reduce((a, b) => a + b, 0)
  const outdoorNeedsByMonth = WATER_USAGE_OUTDOOR_MONTH_DISTRIBUTION.map(m => m * outdoorNeeds / totalOutdoorMonthNeed)

  let indoorNeeds = 0
  if ((residentNumber > 0) && toiletsConnected) {
    indoorNeeds += residentNumber * WATER_USAGE_TOILET_L_PER_PERSON_PER_YEAR;
  }

  if (residentNumber > 0 && washingMachineConnected) {
    if (residentNumber <= 2) {
      indoorNeeds += WATER_USAGE_WASHING_MACHINE_L_PER_PERSON_PER_YEAR["1_TO_2"]
    } else if (residentNumber <= 4) {
      indoorNeeds += WATER_USAGE_WASHING_MACHINE_L_PER_PERSON_PER_YEAR["3_TO_4"]
    } else {
      indoorNeeds += WATER_USAGE_WASHING_MACHINE_L_PER_PERSON_PER_YEAR["5_OR_MORE"]
    }
  }
  indoorNeeds += otherNeeds

  const totalIndoorMonthNeed = WATER_USAGE_INDOOR_MONTH_DISTRIBUTION.reduce((a, b) => a + b, 0)
  const indoorNeedsByMonth = WATER_USAGE_INDOOR_MONTH_DISTRIBUTION.map(m => m * indoorNeeds / totalIndoorMonthNeed)

  return outdoorNeedsByMonth.map((outdoorValue, month) => outdoorValue + indoorNeedsByMonth[month]) as WaterNeedsByMonth
}

/**
 * From water needs by month and rain data, we can estimate a good
 * water collector capacity.
 *
 * We use the "reference volume method" from the ASTEE guide found here (page 32 of the PDF):
 * https://www.astee.org/publications/guide-sur-la-recuperation-et-utilisation-de-leau-de-pluie/
 *
 * We adapted the formula because we have more than 5 years (60 months)
 *
 * @param waterNeeds
 * @param rainData
 * @return ideal water collector capacity in (L) rounded to the nearest 100
 */
export function estimateWaterCollectorCapacity(
  waterNeeds: WaterNeedsByMonth,
  rainData: RainData,
  roofArea: number,
  roofAbsorbtionCoeff: number
): number {
  const correctedRoofArea = roofArea * roofAbsorbtionCoeff * WATER_COLLECTOR_EFFICIENCY // m²

  const coeffRef = Object.entries(rainData.months).reduce<number>((accumulator, [key, precipitation]) => {
    // key are `yyyy-mm`
    const month = Number(key.split('-')[1])
    const collectedRain = precipitation * correctedRoofArea // mm*m² => L

    if (waterNeeds[(month - 1)] > 0) {
      return accumulator + Math.min(1, collectedRain / waterNeeds[(month - 1)])
    } else {
      return accumulator + 1
    }

  }, 0) / Object.keys(rainData.months).length

  // If coeffRef < 0.65, wate needs are superior to the rain the we can collect each
  // month. In this case, original algorithm from the ASTEE document recommends to simulate.
  // For now, we do not do it and we keep the simple formula, rounded to the nearest 100.
  const capacity = waterNeeds.reduce((a, b) => a + b, 0) / 12 * 0.7 / ( coeffRef * coeffRef )

  return (capacity < 100) ? Math.round(capacity / 10) * 10 : Math.round(capacity / 100) * 100
}

export function getWaterCollectorEvolutionPerMonth (
  waterCollectorCapacity: number, // L
  waterNeeds: WaterNeedsByMonth, // L / month
  rainData: RainDataByMonth, // mm / month
  roofArea: number, // m²
  roofAbsorbtionCoeff: number
) {
  const correctedRoofArea = roofArea * roofAbsorbtionCoeff * WATER_COLLECTOR_EFFICIENCY // m²

  const waterCollectorLevelPerMonth = []
  const roofPotentialWaterCollectPerMonth = []
  const rainWaterConsumptionPerMonth = []
  let currentWaterCollectorLevel = 0
  for (const month of Array(12).keys()) {
    const roofPotential = rainData[month] * correctedRoofArea // L
    roofPotentialWaterCollectPerMonth.push(roofPotential)

    currentWaterCollectorLevel += roofPotential

    if ((currentWaterCollectorLevel - waterNeeds[month]) > 0) {
      // We have enought water for our monthly needs
      rainWaterConsumptionPerMonth.push(waterNeeds[month])
      currentWaterCollectorLevel -= waterNeeds[month]
    } else {
      // We have not enought water for our monthly needs
      rainWaterConsumptionPerMonth.push(currentWaterCollectorLevel)
      currentWaterCollectorLevel = 0
    }
    // At then end of month, current water collector level can't be more than its capacity
    currentWaterCollectorLevel = Math.min(waterCollectorCapacity, currentWaterCollectorLevel)
    waterCollectorLevelPerMonth.push(currentWaterCollectorLevel)
  }

  return {
    roofPotentialWaterCollect: roofPotentialWaterCollectPerMonth as WaterByMonth,
    rainWaterConsumption: rainWaterConsumptionPerMonth as WaterByMonth,
    waterCollectorLevel: waterCollectorLevelPerMonth as WaterByMonth,
  }
}
