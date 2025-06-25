# Enphase Gateway Simulation

This project simulates attacks against the Enphase Gateway API, inspired by real-world vulnerabilities.

**Reference Attacks:**
- *Spoofing Energy Production*:  
  [Hacking a Solar Power Controller and Pretending to Generate a Gigawatt](https://community.cadence.com/cadence_blogs_8/b/breakfast-bytes/posts/hacking-a-solar-power-controller-and-pretending-to-generate-a-gigawatt)

- *Power Control Exploit (Unauthenticated)*:  
  [Enphase API – Power Mode Exploit Documentation](https://github.com/Matthew1471/Enphase-API/blob/main/Documentation/IQ%20Gateway%20API/IVP/Mod/EID/Mode/Power.adoc)

---

## Components

### `enphase_sim.py`
- Simulated Flask API that mimics a real Enphase Gateway.
- Implements endpoints for login, inverter data, and power control.

### `run_attack.py`
- Command line interface tool to execute different attack modes using the `--mode` flag.

### `logs/`
- Stores all logs generated during simulated attacks.
  - `attack_log.txt` : Output log file that records attack events and timestamps.

### `attacks/`
- Modular attack implementations.
  - `__init__.py`: Module init file.
  - `api_spoof.py`: Spoofs energy production data via legitimate endpoints.
  - `power_disable.py`: Exploits unauthenticated power shutdown.
  - `lotl_install.py`: Living off the land (LoTL) attack using the firmware upgrade feature

### `utils/`
- Helper utilities and shared code.
  - `loggger.py`: Centralized logging module.
---
