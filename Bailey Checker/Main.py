from GUI import ProgressBar, MessageDialog, FileDialog
from pytexter import Docxer
from time import sleep

gui = ProgressBar(50, 100)
dialog = FileDialog()
#message = MessageDialog("ERROR", "Couldn't load the requested folder")

doc = Docxer()


def exit_app(na):
    gui.destroy()
    #message.destroy()
    exit(0)


def on_start_app():
    files = doc.get_folder("/root/Downloads/SMELI_Essays/")
    doc.run_files("/root/Downloads/SMELI_Essays/", files, "/root/Downloads/SMELI_Essays/Good_Files/")
    exit(0)
    print "Analyzer Started"
    dialog_response = dialog.get_folder()
    if True:  # dialog_response[0]:
        print "okay"
        #message.connect(exit_app)
        #message.show()
        # exit_app()
    path = dialog_response[1]
    gui.set_percent(0)
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
