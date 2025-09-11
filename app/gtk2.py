import gi


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk



class GridWindow(Gtk.Window):

    def __init__(self):


        super().__init__(title="Recognize apples")


        button = Gtk.Button(label="Select an image")

        adjustment = Gtk.Adjustment(0.5, 0, 1, 0.01)

        scale = Gtk.Scale(orientation=0, adjustment=adjustment)
        scale.set_digits(2)

        spinbutton = Gtk.SpinButton()
        spinbutton.set_adjustment(adjustment)
        spinbutton.set_digits(2)


        grid = Gtk.Grid()

        grid.add(button)
        grid.attach(scale, 0, 1, 2, 1)
        grid.attach_next_to(spinbutton, scale, 1, 2, 1)

        self.add(grid)



win = GridWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()

Gtk.main()
