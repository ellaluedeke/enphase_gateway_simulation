import argparse
from attacks.api_spoof import run_spoof_attack
from attacks.power_disable import run_power_disable_attack
from attacks.lotl_install import run_lotl_attack
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run simulated Enphase attacks")
	parser.add_argument("--mode", choices=["spoof", "disable", "lotl"], required=True, help="Attack type")
	args = parser.parse_args()

	if args.mode == "spoof":
		run_spoof_attack()
	elif args.mode == "disable":
		run_power_disable_attack()
	elif args.mode == "lotl":
		run_lotl_attack()

