"""
Run this script to capture positive images for training the face recognizer.
"""
import glob
import os
import sys
import select
import cv2
import RPi.GPIO as GPIO

#import hardware
import config
import face
from picam import camera
from button import button

# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'positive_'

def check_keyboard_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False
        

if __name__ == '__main__':

	try:
		# Initialize Button
		b = button()
		
		# Load Camera
		cam = camera(rotation=180)

		# Create the directory for positive training images if it doesn't exist.
		if not os.path.exists(config.POSITIVE_DIR):
			os.makedirs(config.POSITIVE_DIR)

		# Find the largest ID of existing positive images.
		# Start new images after this ID value.
		files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR, 
		POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
		count = 0
		if len(files) > 0:
			# Grab the count from the last filename.
			count = int(files[-1][-7:-4])+1
	#		print count

		# Capture Images
		print 'Capturing positive training images.'
		print 'Press button or type c (and press enter) to capture an image. Press Ctrl-C to quit.'
		while True:
			if b.is_pressed() or check_keyboard_input('c'):
				print 'Capturing image...'
				image = cam.take_picture()

				# Convert image to grayscale.
				image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

				# Get coordinates of single face in captured image.
				result = face.detect_single(image)
				if result is None:
					print 'Could not detect single face!  Check the image in capture.pgm to see what was captured and try again with only one face visible.'
					print 'Press button or type c (and press enter) to capture an image.'
				else:
					x, y, w, h = result
					# Crop image as close as possible to desired face aspect ratio.
					# Might be smaller if face is near edge of image.
					crop = face.crop(image, x, y, w, h)

					# Save image to file.
					filename = os.path.join(config.POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
					cv2.imwrite(filename, crop)

					print 'Found face and wrote training image', filename

				count+=1
	except KeyboardInterrupt:
		GPIO.close()
		
