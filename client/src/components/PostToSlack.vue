<template>
    <form v-on:submit="formSubmit">
        <label for="n">Share the top: </label>
        <input type="number" id="n" v-model.number="number">
        <button type="submit">to Slack</button>
    </form>
</template>

<script>
export default {
    name: 'PostToSlack',
    data() {
        return { number: 5 }
    },
    methods: {
        formSubmit: async function(e) {
            e.preventDefault();
            const n = JSON.stringify({number: this.number});
            
            const response = await fetch('http://localhost:5000/slack', {
                    method: 'post',
                    body: n,
                    headers:{
                        'Content-Type': 'application/json'
                    }
                });
            return await response.json();

        }
    }
}
</script>

<style scoped>
</style>
