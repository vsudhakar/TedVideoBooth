# Ted Video Booth - UI with Kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.event import EventDispatcher

import sys
sys.path.insert(0, './video/')

from capture import *
from videoModule import *

from threading import Thread

Builder.load_string("""
<GridLayout>
    canvas.before:
		Color:
			#rgba: 0.89, 0.167, 0.117, 1    #TEDx Color
			rgba: 0, 0, 0, 1
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            border: 10, 10, 10, 10
            pos: self.pos
            size: self.size

<IntroScreen>
    GridLayout:
    	id: intro_layout
        size_hint: .9, .9
        pos_hint: {'center_x': .5, 'center_y': .5}
        rows:4
        Label:
        	text: 'TEDxUNC Presents Bodies'
        	font_size: 50
        	color: (0.89, 0.167, 0.117, 1)
		Label:
			text: 'VIDEO EDITION'
			font_size: 40
			color: (0.89, 0.167, 0.117, 1)
		Button:
			text: 'Start!'
			font_size: 30
			color: (1, 1, 1, 1)
			on_press: root.manager.current = 'prompt1'
        Image:
        	source: './res/logo.png'
        	allow_stretch: 'True'
        	keep_ratio: 'False'

<Prompt1Screen>
    GridLayout:
    	id: prompt_one
    	size_hint: .9, .9
    	pos_hint: {'center_x': .5, 'center_y': .5}
        rows:3
        Label:
        	text: 'Question #1'
        	font_size: 45
        	color: (1, 1, 1, 1)
        	valign: 'middle'
        Label:
        	text: 'What kind of restaurant would you open on Franklin Street?'
        	font_size: 30
        	color: (0.89, 0.167, 0.117, 1)
        	#valign: 'middle'
        	halign: 'center'

<VideoScreen>
	GridLayout:
		id: video
		size_hint: .9, .9
		pos_hint: {'center_x': .5, 'center_y': .5}
		rows: 2
		Label:
			text: 'RECORDING'
			font_size: 45
			color: (1, 1, 1, 1)
		Button:
			text: 'Stop Now!'
			font_size: 30
			color: (0.89, 0.167, 0.117, 1)
			on_press: root.stop()
""")

# Global video title
videoTopic = ""


# Declare both screens
class IntroScreen(Screen):
    pass

class Prompt1Screen(Screen):
	global videoTopic
	videoTopic = 'restaurant'
	counter = Label(text='5', font_size=50)
	def addChild(self):
		print 'Adding child'
		self.add_widget(self.counter)
		Clock.schedule_interval(self.decreaseCounter, 1)
	def decreaseCounter(self, dt):
		if (int(self.counter.text) > 0):
			self.counter.text = str(int(self.counter.text)-1)
		else:
			# Call video function
			Clock.unschedule(self.decreaseCounter)
			# Switch screen
			sm.current = 'video'

class VideoScreen(Screen):
	def start(self):
		videoThread = Thread(target=clipCapture, args=(videoTopic, self.stop, ))
		videoThread.start()

	def stop(self):
		print "Force stop from user input"
		externalKill()

		print "Output file: " + vCapture.getVideoTitle()

		aCapture.saveToDisk();
		saveFilmToDisk(vCapture.getBufferName(), vCapture.getVideoTitle())	

		os.system("ffmpeg -i " + vCapture.getBufferName() + " -i " + aCapture.getAudioTitle() + " -c:v copy -c:a copy awesomeMix.avi" + "\n")

		global objs

		objs = [vCapture, aCapture]


# Create the screen manager
sm = ScreenManager()
sm.add_widget(IntroScreen(name='intro'))
sm.add_widget(Prompt1Screen(name='prompt1'))
sm.add_widget(VideoScreen(name='video'))

Prompt1Screen.on_enter = Prompt1Screen.addChild
VideoScreen.on_enter = VideoScreen.start

class VideoBoothApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    VideoBoothApp().run()