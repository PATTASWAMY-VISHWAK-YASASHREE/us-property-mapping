<template>
  <div class="map-view">
    <MapExplorer />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import MapExplorer from '@/components/map/MapExplorer.vue'

export default defineComponent({
  name: 'MapView',
  components: {
    MapExplorer
  }
})
</script>

<style scoped>
.map-view {
  height: 100vh;
  width: 100%;
}
</style>