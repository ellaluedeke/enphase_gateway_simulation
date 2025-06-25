# enphase_gateway_simulation
Simulated spoof attack on the Enphase Gateway API using the hack: https://community.cadence.com/cadence_blogs_8/b/breakfast-bytes/posts/hacking-a-solar-power-controller-and-pretending-to-generate-a-gigawatt

Also API attack in the power state to able to be switch off power without authentication:
https://github.com/Matthew1471/Enphase-API/blob/main/Documentation/IQ%20Gateway%20API/IVP/Mod/EID/Mode/Power.adoc

------------------------------------------------
<pre> ```text gateway-sim/ ├── attacks/ │ ├── __init__.py │ ├── api_spoof.py │ └── power_disable.py ├── enphase_sim.py ├── run_attack.py ├── utils/ │ └── logger.py ├── logs/ │ └── attack_log.txt ├── README.md ``` </pre>
------------------------------------------------
