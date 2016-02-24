from threading import Thread
from gi.repository import Gtk, GObject


class GUIFace:
    def __init__(self):
        GObject.threads_init()
        self.win = Gtk.Window(default_height=50, default_width=300)
        self.win.connect("delete-event", Gtk.main_quit)

        self.progress = Gtk.ProgressBar(show_text=True)
        self.win.add(self.progress)

    def set_text(self, toset):
        toset = "" if toset is None else toset
        self.progress.set_text(str(toset + ": {}%".format(100 * self.progress.get_fraction())))

    def set_percent(self, percent):
        self.progress.set_fraction(float(percent) / 100)
        current = "Running...:" if self.progress.get_text() is None else self.progress.get_text()
        self.set_text(str((current[current.index(":"):])))

    def add_percent(self, toadd):
        self.set_percent((100 * self.progress.get_fraction()) + toadd)

    def remove_percent(self, torem):
        self.set_percent((100 * self.progress.get_fraction()) - torem)

    def start(self, target):
        thread = Thread(target=target)
        thread.daemon = True
        thread.start()
        self.win.show_all()
        Gtk.main()
