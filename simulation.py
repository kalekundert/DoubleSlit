#!/usr/bin/env python

from numpy import *

class Simulation:
    """ All of the physical calculations in this simulation are done by this
    class.  This separates the interface code from the simulation code, which
    is a good thing. """

    def __init__(self, main=None):
        """ Initialize the simulation with default values.  The simulation is
        also provided with a reference to the main interface object, although
        using this reference should never be necessary. """

        self.amplitude = 0
        self.frequency = 0
        self.displacement = 0

    def update(self, parameters):
        """ This method is called by the interface whenever a parameter is
        changed.  The new values of all the parameters are provided in a list.
        It should be used to update the internal state of the simulation so
        that the next call to plot() will produce the correct result. """

        self.amplitude = parameters[0]
        self.frequency = parameters[1]
        self.displacement =  2 * pi * parameters[2]

    def plot(self, independent):
        """ This method is called by the graphical interface whenever the
        graph is being redrawn.  This method is provided with the independent
        variable (i.e. x) and it is expected to return the corresponding
        dependent variable (i.e. y). """

        x = independent + self.displacement
        f = self.frequency; A = self.amplitude

        return A * cos(x / f)

# If this is run as a standalone script, then read parameters from the command
# line and display the resulting graph.  
if __name__ == "__main__":

    import sys
    from pylab import *

    # Convert all command line arguments to floats.
    inputs = sys.argv[1:]
    parameters = [float(input) for input in inputs]

    # Create and initialize a simulation objects.
    simulation = Simulation()
    simulation.update(parameters)

    # Generate the plot.
    x = arange(-pi, pi, 0.01)
    y = simulation.plot(x)

    # Display it using the builtin graphical interface.
    plot(x, y)
    show()
