
import RPi.GPIO as GPIO
import time

import config

class button(object):
	
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(config.BUTTON_PIN, GPIO.IN)
		
		# Set initial box state.
		self.button_state = GPIO.input(config.BUTTON_PIN)

	def is_pressed(self):
		''' Returns True when button is pressed '''
		old_state = self.button_state
		self.button_state = GPIO.input(config.BUTTON_PIN)
		# Check if transition from down to up
		if old_state == config.BUTTON_DOWN and self.button_state == config.BUTTON_UP:
			# Wait 20 milliseconds and measure again to debounce switch.
			time.sleep(20.0/1000.0)
			self.button_state = GPIO.input(config.BUTTON_PIN)
			if self.button_state == config.BUTTON_UP:
				return True
		return False
		
		
if __name__=='__main__':
	
	try:
		b=button()
		while True:
			if b.is_pressed():
				print 'Button Pressed'

	except KeyboardInterrupt:
		GPIO.cleanup()
	
	
