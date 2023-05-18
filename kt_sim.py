import random

weapons = {
	'weapon1': {'attack': 4, 'hit': 3, 'damage': 5, 'crit': 3, 'ap': 2, 'mw': 3},
	'weapon2': {'attack': 4, 'hit': 3, 'damage': 4, 'crit': 5, 'ap': 1},
	'weapon3': {'attack': 4, 'hit': 3, 'damage': 3, 'crit': 4, 'rending': True},
	'weapon4': {'attack': 5, 'hit': 4, 'damage': 4, 'crit': 5, 'lethal': 5, 'piercing': 1},
	'weapon5': {'attack': 5, 'hit': 2, 'damage': 2, 'crit': 4, 'balanced': True, 'rending': True},
	'weapon6': {'attack': 4, 'hit': 2, 'damage': 3, 'crit': 4, 'ceaseless': True},
}

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

defenders = {
	'defense1': {'defense': 0, 'save': 6},
	'defense2': {'defense': 3, 'save': 2},
	'defense3': {'defense': 3, 'save': 3},
	'defense4': {'defense': 3, 'save': 4},
	'defense5': {'defense': 2, 'save': 5},
}


def throw_dice(dice, crit, hit, ceaseless=False):
	results = {'hit': 0, 'crit': 0, 'miss': 0}
	for i in [0:dice]:
		throw = random.randint(1, 6)
		if ceaseless and throw == 1:
			throw = random.randint(1, 6)
		if result >= crit:
			results['crit'] += 1
		elif result >= hit:
			results['hit'] += 1
		else:
			results['miss'] += 1
	return results


def simulate_combat(weapon, defender):
	# throw and interpret attack dice
	attack_results = throw_dice(weapon['attack'],
								weapon['lethal'],
								weapon['hit'],
								weapon['ceaseless'])

	# mortal wound is calculated immediately after crit roll
	damage = attack_results['crit'] * weapon['mw']

	# handle Balanced: only misses are rerolled
	if (weapon['balanced'] or weapon['relentless']) and attack_results['miss']:
		attack_results['miss'] -= 1
		rethrow = throw_dice(1, weapon['lethal'], weapon['hit'])
		for result, value in rethrow.items():
			attack_results[result] += value

	# handle Rending
	if weapon['rending'] and attack_results['crit'] and attack_results['hit']:
		attack_results['hit'] -= 1
		attack_results['crit'] += 1

	# throw and interpret defense dice
	if weapon['piercing'] and attack_results['crit'] and weapon['piercing'] > weapon['ap']:
		defender_dice = defender['defense'] - weapon['piercing']
	else:
		defender_dice = defender['defense'] - weapon['ap']
	defend_results = throw_dice(defender_dice, 6, defender['save'])

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
	damage += attack_results['hit']*weapon['damage'] + attack_results['crit']*weapon['crit']
	return damage


for weapon_name, weapon in weapons.items():
	for stat in weapon_defaults.keys:
		if stat not in weapon.keys:
			weapon[stat] = weapon_defaults[stat]
	for defender_name, defender in defenders.items():
		# simulate 1000 cases, average out results
		sum_damage = 0
		for i in [0:1000]:
			sum_damage += simulate_combat(weapon, defender)
		average_damage = sum_damage / 1000
		print(f"{weapon_name} - {defender_name}: {average_damage}")
