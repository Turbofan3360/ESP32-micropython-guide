from machine import PWM, Pin
import time

def find_duty_cycle(angle):
	duty_length = (angle/90)+1.5
	duty_cycle = round(duty_length*51.2)
	return duty_cycle

servo = PWM(Pin(1), freq=50, duty_ns=1500)
angles = [0, 90, 0, -90]

while True:
	print("Moving...")
	for i in angles:
    		cycle = find_duty_cycle(i)
    		servo.duty(cycle)
    		time.sleep(1)
