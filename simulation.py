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

        self.width= 0
        self.distance= 0
        self.mass= 0
	self.velocity= 0

    def update(self, parameters):
        """ This method is called by the interface whenever a parameter is
        changed.  The new values of all the parameters are provided in a list.
        It should be used to update the internal state of the simulation so
        that the next call to plot() will produce the correct result. """

        self.width = parameters[0]
        self.distance = parameters[1]
        self.mass = parameters[2]
	self.velocity = parameters[3]

    def plot(self, independent):
        """ This method is called by the graphical interface whenever the
        graph is being redrawn.  This method is provided with the independent
        variable (i.e. x) and it is expected to return the corresponding
        dependent variable (i.e. y). """

        x = independent
	a = self.width
	b = self.distance
	inot = 1
	h = 6.62606896e-34
	hbar = h / (2 * pi)
	k = self.mass * self.velocity / hbar
	angle = 0 
	u = (a * k / 2) * (sin(angle) + x)	
	v = (b / a) * u
	
	return inot * (sin(u) / u)**2 * (cos(v)**2)

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
