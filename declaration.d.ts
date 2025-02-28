export type RainData = {
  years: Record<string, number>,
  months: Record<string, number>,
}

export type WaterPrice = {
  price: number, // price : €/m3
  year: number,
  division: "national" | "departemental" | "communal"
}

export type RoofType = { label: string, name: string, coeff: number }
export type RainDataByMonth = [number, number, number, number, number, number, number, number, number, number, number, number]
export type WaterNeedsByMonth = [number, number, number, number, number, number, number, number, number, number, number, number]
export type WaterByMonth = [number, number, number, number, number, number, number, number, number, number, number, number]

export type PrecipitationScenario = "nearest" | "driest" | "wettest"
export type RainDataYearsInfo = Record<PrecipitationScenario, string|undefined>

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
