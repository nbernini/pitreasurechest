"""
Pi camera device capture class for OpenCV.  This class allows you to capture a
single image from the pi camera as an OpenCV image.
"""
import io
import time

import cv2
import numpy as np
import picamera
from picamera import PiCamera

import config

class camera(object):
        def __init__(self,rotation=0):
                self.camera = PiCamera()
                self.camera.rotation = rotation

        def take_picture(self):
                data = io.BytesIO()
                self.camera.capture(data,format='jpeg')
                data = np.fromstring(data.getvalue(), dtype=np.uint8)

                # Decode the image data and return an OpenCV image.
                image = cv2.imdecode(data, 1)

                # Save captured image for debugging.
                cv2.imwrite(config.DEBUG_IMAGE, image)

                # Return the captured image data.
                return image

class webcamp(object):
        ''' TODO '''
        def __init__(self):
                self.webcam=None
                
if __name__=='__main__':
        c = camera(rotation=180)
        #image = c.take_picture()
        
