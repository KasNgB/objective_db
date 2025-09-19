import gi
from yolo_analysis import yolo_analysis


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk



class GridWindow(Gtk.Window):

    def __init__(self):


        super().__init__(title="Recognize apples")

        self.adjustment = Gtk.Adjustment(0.5, 0, 1, 0.01)
        self.selected_ip = None
        self.selected_conf = 0.5


        self.enter_ip = Gtk.Entry()
        self.enter_ip.connect("changed", self.on_enter_ip)

        self.button_run = Gtk.Button(label="run")
        self.button_run.connect("clicked", self.on_button_run_input)

        self.scale = Gtk.Scale(orientation=0, adjustment=self.adjustment)
        self.scale.set_digits(2)

        self.spinbutton = Gtk.SpinButton()
        self.spinbutton.set_adjustment(self.adjustment)
        self.spinbutton.set_digits(2)

        self.adjustment.connect("value-changed", self.on_adjustment_input)


        self.grid = Gtk.Grid()

        self.grid.add(self.enter_ip)
        self.grid.attach(self.button_run, 1, 0, 4, 1)
        self.grid.attach(self.scale, 0, 1, 2, 1)
        self.grid.attach_next_to(self.spinbutton, self.scale, 1, 2, 1)
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)

        self.add(self.grid)

    def on_enter_ip(self, widget):
        self.selected_ip = self.enter_ip.get_text()
        print(f"ip: {self.selected_ip}")

    def on_button_run_input(self, widget):
        try:
            if self.selected_ip == None:
                print("No file selected")
                return
            else:
                yolo_analysis(self.selected_file, self.selected_conf)
        except FileNotFoundError:
            print("You need to select an image")
 
    def on_adjustment_input(self, spin):
        self.selected_conf = self.adjustment.get_value()
        print(f"conf: {self.selected_conf}")

win = GridWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()

Gtk.main()
