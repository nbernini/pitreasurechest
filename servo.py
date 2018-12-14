# https://rpi.science.uoit.cal/lab/servo

 
import RPi.GPIO as GPIO
import time

import config

class box_lock(object):
	
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(config.LOCK_SERVO_PIN, GPIO.OUT)
		self.pwm = GPIO.PWM(config.LOCK_SERVO_PIN, config.LOCK_FREQ)
		self.pwm.start(config.LOCK_0)	

	def update(self,pulse):
		''' Move Servo based on pulse '''
		self.pwm.ChangeDutyCycle(pulse)
		
	def destroy(self):
		self.pwm.stop()
		GPIO.cleanup()

if __name__=='__main__':
	
	try:
		l = box_lock()

		wait_time=.15
		
		vals=[config.LOCK_0,config.LOCK_90,config.LOCK_180]
		rev_vals=[config.LOCK_180,config.LOCK_90,config.LOCK_0]
		while True:
			for v in vals:
				l.update(v)
				time.sleep(wait_time)
			
			for r in rev_vals:
				l.update(r)
				time.sleep(wait_time)

#			val = raw_input('Enter Pulse between X and Y')
#			try:
#				val = float(val)
#			except ValueError:
#				print 'Invalid number between X and Y'
				
#			l.update(val)
		
	except KeyboardInterrupt:
		l.destroy()
		
