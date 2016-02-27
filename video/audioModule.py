import pyaudio
import wave
import time
import string

class AudioModule:
	chunk = 1024
	format = pyaudio.paInt16
	channels = 2
	rate = 44100

	audioTitle = time.strftime("%Y_%m_%d_%H_%M_%S")

	p = pyaudio.PyAudio()

	continueRecord = True

	frames = []

	def getAudioTitle(self):
		return self.audioTitle

	def recordAudio(self, cb, length=5):
		stream = self.p.open(format = self.format,
			channels = self.channels,
			rate = self.rate,
			input = True,
			frames_per_buffer=self.chunk)

		frames = []

		gen = (i for i in range(0, int(self.rate / self.chunk * length)) if self.continueRecord)

		for i in gen:
			data = stream.read(self.chunk)
			frames.append(data)

		self.frames = frames

		stream.stop_stream()
		stream.close()
		self.p.terminate()
		print "PyAudio terminated"
		print self.p
		print "Audio module terminated"
		cb()


	def endCapture(self):
		self.continueRecord = False

	def saveToDisk(self, title):
		print "SAVING AUDIO FILE AS:::", self.getAudioTitle()
		print "TITLE IS::: ", self.topic
		wf = wave.open(title + "_" + self.audioTitle, 'wb')
		wf.setnchannels(self.channels)
		wf.setsampwidth(self.p.get_sample_size(self.format))
		wf.setframerate(self.rate)
		wf.writeframes(b''.join(self.frames)) 
		wf.close()
		

	def __init__(self, appendTitle):
		print "AUDIO TITLE::: ", appendTitle
		self.audioTitle += ".wav"
		self.topic = str(appendTitle)