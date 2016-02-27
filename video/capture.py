import time
from userSettings import LENGTH
from videoModule import VideoModule as video
from audioModule import AudioModule as audio
from videoModule import saveFilmToDisk
from threading import Thread
from msvcrt import getch	# MICROSOFT WINDOWS MODULE
import os

objs = []

def externalKill():
	print "Ending capture"
	global objs
	for o in objs:
		o.endCapture()

# def keypressKill(obj):
# 	getch()		# Essentially just wait for keypress
# 	print "Ending capture"
# 	for o in obj:
# 		o.endCapture()

# def clickKill(vidObj, obj):
# 	while(vidObj.getVideoDisplay() == 0):
# 		pass;

# 	while(vidObj.getVideoDisplay().isNotDone()):
# 		if vidObj.getVideoDisplay().mouseLeft:
# 			print "Ending capture"
# 			for o in obj:
# 				o.endCapture()

vCapture = video('')
aCapture = audio('')

n_finished = 0

def cb():
	global n_finished
	print "Callback function -" + str(n_finished) + " FINISHED"
	n_finished += 1
	if (n_finished == 2):
		print "Calling main callback function"
		cb_stop()

cb_stop = cb

def clipCapture(topic, stop):
	videoTitle = topic

	global vCapture
	global aCapture

	global cb_stop

	vCapture = video(videoTitle)
	aCapture = audio(videoTitle)

	cb_stop = stop

	threads = []

	threads.append(Thread(target=aCapture.recordAudio, args=(cb, LENGTH, )))
	threads.append(Thread(target=vCapture.recordVideo, args=(cb, LENGTH, )))
	#threads.append(Thread(target=clickKill, args=(vCapture, [vCapture, aCapture],)))
	#threads.append(Thread(target=keypressKill, args=([vCapture, aCapture],)))

	for t in threads:
		t.start()

	# threads[0].join()
	
	# print "Output file: " + vCapture.getVideoTitle()

	# saveFilmToDisk('buffer.avi', vCapture.getVideoTitle())
	# aCapture.saveToDisk();

	# os.system("ffmpeg -i " + vCapture.getVideoTitle() + " -i " + aCapture.getAudioTitle() + " -c:v copy -c:a copy awesomeMix.avi" + "\n")

	# global objs

	# objs = [vCapture, aCapture]