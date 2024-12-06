import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw'
import 'leaflet-draw/dist/leaflet.draw.css'

/**
 * Fix for readableArea
 */
const defaultPrecision = {
  km: 2,
  ha: 2,
  m: 0,
  mi: 2,
  ac: 2,
  yd: 0,
  ft: 0,
  nm: 2
};
L.GeometryUtil.readableArea = function (area, isMetric, precisionExtended) {
  let areaStr: any
  const precision = L.Util.extend({}, defaultPrecision, precisionExtended);

  if (isMetric) {
    let units: any[] = ['ha', 'm'];
    const type = typeof isMetric;
    if (type === 'string') {
      units = [isMetric];
    } else if (type !== 'boolean') {
      units = isMetric as unknown as any[];
    }

    if (area >= 1000000 && units.indexOf('km') !== -1) {
      areaStr = L.GeometryUtil.formattedNumber(area * 0.000001 as unknown as string, precision['km']) + ' km²';
    } else if (area >= 10000 && units.indexOf('ha') !== -1) {
      areaStr = L.GeometryUtil.formattedNumber(area * 0.0001 as unknown as string, precision['ha']) + ' ha';
    } else {
      areaStr = L.GeometryUtil.formattedNumber(area as unknown as string, precision['m']) + ' m²';
    }
  } else {
    area /= 0.836127; // Square yards in 1 meter

    if (area >= 3097600) { //3097600 square yards in 1 square mile
      areaStr = L.GeometryUtil.formattedNumber(area / 3097600 as unknown as string, precision['mi']) + ' mi²';
    } else if (area >= 4840) { //4840 square yards in 1 acre
      areaStr = L.GeometryUtil.formattedNumber(area / 4840 as unknown as string, precision['ac']) + ' acres';
    } else {
      areaStr = L.GeometryUtil.formattedNumber(area as unknown as string, precision['yd']) + ' yd²';
    }
  }

  return areaStr;
}
