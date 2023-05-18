import random

weapons = {
	'weapon1': {'attack': 4, 'hit': 3, 'damage': 5, 'crit': 3},
	'weapon2': {'attack': 4, 'hit': 3, 'damage': 4, 'crit': 5}
}

defenders = {
	'defense1': {'defense': 4, 'save': 6},
	'defense2': {'defense': 3, 'save': 4}
}

def simulate_combat(weapon, defender):
	# throw and interpret attack dice
	attack_results = {'hit': 0, 'crit': 0, 'miss': 0}
	for i in [0:weapon['atttack']]:
		throw = random.randint(1, 6)
		if result == 6:
			attack_results['crit'] += 1
		elif result >= weapon['hit']:
			attack_results['hit'] += 1
		else:
			attack_results['miss'] += 1

	# throw and interpret defense dice
	defend_results = {'save': 0, 'crit': 0, 'miss': 0}
	for i in [0:defender['defense']]:
		throw = random.randint(1, 6)
		if result == 6:
			defend_results['crit'] += 1
		elif result >= defender['save']:
			defend_results['save'] += 1
		else:
			defend_results['miss'] += 1

	# use crit saves to negate crit attacks
	attack_results['crit'] -= defend_results['crit']
	# use remaining crit saves to negate normal attacks
	if attack_results['crit'] < 0:
		attack_results['hit'] -= attack_results['crit']
		attack_results['crit'] = 0

	# use normal saves to negate normal hits
	attack_results['hit'] -= defend_results['hit']
	# use remaining saves to save against crit hits
	if attack_results['hit'] < 0:
		if attack_results['crit'] > 0:
			# instead of wasting 1 save dice it's better to save a crit instead
			if attack_results['hit'] == -1:
				attack_results['hit'] = 1
				attack_results['crit'] -= 1
			else:
				attack_results['crit'] -= attack_results['hit'] / 2
				if attack_results['crit'] < 0:
					attack_results['crit'] = 0
		attack_results['hit'] = 0

	# calculate damage
	damage = attack_results['hit']*weapon['damage'] + attack_results['crit']*weapon['crit']
	return damage


for weapon_name, weapon in weapons.items():
	for defender_name, defender in defenders.items():
		# simulate 1000 cases, average out results
		sum_damage = 0
		for i in [0:1000]:
			sum_damage += simulate_combat(weapon, defender)
		average_damage = sum_damage / 1000
		print(f"{weapon_name} - {defender_name}: {average_damage}")
