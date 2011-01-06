#!/usr/bin/env python

import os, sys
import gtk
import math

from numpy import *
from matplotlib.pyplot import plot, draw, xticks

from matplotlib.lines import Line2D
from matplotlib.figure import Figure

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

# Run in a different process.
if os.fork():
    raise SystemExit

class Main:

    def __init__(self):
        self.controls = None
        self.display = None
        self.simulation = None

        self.amplitude = None
        self.frequency = None
        self.displacement = None

    def setup(self, display, controls, simulation):
        self.display = display
        self.controls = controls
        self.simulation = simulation

        window = gtk.Window()
        window.set_default_size(500, 500)
        window.set_title("Double Slit Simulator")

        window.connect("show", self.update)
        window.connect("destroy", self.close)

        layout = gtk.VBox(False)
        window.add(layout)

        display.setup(layout)
        controls.setup(layout)

        """'
        self.amplitude = controls.parameter("Amplitude", -1, 1, 1)
        self.frequency = controls.parameter("Frequency", 0.1, 1, 1)
        self.displacement = controls.parameter("Displacement", -pi, pi)
        '"""

        window.show_all()

    def start(self):
        gtk.main()

    def update(self, *args):
        self.simulation.update()
        self.display.update()

    def close(self, *args):
        gtk.main_quit()

class Controls:

    def __init__(self, main):
        self.main = main
        self.parameters = []
        self.frame = self.table = None

    def add(self, *parameters):
        self.parameters.extend(parameters)

    def setup(self, layout):
        frame = gtk.Frame("Physical Properties")
        frame.set_border_width(10)

        layout.pack_start(frame, expand=False)

        table = gtk.Table(len(self.parameters), 3)
        table.set_border_width(5)
        table.set_col_spacings(10)

        frame.add(table)

        callback = self.main.update
        enumeration = enumerate(self.parameters)
        for row, parameter in enumeration:
            parameter.setup(table, row, callback)

class Parameter:

    def __init__(self, title, lowest, highest, default=None, format="%.2f"):
        self.title = title
        self.format = format

        self.lowest = lowest
        self.highest = highest

        if default is None: self.default = int(lowest + highest) // 2
        else:               self.default = default

        self.adjustment = None

    def setup(self, table, row, callback):
        name = gtk.Label(self.title)
        name.set_alignment(0, 0.5)

        self.adjustment = gtk.Adjustment(self.default,
                self.lowest, self.highest)

        scale = gtk.HScale(self.adjustment)
        scale.set_draw_value(False)
        scale.set_digits(3)

        value = gtk.Label()
        value.set_size_request(40, 17)
        value.set_alignment(0, 0.5)

        self.adjustment.connect("value_changed", callback)
        self.adjustment.connect("value_changed", self.update, value)

        self.update(self.adjustment, value)

        table.attach(name, 0, 1, row, row + 1, xoptions=gtk.FILL)
        table.attach(scale, 1, 2, row, row + 1)
        table.attach(value, 2, 3, row, row + 1, xoptions=0)

    def update(self, adjustment, value):
        percent = (adjustment.get_value() - self.lowest) / (self.highest - self.lowest)
        label = "%d%%" % (100 * percent)
        value.set_label(label)

class Display:

    def __init__(self, main):
        self.main = main
        self.abscissa = arange(-pi - .25, pi + 0.25, 0.01)

        self.curve = None
        self.canvas = None

    def setup(self, layout):
        color = array((237, 236, 234)) / 255.0
        figure = Figure(facecolor=color)
        axes = figure.add_subplot(111)

        # In order to create a line object, a dummy line needs to be plotted.
        # This line will get replaced before the GUI is shown to the user.
        x = y = self.abscissa

        self.curve = axes.plot(x, y)[0]
        self.canvas = FigureCanvas(figure)

        axes.set_xticks((-pi, 0, pi))
        axes.set_xticklabels((r"$-\pi$", "$0$", r"$\pi$"))
        axes.set_xlim(-pi - 0.25, pi + 0.25)

        axes.set_yticks((-1, 0, 1))
        axes.set_ylim((-1.1, 1.1))

        layout.pack_start(self.canvas)

    def update(self):
        main = self.main
        simulation = main.simulation
        ordinate = simulation.plot(self.abscissa)

        self.curve.set_ydata(ordinate)
        self.canvas.draw()

class Simulation:

    def __init__(self, main):
        self.main = main

        self.amplitude = 0
        self.frequency = 0
        self.displacement = 0

    def update(self):
        controls = self.main.controls
        parameters = controls.parameters

        self.amplitude = parameters[0].adjustment.get_value()
        self.frequency = parameters[1].adjustment.get_value()
        self.displacement = parameters[2].adjustment.get_value() * 2 * pi

    def plot(self, independent):
        x = independent + self.displacement
        f = self.frequency; A = self.amplitude

        return A * cos(x / f)

if __name__ == "__main__":
    main = Main()

    display = Display(main)
    controls = Controls(main)
    simulation = Simulation(main)

    amplitude = Parameter("Amplitude", -1, 1, 1)
    frequency = Parameter("Frequency", 0.1, 1, 1)
    displacement = Parameter("Displacement", -1, 1, 0)

    controls.add(amplitude, frequency, displacement)

    main.setup(display, controls, simulation)
    main.start()
