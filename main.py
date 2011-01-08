#!/usr/bin/env python

import os, sys

from interface import Interface, Display, Controls
from parameters import PercentParameter
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
    amplitude = PercentParameter("Amplitude", -1, 1, 1)
    frequency = PercentParameter("Frequency", 0.1, 1, 1)
    displacement = PercentParameter("Displacement", -1, 1, 0)
    mass = PercentParameter("Particle Mass", -1, 1, 1)

    controls.add(amplitude, frequency, displacement, mass)

    # Hook up the interface components and begin the event loop.
    main.setup(display, controls, simulation)
    main.start()
