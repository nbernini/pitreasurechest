"""Raspberry Pi Face Recognition Treasure Box
Treasure Box Script
Copyright 2013 Tony DiCola 
"""
import cv2

import config
import face
#import hardware
from picam import camera
import select
import sys

def check_keyboard_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False

if __name__ == '__main__':
        # Load training data into model
        print 'Loading training data...'
        model = cv2.createEigenFaceRecognizer()
        model.load(config.TRAINING_FILE)
        print 'Training data loaded!'

        # Initialize camera
        cam = camera(rotation=180)

        try:
                print 'Press c (then enter) to take picture.  Press Ctrl-C to quit.'
                while True:
                        if check_keyboard_input('c'):
                        #if True:
                                # Take Picture
                                print 'Capturing image...'
                                image = cam.take_picture()

                                # Convert image to grayscale.
                                print 'Processing image...'
                                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                                # Get coordinates of single face in captured image.
                                result = face.detect_single(image)
                                if result is None:
                                        print 'Could not detect single face!  Check the image in capture.pgm to see what was captured and try again with only one face visible.'
                                else:
                                        print 'Resizing Image ....'
                                        x, y, w, h = result
                                        # Crop and resize image
                                        crop = face.resize(face.crop(image, x, y, w, h))
                                        
                                        # Predict Face
                                        label, confidence = model.predict(crop)
                                        print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
                                                'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
                                                confidence)
                                        if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
                                                print 'Recognized face!'
                                                #box.unlock()
                                        else:
                                                print 'Did not recognize face!'

                                        print '\nPress c (then enter) to take picture.  Press Ctrl-C to quit.'
                                
        except KeyboardInterrupt:
                cam.camera.close()
