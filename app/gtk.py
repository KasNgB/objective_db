import gi


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk



class GridWindow(Gtk.Window):

    def __init__(self):


        super().__init__(title="Recognize apples")

        self.adjustment = Gtk.Adjustment(0.5, 0, 1, 0.01)


        self.file_chooser_button = Gtk.FileChooserButton(
        title="Select a File",
        action=Gtk.FileChooserAction.OPEN
        )
        self.file_chooser_button.connect("file-set", self.on_file_open)

        self.button_run = Gtk.Button(label="run")
        self.button_run.connect("clicked", self.on_button_run_input)

        self.scale = Gtk.Scale(orientation=0, adjustment=self.adjustment)
        self.scale.set_digits(2)
        self.scale.connect("value-changed", self.on_scale_input)

        self.spinbutton = Gtk.SpinButton()
        self.spinbutton.set_adjustment(self.adjustment)
        self.spinbutton.set_digits(2)
        self.spinbutton.connect("value-changed", self.on_spinbutton_input)


        self.grid = Gtk.Grid()

        self.grid.add(self.file_chooser_button)
        self.grid.attach(self.button_run, 1, 0, 4, 1)
        self.grid.attach(self.scale, 0, 1, 2, 1)
        self.grid.attach_next_to(self.spinbutton, self.scale, 1, 2, 1)
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)

        self.add(self.grid)

    def on_file_open(self, widget):
        filename = widget.get_filename()
        print(filename)

    def on_button_run_input(self, widget):
        print("run")

    def on_scale_input(self, scale):
        value = scale.get_value()
        print(value)

    def on_spinbutton_input(self, spin):
        value = spin.get_value()
        print(value)

win = GridWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()

Gtk.main()
