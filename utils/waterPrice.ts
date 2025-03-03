import { WaterPrice } from "~/declaration";

export async function getWaterPrice(centroid: L.LatLng | L.LatLngLiteral, hasSewageSystem: boolean): Promise<WaterPrice> {

  const codeInsee = await findInseeCode(centroid)
  let waterPrice = defaultPriceWater(hasSewageSystem);

  if (codeInsee) {
    let department = codeInsee.substring(0, 2);

    if (department === "97") {
      // Exclusive for DROM-COM
      department = codeInsee.substring(0, 3);
    }
    const resWaterPriceCommune = await getWaterPriceCommune(codeInsee, department, hasSewageSystem);
    if (resWaterPriceCommune) {
      waterPrice = resWaterPriceCommune;
    } else {
      const resWaterPriceDpt = await getWaterPriceDepartement(department, hasSewageSystem);
      if (resWaterPriceDpt) {
        waterPrice = resWaterPriceDpt;
      }
    }
  }

  return waterPrice
}

async function findInseeCode(centroid: L.LatLng | L.LatLngLiteral): Promise<string|undefined> {
  // To avoid error from the reverse adresse API, we round the position to 3 digits,
  // this give use a precision of ~100m which is enought for what we are doing.
  const longitude = centroid.lng.toFixed(3)
  const latitude = centroid.lat.toFixed(3)

  try {
    const response = await fetch(`https://api-adresse.data.gouv.fr/reverse/?lon=${longitude}&lat=${latitude}`);

    if (response.ok) {
      const res = await response.json();

      if ( res.features?.length ) {
        return res.features[0].properties.citycode
      }
    } else {
      console.warn(`can't find adress for location ${longitude};${latitude}`)
    }
  } catch (e) {
    console.warn(`can't find adress for location ${longitude};${latitude}`)
  }
}

/**
 *  Default price (€/m³)
 *  If house is link to sewageSystem "assainissement"
 *  default value from https://www.services.eaufrance.fr/chiffres/1
 */
function defaultPriceWater(hasSewageSystem: boolean): WaterPrice {
  // Eau potable + Assainissement collectif
  if (hasSewageSystem) return {
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

async function getWaterPriceCommune(codeInsee: string, departement: string, hasSewageSystem: boolean) {
  let res: WaterPrice|null = null;
  try {
    const resPriceWaterByCity = await fetch(`/data/prix_eau_communes/${departement}.json`);
    const priceWaterByCity = await resPriceWaterByCity.json();
    if (codeInsee && priceWaterByCity[codeInsee]) {
      if (hasSewageSystem) {
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
}

async function getWaterPriceDepartement(departement: string, hasSewageSystem: boolean) {
  let res: WaterPrice|null = null;
  try {
    const resPriceWaterByDepartment = await fetch(`/data/prix_eau_depts.json`);
    const priceWaterByDepartment = await resPriceWaterByDepartment.json();
    if (priceWaterByDepartment[departement]) {
      if (hasSewageSystem) {
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
