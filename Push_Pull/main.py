from os import path, remove
from glob import glob
import sys
import config
from libs import download_videos
from libs import Youtube
from libs import YoutubeCheck
from libs import WaterMarker
from time import sleep

if __name__ == "__main__":
    currentDir = path.dirname(path.realpath(__file__))

    outputdir = currentDir
    temp_name = "/temp/"
    bin_name = "/bin/"

    print "Hello and welcome to the FaceTube translator (Starting)..." + \
          "\nCurrent Working directory: " + currentDir

    if not path.isfile(config.facebook_list_path) or not path.isdir(currentDir + "/"):
        exit("File and/or output folder not found... exiting")

    files = []
    print "Downloading videos..."
    try:
        files = download_videos(config.facebook_list_path, currentDir + temp_name)
    except IndexError:
        pass

    youtube_temp = Youtube(config.google_temp_clientid, config.google_temp_clientsecret)  # TEMP ACCOUNT

    checker = YoutubeCheck(config.google_temp_email, config.google_temp_pass)

    youtube_final = Youtube(config.google_final_clientid, config.google_final_clientsecret)  # FINAL ACCOUNT

    for filein in files:
        origname = filein[0]
        name = filein[1]
        desc = filein[2]
        youtube_temp.upload_video(currentDir + temp_name, name, desc, "22", "", "private")  # Upload to temp account
        print "Waiting for bad emails to come in..."
        for nums in range(60):
            print nums,
            sys.stdout.flush()
            sleep(1)
            print "\r",
    print "\nDone\nChecking using Gmail..."
    bad_videos = checker.check_videos()

    if not config.force_upload:
        for bad in bad_videos:
            for f in glob(currentDir + temp_name + bad + ".mp4"):
                remove(f)

    new_videos = glob(currentDir + temp_name)  # Get new list

    marker = WaterMarker()
    marker.setratiodivision(10, 10)
    marker.setdistance(5, 5)

    for new_video in new_videos:
        marker.setvideopath(new_video)
        marker.setwatermarkpath(config.watermark_path)
        marker.setoutput(new_video + "-checked.mp4")
        marker.run()
        youtube_final.upload_video(new_video + "-checked.mp4", new_video[:new_video.index(".mp4")], "desc",
                                   "22", "", "public")
    print "\n\n\n\n\nDONE!!! all videos but: " + bad_videos
