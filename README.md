# enphase_gateway_simulation
Simulated spoof attack on the Enphase Gateway API using the hack: https://community.cadence.com/cadence_blogs_8/b/breakfast-bytes/posts/hacking-a-solar-power-controller-and-pretending-to-generate-a-gigawatt

Also API attack in the power state to able to be switch off power without authentication:
https://github.com/Matthew1471/Enphase-API/blob/main/Documentation/IQ%20Gateway%20API/IVP/Mod/EID/Mode/Power.adoc

------------------------------------------------
gateway-sim/
├── attacks/
│ ├── init.py
│ ├── api_spoof.py # Attack to spoof energy production data
│ └── power_disable.py # Attack to remotely disable production
├── enphase_sim.py # Flask app simulating an Enphase Gateway
├── run_attack.py # Command-line attack runner
├── utils/
│ └── logger.py # Logging utility
├── logs/
│ └── attack_log.txt # Output logs from attack runs
├── README.md
------------------------------------------------
