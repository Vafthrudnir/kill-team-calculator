<template>
    <v-select label="attacker" :items="teams" v-model="attacker" item-value="id" item-title="name"></v-select>
    <v-select label="defender" :items="teams" v-model="defender" item-value="id" item-title="name"></v-select>
    <v-btn @click="simulate_combat()">Simulate</v-btn>

    <v-table v-if="results.length">
        <thead>
          <tr>
            <th class="text-left">
              Attacker
            </th>
            <th class="text-left">
              Weapon
            </th>
            <th class="text-left">
              Defender
            </th>
            <th class="text-left">
              Expected damage
            </th>
            <th class="text-left">
              Deviation
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="combat_case in results"
            :key="combat_case.id"
          >
            <td>{{ combat_case.attacker }}</td>
            <td>{{ combat_case.weapon }}</td>
            <td>{{ combat_case.defender }}</td>
            <td>{{ parseFloat(combat_case.expected_damage).toFixed(2) }}</td>
            <td>{{ parseFloat(combat_case.deviation).toFixed(2) }}</td>
          </tr>
        </tbody>
    </v-table>
</template>

<script lang="ts">
import axios from 'axios'

export default {
    data() {
        return {
            results: [],
            teams: [],
            attacker: '',
            defender: ''
        }
    },
    methods: {
        load_teams() {
            const path ='http://localhost:5000/teams/'
            axios
                .get(path)
                .then((res) => {
                    this.teams = res.data
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        simulate_combat() {
            const path = 'http://localhost:5000/simulate'
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
