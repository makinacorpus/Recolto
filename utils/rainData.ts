
import { CRS } from "leaflet";
import { RainData, RainDataByMonth, RainDataYearsInfo } from "~/declaration";

/**
 * Retrieve the file related to the nearest centroid
 *
 * Unit is millimeter, mm
 */
export async function getRainData(centroid: L.LatLng | L.LatLngLiteral): Promise<RainData> {
  /**
   * Load all area coordinates
   */
  const centroidsCoordinatesResponse = await fetch("/data/centroid_coordinates_safran.json");
  const centroidsCoordinates: { lng: number, lat: number, gid: number }[] = await centroidsCoordinatesResponse.json();

  /**
   * Get nearest centroid coordinate
   */
  let nearestCentroidCoordinates: { lng: number, lat: number, gid: number }|undefined;
  let shortestDistance: number | null = null;
  centroidsCoordinates.forEach(currentPoint => {
    // Error ts caused by key "lon" instead of "lng"
    // Todo: Can we updated centroid_coordinates_all.json?
    const currentDistance = CRS.Earth.distance(centroid, currentPoint);
    if (shortestDistance === null || currentDistance < shortestDistance) {
      shortestDistance = currentDistance;
      nearestCentroidCoordinates = currentPoint;
    }
  });

  if (nearestCentroidCoordinates === undefined) {
    throw 'No weather data found'
  }
  const rainDataResponse = await fetch("/data/FR-ID-JSON/" + nearestCentroidCoordinates.gid + ".json");
  return await rainDataResponse.json()
}

export function getRainDataYearsInfo(rainData: RainData): RainDataYearsInfo {
  let nearestYear = undefined
  let driestYear = undefined
  let driestYearPrecipitation = undefined
  let wettestYear = undefined
  let wettestYearPrecipitation = undefined
  for (const [year, precipitation] of Object.entries(rainData.years)) {
    if (!nearestYear || (nearestYear < year)) {
      nearestYear = year
    }
    if (!driestYearPrecipitation || (driestYearPrecipitation > precipitation)) {
      driestYear = year
      driestYearPrecipitation = precipitation
    }
    if (!wettestYearPrecipitation || (wettestYearPrecipitation < precipitation)) {
      wettestYear = year
      wettestYearPrecipitation = precipitation
    }
  }

  return {
    nearest: nearestYear,
    driest: driestYear,
    wettest: wettestYear,
  }
}

export function getYearRainData(year: string, rainData: RainData): RainDataByMonth {
  return Object.entries(rainData.months)
    .filter(([month, _]) => month.startsWith(year as string))
    .sort(([monthA, _a], [monthB, _b]) => monthA > monthB ? 1 : -1)
    .map(([_, value]) => value) as RainDataByMonth
}
