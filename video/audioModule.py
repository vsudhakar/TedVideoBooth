import pyaudio
import wave
import time

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
		cb()


	def endCapture(self):
		self.continueRecord = False

	def saveToDisk(self):
		wf = wave.open(self.audioTitle, 'wb')
		wf.setnchannels(self.channels)
		wf.setsampwidth(self.p.get_sample_size(self.format))
		wf.setframerate(self.rate)
		wf.writeframes(b''.join(self.frames)) 
		wf.close()
		

	def __init__(self, appendTitle):
		self.audioTitle += appendTitle + ".wav"