import statistics
import simulate_combat, test_values
from flask import Flask

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

	response = "<pre>"
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
			print(f"{weapon_name} - {defender_name}: {average_damage:.2f} - {deviation:.2f}")
			response += f"{weapon_name} - {defender_name}: {average_damage:.2f} - {deviation:.2f}\n"
	return response+"</pre>"
