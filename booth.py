# Ted Video Booth - UI with Kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.event import EventDispatcher

import imp

import sys
sys.path.insert(0, './video/')

# from capture import *
import capture
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

<Prompt2Screen>
    GridLayout:
    	id: prompt_two
    	size_hint: .9, .9
    	pos_hint: {'center_x': .5, 'center_y': .5}
        rows:3
        Label:
        	text: 'Question #2'
        	font_size: 45
        	color: (1, 1, 1, 1)
        	valign: 'middle'
        Label:
        	text: 'What do you regret the most?'
        	font_size: 30
        	color: (0.89, 0.167, 0.117, 1)
        	#valign: 'middle'
        	halign: 'center'

<Prompt3Screen>
    GridLayout:
    	id: prompt_three
    	size_hint: .9, .9
    	pos_hint: {'center_x': .5, 'center_y': .5}
        rows:3
        Label:
        	text: 'Question #3'
        	font_size: 45
        	color: (1, 1, 1, 1)
        	valign: 'middle'
        Label:
        	text: 'What do you look forward to in 2017?'
        	font_size: 30
        	color: (0.89, 0.167, 0.117, 1)
        	#valign: 'middle'
        	halign: 'center'

<Prompt4Screen>
    GridLayout:
    	id: prompt_four
    	size_hint: .9, .9
    	pos_hint: {'center_x': .5, 'center_y': .5}
        rows:3
        Label:
        	text: 'Question #4'
        	font_size: 45
        	color: (1, 1, 1, 1)
        	valign: 'middle'
        Label:
        	text: 'If you could change one thing about UNC, what would it be?'
        	font_size: 30
        	color: (0.89, 0.167, 0.117, 1)
        	#valign: 'middle'
        	halign: 'center'

<Prompt5Screen>
    GridLayout:
    	id: prompt_five
    	size_hint: .9, .9
    	pos_hint: {'center_x': .5, 'center_y': .5}
        rows:3
        Label:
        	text: 'Question #5'
        	font_size: 45
        	color: (1, 1, 1, 1)
        	valign: 'middle'
        Label:
        	text: 'Make the strangest noise you can!'
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

<EndScreen>
    GridLayout:
    	id: intro_layout
        size_hint: .9, .9
        pos_hint: {'center_x': .5, 'center_y': .5}
        rows:4
        Label:
        	text: "... and that's a cut!"
        	font_size: 50
        	color: (0.89, 0.167, 0.117, 1)
		Label:
			text: 'Thanks for participating!'
			font_size: 40
			color: (0.89, 0.167, 0.117, 1)
		Button:
			text: 'Start!'
			font_size: 30
			color: (1, 1, 1, 1)
			on_press: root.manager.current = 'intro'
        Image:
        	source: './res/logo.png'
        	allow_stretch: 'True'
        	keep_ratio: 'False'
""")

# Global video title
videoTopic = ""


# Declare both screens
class IntroScreen(Screen):
    pass

class EndScreen(Screen):
	pass

class Prompt1Screen(Screen):
	counter = Label(text='5', font_size=50)
	def addChild(self):
		global videoTopic
		videoTopic = 'restaurant'
		print 'Adding child'
		self.add_widget(self.counter)
		Clock.schedule_interval(self.decreaseCounter, 1)
	def decreaseCounter(self, dt):
		if (int(self.counter.text) > 0):
			self.counter.text = str(int(self.counter.text)-1)
		else:
			# Call video function
			Clock.unschedule(self.decreaseCounter)
			# Switch screens
			sm.current = 'video'

class Prompt2Screen(Screen):
	counter = Label(text='5', font_size=50, color=(1, 1, 1, 1))
	def addChild(self):
		global videoTopic
		videoTopic = 'regret'
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

class Prompt3Screen(Screen):
	counter = Label(text='5', font_size=50, color=(1, 1, 1, 1))
	def addChild(self):
		global videoTopic
		videoTopic = '2017'
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

class Prompt4Screen(Screen):
	counter = Label(text='5', font_size=50, color=(1, 1, 1, 1))
	def addChild(self):
		global videoTopic
		videoTopic = 'changeUNC'
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

class Prompt5Screen(Screen):
	counter = Label(text='5', font_size=50, color=(1, 1, 1, 1))
	def addChild(self):
		global videoTopic
		videoTopic = 'noise'
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
		imp.reload(capture)
		print "Starting video screen!"
		global videoTopic
		videoThread = Thread(target=capture.clipCapture, args=(videoTopic, self.stop, ))
		videoThread.start()
		videoThread.join()

	def stop(self):
		print "Force stop from user input"
		capture.externalKill()

		print "Moving on to the next prompt!"

		global videoTopic

		if (videoTopic == 'restaurant'):
			sm.current = 'prompt2'
		elif (videoTopic == 'regret'):
			sm.current = 'prompt3'
		elif (videoTopic == '2017'):
			sm.current = 'prompt4'
		elif (videoTopic == 'changeUNC'):
			sm.current = 'prompt5'
		elif (videoTopic == 'noise'):
			sm.current = 'end'

# Create the screen manager
sm = ScreenManager()
sm.add_widget(IntroScreen(name='intro'))
sm.add_widget(Prompt1Screen(name='prompt1'))
sm.add_widget(Prompt2Screen(name='prompt2'))
sm.add_widget(Prompt3Screen(name='prompt3'))
sm.add_widget(Prompt4Screen(name='prompt4'))
sm.add_widget(Prompt5Screen(name='prompt5'))
sm.add_widget(VideoScreen(name='video'))
sm.add_widget(EndScreen(name='end'))

Prompt1Screen.on_enter = Prompt1Screen.addChild
Prompt2Screen.on_enter = Prompt2Screen.addChild
Prompt3Screen.on_enter = Prompt3Screen.addChild
Prompt4Screen.on_enter = Prompt4Screen.addChild
Prompt5Screen.on_enter = Prompt5Screen.addChild
VideoScreen.on_enter = VideoScreen.start

class VideoBoothApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    VideoBoothApp().run()