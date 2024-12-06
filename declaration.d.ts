export interface ApiAdresse {
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
