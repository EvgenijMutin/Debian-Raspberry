import gi
import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from numpy import random


class Test:
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    def __init__(self):
        self.interface = Gtk.Builder()
        self.interface.add_from_file('UI.glade')
        self.interface.connect_signals(self)
        self.window = self.interface.get_object('Main')

        # first
        self.sw1 = self.interface.get_object('firstScrolled')
        self.fig1 = Figure()
        self.a1 = self.fig1.add_subplot(111)
        self.a1.plot(self.x1, self.y1)
        self.canvas1 = FigureCanvas(self.fig1)
        self.sw1.add_with_viewport(self.canvas1)

        # second
        self.sw2 = self.interface.get_object('secondScrolled')
        self.fig2 = Figure(figsize=(5, 5), dpi=100)
        self.a2 = self.fig2.add_subplot(111)
        self.a2.plot(self.x2, self.y2)
        self.canvas2 = FigureCanvas(self.fig2)
        self.sw2.add_with_viewport(self.canvas2)

        self.window.show_all()

    def on_button1_clicked(self, widget):
        print("Exit")
        sys.exit()

    def on_button2_clicked(self, widget):
        print("Plot2")
        self.x1.clear()
        self.y1.clear()
        i = 0
        while i < 20:
            self.x1.append(random.random() * 100)
            self.y1.append(random.random() * 100)
            i = i + 1
        print(self.x1)
        print(self.y1)
        self.a1.clear()
        self.a1.plot(self.x1, self.y1)
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas1.draw()
        self.window.show_all()
        self.window.queue_draw()

    def on_button3_clicked(self, widget):
        self.x2.clear()
        self.y2.clear()
        print("Plot1")
        i = 0
        while i < 20:
            self.x2.append(random.random() * 100)
            self.y2.append(random.random() * 100)
            i = i + 1
        print(self.x2)
        print(self.y2)
        self.a2.clear()
        self.a2.plot(self.x2, self.y2)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas2.draw()
        self.window.show_all()
        self.window.queue_draw()


if __name__ == '__main__':
    Test()
    Gtk.main()
