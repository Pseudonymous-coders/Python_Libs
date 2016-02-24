from threading import Thread
from gi.repository import Gtk, GObject


class ProgressBar:
    def __init__(self, width, height):
        GObject.threads_init()
        self.win = Gtk.Window(default_height=height, default_width=width)
        self.win.connect("delete-event", Gtk.main_quit)
        self.win.resize(width=width, height=height)
        self.win.set_resizable(False)

        self.progress = Gtk.ProgressBar(show_text=True)
        self.win.add(self.progress)

    def set_text(self, toset):
        toset = "" if "%" in str("" if toset is None else toset) else toset
        self.progress.set_text(str(toset + ": {}%".format(100 * self.progress.get_fraction()))
                               if toset is not "" else str(100 * self.progress.get_fraction()) + " %")

    def set_percent(self, percent):
        self.progress.set_fraction(float(percent) / 100)
        current = "Running...:" if self.progress.get_text() is None else self.progress.get_text()
        self.set_text(str((current[current.index(":"):])) if ":" in current else "")

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
