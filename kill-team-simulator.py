import statistics
import json
import os
from flask import Flask, request

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

SAMPLES = 10000


def combine_operatives(attacker_dict, defender_dict):
	results = ''
	for weapon_name, weapon in attacker_dict.items():
		print(weapon_name)
		for stat in weapon_defaults.keys():
			if stat not in weapon.keys():
				weapon[stat] = weapon_defaults[stat]
		for defender_name, defender in defender_dict.items():
			# simulate SAMPLE cases, average out results
			damages = []
			for i in range(0,SAMPLES):
				damages.append(simulate_combat.simulate(weapon, defender))
			average_damage = statistics.mean(damages)
			deviation = statistics.stdev(damages)
			print(f'{weapon_name} - {defender_name}: {average_damage:.2f} - {deviation:.2f}')
			results += f'{weapon_name} - {defender_name}: {average_damage:.2f} - {deviation:.2f}\n'
	return results


@app.route('/simulate_all')
def simulate_all():
	results = combine_operatives(test_values.weapons, test_values.defenders)
	return '<pre>' + results + '</pre>'


@app.route('/teams/<team>')
def get_team(team):
	team_details = load_team(team)
	return team_details if team_details else (f'team "{team}" does not exist!', 400)


def load_team(team):
	try:
		with open(f'datasets/{team}.json') as team_handler:
			team_dict = json.load(team_handler)
	except OSError:
			return None
	return team_dict


@app.route('/teams/')
def get_team_list():
	response = '<pre>'
	res = []
	for path in os.listdir('datasets/'):
		if os.path.isfile(os.path.join('datasets/', path)):
			res.append(os.path.splitext(path)[0])
	print(res)
	return res


@app.route('/simulate')
def simulate():
	content = request.json
	attacker = load_team(content['attacker'])
	defender = load_team(content['defender'])
	if attacker == None:
		return f'team {content["attacker"]} does not exist!', 400
	elif defender == None:
		return f'team "{content["defender"]}" does not exist!', 400

	attacker_dict = {}
	for attacker_description in attacker.values():
		for operative, op_details in attacker_description['operatives'].items():
			try:
				for weapon_name, weapon in op_details['ranged-weapons'].items():
					attacker_dict[f'{operative} - {weapon_name}'] = weapon
			except KeyError:
				pass
		for equipment, eq_details in attacker_description['equipment'].items():
			try:
				if eq_details['stand-alone']:
					attacker_dict[f'{equipment}'] = eq_details['stats']
			except KeyError:
				pass

	defender_dict = {}
	for defender_description in defender.values():
		for operative, op_details in defender_description['operatives'].items():
			defender_dict[operative] = op_details['stats']

	results = combine_operatives(attacker_dict, defender_dict)
	return '<pre>' + results + '</pre>'
