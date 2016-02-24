from zipper import Zipper

totalPath = str(__file__).rfind("\\")
if totalPath == -1:
    totalPath = str(__file__).rfind("/")

path = str(__file__)[:totalPath + 1]

print path

zip = Zipper()
zip.create_zip("readyMan")
zip.add_dir(path + "imageZip")
zip.close_zip()
