<template>
  <ul class="list" v-if="flights.length">
    <h3>{{flights[0].created}}</h3>
    <FlightItem 
      v-for="(flight, index) in flights" 
      :index="index" 
      :flight="flight"
      :key="index"
    />
  </ul>
</template>

<script>
import FlightItem from './FlightItem.vue'

export default {
  name: 'List',
  components: { FlightItem },
  data() {
      return { flights: [] }
  },
  created() {
      return fetch("http://localhost:5000/flights")
        .then(res => res.json())
        .then(json => {
            this.flights = json
        })
  }
}
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  width: 100%;
}
a {
  color: #42b983;
}
</style>
