<template>
  <div id="app">
    <PostToSlack />
    <List />
  </div>
</template>

<script>
import List from './components/FlightList.vue'
import PostToSlack from './components/PostToSlack.vue'

export default {
  name: 'app',
  components: {
    List,
    PostToSlack
  }
}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
