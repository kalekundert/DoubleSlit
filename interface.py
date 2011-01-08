import gtk
import numpy

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg

class Interface:
    """ This is the highest level graphical interface class.  It organizes all
    of the other interface classes into a window and manages input events. """

    def __init__(self):
        """ Initializes most of the attributes to null pointers.  Further
        setup is performed in the setup() method. """

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

        window.show_all()

    def start(self):
        gtk.main()

    def update(self, *ignore):
        values = self.controls.values()
        self.simulation.update(values)
        self.display.update()

    def close(self, *args):
        gtk.main_quit()

class Controls:
    """ This class is responsible for controls on the bottom part of the
    window.  Whenever the values of these bars change, the simulation as a
    whole needs to be updated.  This class initiates the update and provides
    the new values of the controls. """

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

    def values(self):
        return [parameter.adjustment.get_value()
                for parameter in self.parameters]

class Display:
    """ This class is responsible for rendering the graph in the upper portion
    of the window.  The data in the graph is taken from a Simulation object,
    which is accessed through the main Interface object. """

    # This is a color I chose to perfectly match the background of the rest of
    # the interface.  It might only work on my computer.
    background = "#edecea" 

    def __init__(self, main):
        self.main = main

        pi = numpy.pi
        self.abscissa = numpy.arange(-pi - .25, pi + 0.25, 0.01)

        self.curve = None
        self.canvas = None

    def setup(self, layout):
        """ This method creates the graph that is displayed on the top half of
        the user interface.  Currently, the axes are completely hard-coded in
        this method and cannot be changed on-the-fly. """

        figure = Figure(facecolor=Display.background)
        axes = figure.add_subplot(111)

        # In order to create a line object, a dummy line needs to be plotted.
        # This line will get replaced before the GUI is shown to the user.
        pi = numpy.pi
        x = y = self.abscissa

        self.curve = axes.plot(x, y)[0]
        self.canvas = FigureCanvasGTKAgg(figure)

        # The tick labels are formatted using LaTeX.  This makes it possible
        # to use symbols like pi.
        axes.set_xticks((-pi, 0, pi))
        axes.set_xticklabels((r"$-\pi$", "$0$", r"$\pi$"))
        axes.set_xlim(-pi - 0.25, pi + 0.25)

        axes.set_yticks((-1, 0, 1))
        axes.set_yticklabels((r"$-1$", "$0$", r"$1$"))
        axes.set_ylim((-1.1, 1.1))

        layout.pack_start(self.canvas)

    def update(self):
        """ This method updates the graph using the new ordinate values
        returned by the simulation. """

        main = self.main
        simulation = main.simulation
        ordinate = simulation.plot(self.abscissa)

        self.curve.set_ydata(ordinate)
        self.canvas.draw()
