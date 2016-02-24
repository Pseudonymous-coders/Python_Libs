from GUI import ProgressBar
from time import sleep

gui = ProgressBar(50, 100)


def on_start_app():
    print "App started"
    gui.set_text("")
    while True:
        for a in range(100):
            gui.set_percent(a)
            gui.set_text("Who cares?")
            sleep(0.1)
        for a in range(100, 0, -1):
            gui.set_percent(a)
            gui.set_text("My caring cares")
            sleep(0.1)
        sleep(0.01)

if __name__ == "__main__":
    gui.start(on_start_app)
