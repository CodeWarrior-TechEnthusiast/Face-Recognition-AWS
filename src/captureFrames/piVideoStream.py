import os
import datetime as dt
from picamera import PiCamera
from picamera.array import PiRGBArray
import threading
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class PiVideoStream:
	def __init__(self, resolution=(320, 240), framerate=32):
		# initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False
		self.filename = None
	
	def __init__(self, resolution=(320, 240), framerate=32, rotate=0):
		# initialize the camera and stream
		self.camera = PiCamera()
		self.camera.rotation = rotate
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False

	def start(self):
                os.makedirs("./recordings/", exist_ok=True)
                self.filename = os.path.join("./recordings/", dt.datetime.now().strftime('recording_%Y-%m-%d_%H.%M.%S.h264'))
                self.camera.start_recording(self.filename)
		# start the thread to read frames from the video stream
                t = threading.Thread(target=self.update, args=())
                t.daemon = True
                t.start()
                return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			self.frame = f.array
			self.rawCapture.truncate(0)

			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
                self.camera.stop_recording()
		# indicate that the thread should be stopped
                self.stopped = True
