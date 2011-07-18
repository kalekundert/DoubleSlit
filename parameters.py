import gtk

class Parameter:
    """ This class represents a single adjustable parameter.  Objects of this
    class should be managed by a Controls object.  It is also possible to
    subclass this class in order to control how the value of the parameter is
    formatted. """

    def __init__(self, title, lowest, highest, default=None, format='%0.2g'):
        """ The constructor initializes the parameter object with the
        information that is passed in.  If a default value isn't given, it is
        taken to be the average of the lowest and highest values. """

        assert highest > lowest

        self.title = title
        self.format = format

        self.lowest = lowest
        self.highest = highest

        if default is None: self.default = (lowest + highest) / 2
        else:               self.default = default

        self.adjustment = None

    def setup(self, table, row, callback):
        """ This method is called by the setup() method of a Controls object.
        That object provides a GTK table widget which this method can then
        fill in. """

        name = gtk.Label(self.title)
        name.set_alignment(0, 0.5)

        self.adjustment = gtk.Adjustment(self.default,
                self.lowest, self.highest)

        scale = gtk.HScale(self.adjustment)
        scale.set_draw_value(False)
        scale.set_digits(3)

        value = gtk.Label()
        value.set_size_request(60, 17)
        value.set_alignment(0, 0.5)

        self.adjustment.connect("value_changed", callback)
        self.adjustment.connect("value_changed", self.update, value)

        self.update(self.adjustment, value)

        table.attach(name, 0, 1, row, row + 1, xoptions=gtk.FILL)
        table.attach(scale, 1, 2, row, row + 1)
        table.attach(value, 2, 3, row, row + 1, xoptions=0)

    def update(self, adjustment, value):
        """ This method is called whenever the value of this parameter
        changes, so it is a good place to update the value being displayed.
        To have more control over how that value is formatted, create a
        subclass and overwrite this method. """

        label = self.format % adjustment.get_value()
        value.set_label(label)

class PercentParameter(Parameter):
    """ This is a subclass of the base Parameter class that formats the value
    of the slider as a percentage of the highest and lowest values. """

    def update(self, adjustment, value):
        """ Calculate the current percentage using the lowest and highest
        possible values. """

        current = float(adjustment.get_value() - self.lowest)
        range = float(self.highest - self.lowest)

        label = "%d%%" % (100 * current / range)
        value.set_label(label)
