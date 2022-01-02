import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(22, GPIO.OUT)
while True:
	GPIO.output(22, GPIO.HIGH)
	time.sleep(10)
	GPIO.output(22, GPIO.LOW)
