# enphase_gateway_simulation
Simulated spoof attack on the Enphase Gateway API using the hack: https://community.cadence.com/cadence_blogs_8/b/breakfast-bytes/posts/hacking-a-solar-power-controller-and-pretending-to-generate-a-gigawatt

Also API attack in the power state to able to be switch off power without authentication:
https://github.com/Matthew1471/Enphase-API/blob/main/Documentation/IQ%20Gateway%20API/IVP/Mod/EID/Mode/Power.adoc

------------------------------------------------
Components:

- enphase_sim.py : Simulated Flask server mimicking Enphase Gateway
- run_attack.py : Command Line Interface to run selected attacks using --mode
- logs/
      - attack_log.txt : Output logs from attack
- attacks/
      - _init_.py
      - api_spoof.py : Spoofs energy production data
      - power_disable.py : Remotely disables power production
  - utils/
      - loggger.py : Logging utility

------------------------------------------------
