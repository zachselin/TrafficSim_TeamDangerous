# TrafficSim_TeamDangerous
Repo for UWB Computer Simulations course. Traffic simulation system.

As of now, the system is mostly a structural model of the freeway system.

Run with `python3 Main.py` or through Canopy. As of now there are mainly 4 variables to manipulate at the beginning of the file, but this is still evolving heavily.

Main.py relies on the implementation of Car in car.py. It also relies on the global variables/objects in shared.py. It is initiated by Main.py so that values are set at one time, and both car.py and Main.py utilize those globals, denoted with `g.<attribute>`.

