<template>
    <v-select label="attacker" :items="teams" v-model="attacker"></v-select>
    <v-select label="defender" :items="teams" v-model="defender"></v-select>
    <v-btn @click="simulate_combat()">Load Teams</v-btn>
    <div class="text-body-2">results: {{ results }}</div>
</template>

<script lang="ts">
import axios from 'axios'

export default {
    data() {
        return {
            results: "",
            teams: [],
            attacker: '',
            defender: '',
        }
    },
    methods: {
        load_teams() {
            const path ='http://localhost:5000/teams/'
            axios
                .get(path)
                .then((res) => {
                    this.teams = res.data
                    this.attacker = this.teams[0]
                    this.defender = this.teams[0]
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        simulate_combat() {
            const path ='http://localhost:5000/simulate'
            const payload = {
                attacker: this.attacker,
                defender: this.defender
            }
            axios
                .put(path, payload)
                .then((res) => {
                    this.results = res.data
                })
                .catch((error) => {
                    console.error(error)
                })
        }
    },
    created() {
        this.load_teams()
    }
}
</script>
