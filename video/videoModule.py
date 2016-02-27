from SimpleCV import Camera, VideoStream, Display
from multiprocessing import Process
import subprocess
import time
import datetime
import sys
from sys import argv
import os
import getopt

BUFFER_NAME = ''

def saveFilmToDisk(bufferName, outname):
    params = " -i {0} -c:v mpeg4 -b:v 700k -r 24 {1}".format(bufferName, outname)
    subprocess.call('ffmpeg'+params, shell=True)
    print ".mp4 file should have been generated at this step"
    try:
        os.remove(BUFFER_NAME)
    except:
        pass

class VideoModule:
    videoTitle =  time.strftime("%Y_%m_%d_%H_%M_%S")

    continueRecord = True

    width = 300
    height = 300

    makefilmProcess = Process()

    disp = 0

    def getVideoTitle(self):
        return self.videoTitle

    def getVideoDisplay(self):
        return self.disp

    def recordVideo(self, cb, length=5):
        global BUFFER_NAME

        BUFFER_NAME = 'buffer_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.avi'
        vs = VideoStream(fps=24, filename=BUFFER_NAME, framefill=True)
        self.disp = Display((self.width, self.height))
        cam = Camera(1, prop_set={"width":self.width,"height":self.height})

        while self.continueRecord:
            gen = (i for i in range(0, 30 * length) if self.continueRecord)
            for i in gen:
                img = cam.getImage()
                vs.writeFrame(img)
                img.save(self.disp)
            self.continueRecord = False
        print "Broke capture loop"
        self.disp.quit()

        print "Saving video"

        # This is to run this process asynchronously - we will skip that
        # self.makefilmProcess = Process(target=saveFilmToDisk, args=(BUFFER_NAME, self.videoTitle))
        # self.makefilmProcess.start()

        # Callback function
        cb()

    def getBufferName(self):
        global BUFFER_NAME
        return BUFFER_NAME

    def endCapture(self):
        self.continueRecord = False
        self.disp.quit()
        print "Set variable to false"

    def __init__(self, appendTitle):
        self.videoTitle += appendTitle + ".mp4"
