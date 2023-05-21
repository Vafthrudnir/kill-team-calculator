import math
import random


def throw_dice(dice, crit, hit, ceaseless=False):
	results = {'hit': 0, 'crit': 0, 'miss': 0}
	for i in range(0,dice):
		throw = random.randint(1, 6)
		if ceaseless and throw == 1:
			throw = random.randint(1, 6)
		if throw >= crit:
			results['crit'] += 1
		elif throw >= hit:
			results['hit'] += 1
		else:
			results['miss'] += 1
	return results


def simulate(weapon, defender):
	# throw and interpret attack dice
	attack_results = throw_dice(weapon['attack'],
								weapon['lethal'],
								weapon['hit'],
								weapon['ceaseless'])

	# mortal wound is calculated immediately after crit roll
	damage = attack_results['crit'] * weapon['mw']

	# handle Balanced and Relentless: only misses are rerolled
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

	# use crit saves to negate crit attacks, only use the rest for normal attacks
	results = {'hit': 0, 'crit': 0}
	if attack_results['crit'] >= defend_results['crit']:
		results['crit'] = attack_results['crit'] - defend_results['crit']
		results['hit'] = attack_results['hit']
	else:
		results['crit'] = 0
		results['hit'] = attack_results['hit'] - attack_results['crit'] - defend_results['crit']

	if defend_results['hit'] > 0:
		# special case: better to let 1 normal hit go in and deflect a crit than to waste a save
		if results['crit'] > 0 and results['hit'] == defend_results['hit'] + 1:
			results['hit'] = 1
			results['crit'] -= 1
		# use normal saves for normal hits
		elif results['hit'] >= defend_results['hit']:
			results['hit'] -= defend_results['hit']
		# and if there's any left use it for crits
		else:
			results['crit'] -= math.floor((defend_results['hit'] - results['hit'])/2)
			results['hit'] = 0

	# calculate damage
	damage += results['hit']*weapon['damage'] + results['crit']*weapon['crit']
	return damage
