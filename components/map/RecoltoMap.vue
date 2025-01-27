<template>
  <div id="map"></div>
</template>

<script lang="ts">
const runtime_config = useRuntimeConfig();
let center_coordinates = runtime_config.public.CENTER_COORDINATES as L.LatLngTuple;
let zoom = runtime_config.public.ZOOM ;
export default {};
</script>

<script setup lang="ts">
import L from "leaflet";
import "./leaflet-deps";

let map: L.DrawMap;
let polygonDrawer: L.Draw.Polygon;
let drawControl: L.Control.Draw;

const props = withDefaults(defineProps<{
  center?: { latlng: L.LatLngExpression, accuracy?: number },
  drawEnabled: null | { area: "roof" | "garden" | "vegetable" | "allUsage", action?: "draw" | "clear" }
}>(), {
  center: () => ({ latlng: center_coordinates }),
  drawEnabled: null,
});

const emit = defineEmits(["polygon:created", "polygon:deleted", "polygon:edited"]);
const editableLayers = new L.FeatureGroup();

/**
 * Init HTML element with a Leaflet map
 *
 * Need a leaflet selector (quitely different from a CSS one),
 * a center [lat, lng] and a zoom level (number 0 to 22, 16 is nice).
 *
 * Returns a Leaflet.Map with helpers
 */
onMounted(() => {
  map = L.map("map", { zoomControl: false }).setView(center_coordinates, zoom);

  L.control.zoom({
    position: "topright",
    zoomInTitle: "Zoomer",
    zoomOutTitle: "Dézoomer"
  }).addTo(map);

  // Set up the OSM layer
  // https://geoservices.ign.fr/services-web-decouverte
  L.tileLayer(
    'https://data.geopf.fr/wmts?' +
    '&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&TILEMATRIXSET=PM'+
    '&LAYER={ignLayer}&STYLE={style}&FORMAT={format}'+
    '&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}', {
      ignLayer: 'ORTHOIMAGERY.ORTHOPHOTOS',
      style: 'normal',
      format: 'image/jpeg',
      service: 'WMTS',
      attribution: 'Carte © IGN/Geoplateforme',
      maxNativeZoom: 19,
      maxZoom: 22,
    })
  .addTo(map);

  // Initialise the FeatureGroup to store editable layers
  map.addLayer(editableLayers);

  // Initialise the draw control and pass it the FeatureGroup of editable layers
  drawControl = new L.Control.Draw({
    position: "topright",
    draw: false,
    edit: {
      featureGroup: editableLayers,
      remove: true,
    },
  });

  // Override Locale
  L.drawLocal.draw.handlers.polygon = {
    tooltip: {
      start: "Cliquez pour commencer à dessiner les limites de la zone",
      cont: "Cliquez pour continuer à dessiner les limites de la zone",
      end: "Cliquez sur le premier point pour terminer",
    },
  };
  L.drawLocal.edit = {
    toolbar: {
      actions: {
        save: {
          title: "Enregistrer la modification",
          text: "Enregistrer",
        },
        cancel: {
          title: "Annuler l'édition",
          text: "Annuler",
        },
        clearAll: {
          title: "Supprimer le tracé",
          text: "Tout supprimer",
        },
      },
      buttons: {
        edit: "Éditer",
        editDisabled: "Aucun tracé à éditer",
        remove: "Supprimer",
        removeDisabled: "Aucun tracé à supprimer",
      },
    },
    handlers: {
      edit: {
        tooltip: {
          text: "Déplacer les points pour modifier le tracé",
          subtext: "Cliquez sur annuler pour ignorer l'édition",
        },
      },
      remove: {
        tooltip: {
          text: "Cliquez sur un tracé à supprimer", // Pas utilisé
        },
      },
    },
  };


  // Define you draw handler somewhere where you click handler can access it. N.B. pass any draw options into the handler
  polygonDrawer = new L.Draw.Polygon(map, {
    showArea: true,
    allowIntersection: false, // Restricts shapes to simple polygons
    drawError: {
      color: "#e1e100", // Color the shape will turn when intersects
      message:
        "<strong>Le polygone du toit ne peut pas avoir d'intersections !<strong>",
    },
    shapeOptions: {
      color: "#009FE3",
      opacity: 0.6,
      fillColor: "rgba(0,159,227,0.6)",
      fillOpacity: 0.8,
    },
  });

  /**
   * When user draw a polygon,
   * we trigger a Vue.js event that can be catch up by our parent
   */
  map.on("draw:created", function (e) {
    const layer = e.layer;
    const geodesicArea = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
    layer.properties = { ...props.drawEnabled };
    editableLayers.addLayer(layer);
    const centroid = layer.getCenter();
    layer.bindTooltip(
      `${(Math.round(geodesicArea)).toLocaleString("fr-FR")} m²`,
      { permanent: true, direction: "center", className: "textArea" },
    );
    emit("polygon:created", geodesicArea, centroid, props.drawEnabled?.area);
  });

  map.on("draw:edited ", function (e) {
    // Errors in types, don't trust it see https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html#l-draw
    const layers = e.layers;
    layers.eachLayer(function (layer) {
      const geodesicArea = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
      // Update tooltip-like on map with geodesic area updated
      layer.bindTooltip(
        `${(Math.round(geodesicArea)).toLocaleString("fr-FR")} m²`,
        { permanent: true, direction: "center", className: "textArea" },
      );
    });
    // Get all layer to have the sum of area
    const allLayers = editableLayers.getLayers();
    const totalGeodesicArea = allLayers.reduce((acc, layer) => {
      if (layer.properties.area === props.drawEnabled?.area) {
        acc += L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
      }
      return acc;
    }, 0);
    emit("polygon:edited", totalGeodesicArea, props.drawEnabled?.area);
  });

  map.on("draw:deleted ", function (e) {
    // Errors in types, don't trust it see https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html#l-draw
    const layers = e.layers;
    layers.eachLayer(function (layer) {
      if (layer.properties.area !== "roof") {
        const geodesicArea = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
        emit("polygon:deleted", geodesicArea, props.drawEnabled?.area);
      } else {
        editableLayers.addLayer(layer);
      }
    });
  });
});

function enableDraw (data: { area: "roof" | "garden" | "vegetable" | "allUsage", action?: "draw" | "clear" } | null) {
  if (data?.area === "garden") {
    if (data.action === "clear") {
      // Clear all layers related to garden
      const allLayers = editableLayers.getLayers();
      const idsToRemove = allLayers.reduce((acc, layer) => {
        if (layer.properties.area === "garden") {
          acc.push(layer._leaflet_id);
        }
        return acc;
      }, []);
      idsToRemove.forEach(id => {
        editableLayers.removeLayer(id);
      });
    } else {
      // Set custom style on draw
      polygonDrawer.setOptions({
        shapeOptions: {
          color: "#6ce868",
          opacity: 0.6,
          fillColor: "rgba(108,232,104,0.6)",
          fillOpacity: 0.8,
        },
      });
    }
  } else if (data?.area === "vegetable") {
    if (data.action === "clear") {
      // Clear all layers related to vegetable
      const allLayers = editableLayers.getLayers();
      const idsToRemove = allLayers.reduce((acc, layer) => {
        if (layer.properties.area === "vegetable") {
          acc.push(layer._leaflet_id);
        }
        return acc;
      }, []);
      idsToRemove.forEach(id => {
        editableLayers.removeLayer(id);
      });
    } else {
      // Set custom style on draw
      polygonDrawer.setOptions({
        shapeOptions: {
          color: "#f47e27",
          opacity: 0.6,
          fillColor: "rgba(244,126,39,0.6)",
          fillOpacity: 0.8,
        },
      });
    }
  } else if (data?.area === "allUsage") {
    if (data.action === "clear") {
      // Clear all layers when user change step
      const allLayers = editableLayers.getLayers();
      const idsToRemove = allLayers.reduce((acc, layer) => {
        if (layer.properties.area !== "roof") {
          acc.push(layer._leaflet_id);
        }
        return acc;
      }, []);
      idsToRemove.forEach(id => {
        editableLayers.removeLayer(id);
      });
    }
    // Disable draw
    return
  } else if (data?.area === "roof") {
    editableLayers.clearLayers();
    polygonDrawer.setOptions({
      shapeOptions: {
        color: "#009FE3",
        opacity: 0.6,
        fillColor: "rgba(0,159,227,0.6)",
        fillOpacity: 0.8,
      },
    });
  }
  polygonDrawer.enable();
  map.addControl(drawControl);
}

function disableDraw () {
  polygonDrawer.disable();
  map.removeControl(drawControl);
}

/**
 * When center prop evolve, we center the map to this new center,
 * with the initial zoom
 */
watch(() => props.center, (to) => {
  if (!map) return

  if (to.accuracy === undefined) {
    map.flyTo(to.latlng, 16, { animate: true })
  } else {
    map.flyToBounds(L.latLng(to.latlng).toBounds(to.accuracy), { animate: true })
  }
});

watch(() => props.drawEnabled, () => {
  if (props.drawEnabled?.area) enableDraw(props.drawEnabled);
  else disableDraw();
});

</script>

<style>
#map {
  height: 100%;
  width: 100%;
}

/**
 * Map styles
 */
.leaflet-editing-icon {
  height: 10px !important;
  margin-left: -5px !important;
  margin-top: -5px !important;
  width: 10px !important;
  border-radius: 50%;
}

.textArea {
  background: transparent;
  border: unset;
  color: white;
  font-size: larger;
  font-weight: bolder;
  box-shadow: unset;
}

.leaflet-touch .leaflet-bar {
  @apply rounded-md;

  a {
    @apply p-2.5 h-10 w-10 leading-none;

    &:first-child {
      @apply rounded-t-md;
    }
    &:last-child {
      @apply rounded-b-md;
    }

  }

  &.leaflet-draw-toolbar a {
    background-size: 307px 42px;
  }
}
.leaflet-touch .leaflet-right .leaflet-draw-actions {
  @apply mt-1.5 right-[42px];
}
</style>
