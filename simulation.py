#!/usr/bin/env python

from numpy import *
import scipy
from scipy.special import fresnel

class Simulation:
    """ All of the physical calculations in this simulation are done by this
    class.  This separates the interface code from the simulation code, which
    is a good thing. """

    def __init__(self, main=None):
        """ Initialize the simulation with default values.  The simulation is
        also provided with a reference to the main interface object, although
        using this reference should never be necessary. """

        self.width= 0
        self.space= 0
        self.momentum= 0
	self.distanceSource= 0
	self.distanceObs= 0

    def update(self, parameters):
        """ This method is called by the interface whenever a parameter is
        changed.  The new values of all the parameters are provided in a list.
        It should be used to update the internal state of the simulation so
        that the next call to plot() will produce the correct result. """

        self.width = parameters[0]
        self.space = parameters[1]
        self.momentum = parameters[2]
	self.distanceSource = parameters[3]
	self.distanceObs= parameters[4]

    def plot(self, independent):
        """ This method is called by the graphical interface whenever the
        graph is being redrawn.  This method is provided with the independent
        variable (i.e. x) and it is expected to return the corresponding
        dependent variable (i.e. y). """

        #x = independent
	#a = self.width
	#b = self.space
	#inot = 1
	#h = 6.62606896e-34
	#hbar = h / (2 * pi)
	#k = self.momentum / hbar
	#angle = 0 
	#u = (a * k / 2) * (sin(angle) + x)	
	#v = (b / a) * u
	
	#return inot * (sin(u) / u)**2 * (cos(v)**2)

	h = 6.62606896e-34
        wavelen = h / self.momentum
        x = independent
	a = self.width
	b = self.space
        d1 = self.distanceSource
        d2 = self.distanceObs
	inot = 1
        y = ((2 / wavelen) * ((1/d1) + (1/d2)))**(1/2)

        utop1 = y * ((d1/(d1+d2)) * (x + (b/2)) + (a/2))
        utop2 = y * ((d1/(d1+d2)) * (x + (b/2)) - (a/2))

        ubottom1 = y * ((d1/(d1+d2)) * (x - (b/2)) + (a/2))
        ubottom2 = y * ((d1/(d1+d2)) * (x - (b/2)) - (a/2))
        
        (ssat2, ccat2) = scipy.special.fresnel(utop2)
        (ssat1, ccat1) = scipy.special.fresnel(utop1)

        (ssab2, ccab2) = scipy.special.fresnel(ubottom2)
        (ssab1, ccab1) = scipy.special.fresnel(ubottom1)

        print ssat1
        print ssat2
        fsin1 = ssat1 - ssat2
        fcos1 = ccat1 - ccat2
        fint1 = fcos1 + (fsin1*1j)

        fsin2 = ssab1 - ssab2
        fcos2 = ccab1 - ccab2
        fint2 = fcos2 + (fsin2*1j)
        
        finttotal = abs(fint1 + fint2)
        diffract = 1/2 * 1 * (finttotal**2)
        return diffract


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
