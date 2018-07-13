<template>
  <line-chart :data="flights" :legend="false" prefix="$"/>
</template>

<script>
import Vue from 'vue'
import VueChartkick from 'vue-chartkick'
import Chart from 'chart.js'
Vue.use(VueChartkick, {adapter: Chart})

export default {
  name: 'FlightGraph',
  data() {
      return { flights: [] }
  },
  created() {
      return fetch("http://localhost:5000/graph")
        .then(res => res.json())
        .then(json => {
            this.flights = json
        })
  }
}
</script>

<style></style>
