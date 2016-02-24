from os import *
from zipfile import *


class Zipper:
    def __init__(self):
        self.zip = None
        self.zipName = ""

    def create_zip(self, zipname):
        self.zip = ZipFile(zipname + ".zip", "w")
        self.zipName = zipname

    def close_zip(self):
        self.zip.close()

    def add_file(self, pathtofile):
        self.zip.write(pathtofile, "#"+pathtofile, ZIP_DEFLATED)

    def add_dir(self, paths):
        self.zip.start_dir = "paths"
        for root, dirs, files in walk(paths):
            for filein in files:
                self.add_file(paths + "/" + filein)
