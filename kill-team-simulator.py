import statistics
import json
import os
from flask import Flask

import simulate_combat, test_values


app = Flask(__name__)


weapon_defaults = {
	'ap': 0,
	'mw': 0,
	'lethal': 6,
	'rending': False,
	'piercing': 0,
	'balanced': False,
	'ceaseless': False,
	'relentless': False
}


@app.route("/simulate_all")
def simulate_all():
	SAMPLES = 100000

	results = ''
	for weapon_name, weapon in test_values.weapons.items():
		for stat in weapon_defaults.keys():
			if stat not in weapon.keys():
				weapon[stat] = weapon_defaults[stat]
		for defender_name, defender in test_values.defenders.items():
			# simulate SAMPLE cases, average out results
			damages = []
			for i in range(0,SAMPLES):
				damages.append(simulate_combat.simulate(weapon, defender))
			average_damage = statistics.mean(damages)
			deviation = statistics.stdev(damages)
			print(f'{weapon_name} - {defender_name}: {average_damage:.2f} - {deviation:.2f}')
			results += f'{weapon_name} - {defender_name}: {average_damage:.2f} - {deviation:.2f}\n'
	return '<pre>' + results + '</pre>'


@app.route("/teams/<team>")
def get_team(team):
	with open(f'datasets/{team}.json') as team_handler:
		team_dict = json.load(team_handler)
	return team_dict


@app.route("/teams/")
def get_team_list():
	response = '<pre>'
	res = []
	for path in os.listdir('datasets/'):
		if os.path.isfile(os.path.join('datasets/', path)):
			res.append(os.path.splitext(path)[0])
	print(res)
	return res
