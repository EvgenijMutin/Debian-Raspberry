import gi
import socket

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import time
import threading


class slave(threading.Thread):
    def __init__(self, iter=200, port=6006):
        self.iter = iter
        self.value = 0
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread.__init__(self)

    def run(self):
        self.s.bind(('', self.port))
        self.s.settimeout(1)
        while self.iter > 0:
            self.iter = self.iter - 1
            time.sleep(1)
            try:
                self.value = str(self.s.recv(1024), encoding='utf-8')

            except:
                print('ждем сообщение')
        self.s.close()


s = slave()
s.start()


class MyWindow(Gtk.Window):

    def __init__(self, port=6007):
        Gtk.Window.__init__(self, title="controller")
        self.port = port

        self.box = Gtk.Box(spacing=15)
        self.add(self.box)

        self.label = Gtk.Label("Accel data")
        self.box.pack_start(self.label, True, True, 0)

        self.button1 = Gtk.Button(label="обновить")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.box.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.Button(label="режим акселерометра")
        self.button2.connect("clicked", self.on_button2_clicked)
        self.box.pack_start(self.button2, True, True, 0)

        self.button3 = Gtk.Button(label="передать цвет")
        self.button3.connect("clicked", self.on_button3_clicked)
        self.box.pack_start(self.button3, True, True, 0)

        self.entry = Gtk.Entry()
        self.box.pack_start(self.entry, True, True, 0)

        self.messenger = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.messenger.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def on_button1_clicked(self, widget):
        self.label.set_text(str(s.value))

    def on_button2_clicked(self, widget):
        print('акселерометр')
        self.messenger.sendto(bytes('ax', encoding='utf-8'), ('192.168.0.131', self.port))
        self.messenger.close()

    def on_button3_clicked(self, widget):
        print('передача цвета')
        print(self.entry.get_text())
        self.messenger.sendto(bytes(self.entry.get_text() + ' ', encoding='utf-8'), ('192.168.0.131', self.port))
        self.messenger.close()


time.sleep(1)
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
