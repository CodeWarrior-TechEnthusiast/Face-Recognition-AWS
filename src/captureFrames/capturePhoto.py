from picamera import PiCamera
from PIL import Image
import datetime as dt
import os
import numpy as np
import time

cam = PiCamera()
cam.resolution = (160,160)
cam.rotation = -180
cam.start_preview()
os.makedirs("./images", exist_ok=True)
output = np.empty((160, 160, 3), dtype=np.uint8)

time.sleep(5)

try:
    for i in range(500):
        cam.capture(output, 'rgb')
        im = Image.fromarray(output)
        im.save(os.path.join("images", dt.datetime.now().strftime('image_%Y-%m-%d_%H.%M.%S.png')))
        print(f"Saved image: {i}")
    cam.stop_preview()
    cam.close()
except Exception as ex:
    print(ex)
