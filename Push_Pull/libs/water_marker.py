from os import popen, system
from re import findall
from PIL import Image


class WaterMarker:
    def __init__(self):
        print "Starting WaterMarker...",
        self.videoPath = ""
        self.waterPath = ""
        self.outputVideo = ""

        self.videoDim = (None, None)
        self.waterDim = (None, None)

        self.overlay = (10, 10)
        self.division = (20, 20)

        print "Done"

    def setvideopath(self, pathtovideo):
        self.videoPath = pathtovideo
        print "Setting path to video %s... Done" % pathtovideo

    def setwatermarkpath(self, pathtowatermark):
        self.waterPath = pathtowatermark
        print "Setting path to watermark %s... Done" % pathtowatermark

    def setoutput(self, pathtovideo):
        self.outputVideo = pathtovideo
        print "Going to save end video in %s... Done" % pathtovideo

    def setdistance(self, x, y):
        self.overlay = (x, y)
        print "Set the overlay distance to %d x %d... Done" % self.overlay

    def setratiodivision(self, x, y):
        self.division = (x, y)
        print "Set ratio division for watermark to %d x %d... Done" % self.division

    def run(self):
        print "Getting ready to analyze the video...",
        lines = popen("avconv -i " + str(self.videoPath) + " 2>&1")
        print "Done\nChecking dimensions...",
        full = None
        for line in lines:
            iffound = findall(r'(\d+x\d+)', line)
            if str(iffound) != "[]":
                full = iffound[0]

        print "Done\nTrying to parse output...",

        if full is None:
            print "Couldn't get dimensions"
            exit("Video not found... exiting")

        try:
            self.videoDim = (int(full[:full.index("x")]), int(full[full.index("x") + 1:]))
        except ValueError:
            exit("Couldn't get dimensions from Video... exiting")

        print "Done\nVideo dimensions: %d x %d... Done\nImporting watermark..." % self.videoDim,
        im = None
        try:
            im = Image.open(self.waterPath)
        except IOError:
            exit("No watermark found!")

        self.waterDim = im.size

        print "Done\nWatermark dimensions %d x %d... Done\nGetting new ratio..." % (self.waterDim[0], self.waterDim[1]),
        newimagedim = (int(self.videoDim[0] / self.division[0]), int(self.videoDim[1] / self.division[1]))
        newvideodim = (int((self.videoDim[0] - (self.waterDim[0]/2)) / self.overlay[0]),
                       int((self.videoDim[1] - (self.waterDim[1])/2) / self.overlay[1]))
        print "Done\nResized watermark dimensions: %d x %d... Done" % newimagedim
        try:
            im.thumbnail(newimagedim, Image.ANTIALIAS)
            im.save("tempWaterMark.png", "PNG")
        except IOError:
            print "Couldn't resize watermark"

        print "Applying resized watermark to video (Might take a while)...",

        waters = system("avconv -v 0 -y -i " + self.videoPath + " -strict experimental -c:a aac -q:a 3 -vf "
                        "'movie=tempWaterMark.png [watermark];[in][watermark] overlay=" + str(newvideodim[0]) +
                        ":" + str(newvideodim[1]) + " [out]' " + self.outputVideo + " 2>&1")

        print "Done\nFinished watermarking video (output): %s" % self.outputVideo

        if waters != 0:
            exit("Error placing watermark on video....")

        return str(self.outputVideo)

# if ("'" in out) and ("x"):
# print str(re.findall(r'(\d+x\d+)', out))

# if __name__ == '__main__':
# youtube = Youtube()
# youtube.upload_video("/root/Downloads/WIN_20151221_17_54_52_Pro.mp4", "Coolest title", "This is a test description",
# "22", "cool, swag, amazing", "private")
