<template>
    <li>
        <a :href="linkUrl()" class="flight-item">
            <strong>${{flight.cost}} to {{flight.destination}}</strong> ({{flight.code}})
        </a>
        <div class="flight-item">
            from {{flight.dates}}
        </div>

         <button>Share the shit out of it!</button>
    </li>
</template>

<script>
export default {
  props: {
      flight: {
          type: Object,
          required: false
      }
  },
  methods: {
      linkUrl: function() {
          return `https://airfarewatchdog.com/${this.flight.url}`
      }
  }
}
</script>

<style scoped>
li {
  padding: 5px;
  display: flex;
  flex-direction: row;
  align-items: row;
  justify-content: flex-start;
}
li:first-child {
  margin-left: auto;
}

button {
  border: 1px solid black;
  border-radius: 3px;
}

.flight-item {
  width: 33%;
}

button:hover {
  background: black;
  color: grey;
  cursor: pointer;
}
</style>
