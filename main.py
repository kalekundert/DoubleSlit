#!/usr/bin/env python

import os, sys

from interface import Interface, Display, Controls
from parameters import PercentParameter, Parameter
from simulation import Simulation

# Return immediately if this is being imported in another module.
if __name__ == "__main__":

    # Run in a different process.
    if os.fork():
        sys.exit()

    # Instantiate the main interface object.
    main = Interface()

    # Create the other components of the interface...
    display = Display(main)
    controls = Controls(main)
    simulation = Simulation(main)

    # ...and add a set of slider controls to it.
    electronMass= 9.10938188e-31 # Kg
    c = 299792458
    width= Parameter("Width of Slits", 1e-8, 1)
    space= Parameter("Distance Between Slits", 1e-6, 1)
    momentum = Parameter("Momentum of Particle", 0.01*c*electronMass, c*1000*electronMass, 9*c*electronMass)	
    distanceSource = Parameter("Distance from Source to Aperture", 1, 1000, 200)
    distanceObs = Parameter("Distance from Aperture to Observation Screen", 1, 1000, 200)

    controls.add(width, space, momentum, distanceSource, distanceObs)

    # Hook up the interface components and begin the event loop.
    main.setup(display, controls, simulation)
    main.start()
