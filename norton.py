# %% md
# # Norton's Theorem
# ## Let's draw the circuit first
# For that I will use schemdraw
# ### v1.0

# %% Draw
import schemdraw
schemdraw.use('svg')
elm=schemdraw.elements
d=schemdraw.Drawing(file='norton_ckt.svg')
d+=elm.SourceI().up()
d+=elm.Resistor().right()
d+=elm.Resistor().down().hold()
d+=(R:=elm.Resistor()).right()
d+=elm.Resistor().down().label('$R_L$')
d+=elm.Line().left().tox(0)
d+=elm.Ground()
d.draw()

# %% md
# ## Now the simulation
# For this I will use PySpice

# %% import
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# %% setup
logger = Logging.setup_logging()

# %% circuit
rl=1@u_kOhm
circuit = Circuit("Norton's Theorem")
circuit.R('1', 'input', 1, 1@u_kOhm)
circuit.R('3', 1, 'load', 1.5@u_kOhm)
circuit.R('2', 1, circuit.gnd, 2@u_kOhm)
circuit.I('', circuit.gnd, 'input', 1@u_A)
circuit.R('L', 'load', circuit.gnd, rl)

# %% simulate
simulator = circuit.simulator()
analysis = simulator.operating_point()
vl=u_V(float(analysis.load))

# %% rn
circuit = Circuit("Resistor network")
circuit.R('1', 'input', 1, 1@u_kOhm)
circuit.R('3', 1, 'load', 1.5@u_kOhm)
circuit.R('2', 1, circuit.gnd, 2@u_kOhm)
circuit.V('', 'load', circuit.gnd, (v:=1@u_V))

# %% simulate
simulator = circuit.simulator()
analysis = simulator.operating_point()
i=u_A(float(-analysis.v))
rn=v/i

# %% display
il=vl/rl
req=(rn*rl)/(rn+rl)
ino=vl/req
print('Norton equivalent current is: {:.2f} A'.format(float(ino)))
print('Current flowing through load is: {:.2f} A'.format(float(il)))
print('Norton equivalent resistance is: {:.2f} Ohm'.format(float(rn)))
