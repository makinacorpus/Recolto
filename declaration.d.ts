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
  toiletsConnected: boolean,
  washingMachineConnected: boolean,
  residentNumber: number,
  evolutionStockWater: number[], // L
  consumptionByTapWater: number[], // L
  driestYear: string,
  wettestYear: string,
}

export interface ApiAddress {
  id?: string
  type?: string
  geometry: {
    type: 'Point'
    coordinates: [number, number]
  }
  properties?: {
    city: string
    citycode: string
    context: string
    id: string
    importance: number
    label: string
    name: string
    postcode: string
    score: number
    type: string
    x: number
    y: number
  }
}
