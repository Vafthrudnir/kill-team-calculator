import statistics
import json
import os
import hashlib, base64
from flask import Flask, request
from flask_cors import CORS

import simulate_combat


app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

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
	results = []
	for attacker, weapon in attacker_dict.items():
		for stat in weapon_defaults.keys():
			if stat not in weapon.keys():
				weapon[stat] = weapon_defaults[stat]
		for defender_name, defender in defender_dict.items():
			# simulate SAMPLE cases, average out results
			damages = []
			for i in range(0,SAMPLES):
				damages.append(simulate_combat.simulate(weapon, defender))
			expected_damage = statistics.mean(damages)
			deviation = statistics.stdev(damages)
			print(f'{attacker} - {defender_name}: {expected_damage:.2f} - {deviation:.2f}')
			uid = hashlib.md5(
				str.encode(
					f'{attacker[0] or "equipment"}-{attacker[1]}-{defender_name}'
				)).digest()
			result_dict = {
				"id": base64.b64encode(uid).decode(),
				"attacker": attacker[0] or 'equipment',
				"weapon": attacker[1],
				"defender": defender_name,
				"expected_damage": expected_damage,
				"deviation": deviation
			}
			results.append(result_dict)
	return results


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
	team_dict['id'] = team
	return team_dict


@app.route('/teams/')
def get_all_teams():
	res = []
	for path in os.listdir('datasets/'):
		if os.path.isfile(os.path.join('datasets/', path)):
			team = os.path.splitext(path)[0]
			res.append(load_team(team))
	print(res)
	return res


@app.route('/simulate', methods=['PUT'])
def simulate():
	content = request.json
	attacker = load_team(content['attacker'])
	defender = load_team(content['defender'])
	if attacker == None:
		return f'team {content["attacker"]} does not exist!', 400
	elif defender == None:
		return f'team "{content["defender"]}" does not exist!', 400

	attacker_dict = {}
	for operative, op_details in attacker['operatives'].items():
		try:
			for weapon_name, weapon in op_details['ranged-weapons'].items():
				attacker_dict[(operative, weapon_name)] = weapon
		except KeyError:
			pass
	for equipment, eq_details in attacker['equipment'].items():
		try:
			if eq_details['stand-alone']:
				attacker_dict[(None, equipment)] = eq_details['stats']
		except KeyError:
			pass

	defender_dict = {}
	for operative, op_details in defender['operatives'].items():
		defender_dict[operative] = op_details['stats']

	return combine_operatives(attacker_dict, defender_dict)
