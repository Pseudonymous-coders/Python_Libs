from GUI import GUIFace
from time import sleep

gui = GUIFace()


def on_start_app():
    print "App started"
    gui.set_text("")
    while True:
        for a in range(100):
            gui.add_percent(1)
            gui.set_text("")
            sleep(0.1)
        for a in range(100, 0):
            gui.remove_percent(1)
            gui.set_text("")
            sleep(0.1)
        sleep(0.01)


if __name__ == "__main__":
    gui.start(on_start_app)
