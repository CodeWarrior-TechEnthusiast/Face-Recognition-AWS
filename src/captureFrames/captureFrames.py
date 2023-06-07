import time
import sys
import signal
import piVideoStream
import numpy as np
import logging
import persistance
import datetime as dt
from pathlib import Path
from multiprocessing import Process
import subscribeMQ
import os

# Creating logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
file = logging.FileHandler("app.log")
fileformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", '%m/%d/%Y %I:%M:%S %p')
file.setLevel(logging.INFO)
file.setFormatter(fileformat)

stream_handler = logging.StreamHandler()
streamformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", '%m/%d/%Y %I:%M:%S %p')
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(streamformat)

log.addHandler(file)
log.addHandler(stream_handler)

def main():
    MQ_BROKER_ID = os.environ.get("MQ_BROKER_ID")
    MQ_USERNAME = os.environ.get("MQ_USERNAME")
    MQ_PASSWORD = os.environ.get("MQ_PASSWORD")
    MQ_REGION = os.environ.get("MQ_REGION")
    MQ_NAME = os.environ.get("MQ_NAME")
    MessageQueue = subscribeMQ.MQ(MQ_BROKER_ID, MQ_USERNAME, MQ_PASSWORD, MQ_REGION) 
    MessageQueueProcess = Process(target=MessageQueue.consume_messages, args=(MQ_NAME,))
    log.info("Subscribed MessageQueue...")
    MessageQueueProcess.start()
    log.info("Initializing Pi Video Stream with Res(160*160) and framerate(32)")
    stream = piVideoStream.PiVideoStream(resolution=(160, 160), framerate=32)
    log.info("Starting Video Stream")
    stream = stream.start()
    log.info("Recording started now!...")
    sent_count = 0
    def signal_handler(sig, frame):
        log.info("Stopping Video Stream")
        stream.stop()
        log.info("Stopped Video Stream")
        log.info("Closing Message Queue Connection")
        MessageQueueProcess.terminate()
        MessageQueueProcess.join()
        log.info("Closed Message Queue Connection")
        log.info("Recording saved at {}".format(stream.filename))
        video_filename = Path(stream.filename).name
        persistance.upload_video_to_s3(stream.filename, video_filename)
        log.info("Uploaded {} video file to S3 Bucket".format(video_filename))
        print("Total Messages Sent: {}".format(sent_count))
        print("Total Messages Received: {}".format(subscribeMQ.received_count.value))
        print("Average Latency: {}".format(subscribeMQ.total_latency.value/subscribeMQ.received_count.value))
        log.info("==================BYE!==================")
        sys.exit(1)
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        frame = stream.read()
        if frame is not None:
            image = persistance.process_image_data(np.array(frame))
            image_name = dt.datetime.now().strftime('image_%Y-%m-%d_%H.%M.%S.png')
            persistance.upload_resource_to_s3(persistance.FRAME_BUCKET, image_name, image)
            log.info("Persisted frame: {}".format(image_name))
            subscribeMQ.timestamp_queue.put(dt.datetime.now())
            sent_count += 1
        time.sleep(0.5)

if __name__ == "__main__":
    main()
