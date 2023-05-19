import statistics
import simulate_combat

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


SAMPLES = 100000

for weapon_name, weapon in weapons.items():
	for stat in weapon_defaults.keys():
		if stat not in weapon.keys():
			weapon[stat] = weapon_defaults[stat]
	for defender_name, defender in defenders.items():
		# simulate SAMPLE cases, average out results
		damages = []
		for i in range(0,SAMPLES):
			damages.append(simulate_combat.simulate(weapon, defender))
		average_damage = statistics.mean(damages)
		deviation = statistics.stdev(damages)
		print(f"{weapon_name} - {defender_name}: {average_damage:.2f} - {deviation:.2f}")
