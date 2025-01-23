export type CalculatorResult = {
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
}
