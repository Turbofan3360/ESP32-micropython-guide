# ESP32 micropython setup:

**PLEASE NOTE - I USE LINUX UBUNTU OS. THERE MAY BE DIFFERENCES FOR OTHER OPERATING SYSTEMS**

After looking around, I found many old/deprecated IDEs people have used. Eventually, I found that the Thonny IDE is the best option. After trying to flash firmware to the chip, I encountered “Errno 13”, which I found a solution to here: https://github.com/thonny/thonny/issues/2360. I then continued, but came across another issue - error message: A fatal error occurred: Failed to connect to Espressif device: No serial data received. For troubleshooting steps visit: https://docs.espressif.com/projects/esptool/en/latest/troubleshooting.html Erase command returned with error code 2

I realised this was due to my USB cable being plugged into the USB-OTG port rather than the USB-UART (one of my boards had a faulty USB-UART). This solved my problem.

I then encountered issues when trying to flash firmware to the chip - the stub flashers (.JSON files) for the “esptool” package installed via apt repositories were incomplete, not containing the required stub flashers for an ESP-32-S3 model.

After struggling to install esptool via github (https://github.com/espressif/esptool), which contained the required stub flashers, due to install scripts being faulty, I used pip3 to install it - forcing pip to install (despite it wanting me to use apt as is standard in newer Ubuntu versions) via: 
```
pip3 install esptool --break-system-packages
```
This then allowed me to flash micropython firmware via the Thonny IDE to the board. To do this, enter Thonny and go to Tools > Options > Interpreter (if you have esptool downloaded as well, you will need to select the three lines next to the install button > Select local MicroPython Image to choose your downloaded firmware). Download the latest micropython firmware at https://micropython.org/download/?port=esp32 and then flash it to the board. I also installed the Thonny ESP32 plugin for future use.

NOTE: If you want OCTAL SPIRAM/PSRAM support, scroll further down on the download page to find firmwares that support it

To test the installation, you can connect your board via USB-UART, then enter Thonny Options > Interpreter (as seen above in the image with installation of micropython). Select the port, and hit “OK” to connect your board. You should be able to see in the shell that it is connected - type “help()” to confirm this and get an output from your ESP32.

# SG90 Servo:

Firstly I looked up the datasheet for my SG90 servo, found here: http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf This told me everything I needed to know to use PWM (an artificially analogue communication protocol) to control it - in my case, a duty cycle between 1-2ms long (500/1,000Hz) with a period of 50hz

I then also read through the ESP32 Micropython docs section on PWM: https://www.micropython.org/resources/docs/en/latest/library/machine.PWM.html#machine-pwm

This gave me all the knowledge I needed to write code to control my servo. I connected my servo up to an external power supply (not running it off the ESP32’s 5V pins), and connected the servo signal wire to the ESP32 pin 1 (although almost any other pin would work - check your board’s pinout).

This is the code I eventually used to control my servo:

```
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
```

I struggled at the start as my servo wasn’t moving at all. However, upon coming across a wiring diagram online, I tried connecting my servo’s ground to the ESP-32’s ground pin. This solved the problem! I now know the issue was that for a protocol such as PWM, where the voltages of the output pin are key, you need a common ground between the servo and controller to measure those voltages from.

PLEASE NOTE: The function find_duty_cycle() in the above code is the result of what I found on this website: https://www.upesy.com/blogs/tutorials/esp32-servo-motor-sg90-on-micropython I used that code as a guideline to build my own function to find a duty cycle value to output. This find_duty_cycle() function is highly simplified, containing multiple steps in one line. It is applicable to my SG90 servo with a 180° travel range (from +90° to -90°). It may need to be altered to suit other servos.

# Useful Links:

Incredibly useful micropython docs: https://docs.micropython.org/en/latest/esp32/quickref.html

Design guidelines for custom PCBs with ESP32: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/index.html

Custom PCB design review by ESP32 company creator: https://www.espressif.com/en/contact-us/circuit-schematic-pcb-design-review

ESP32 troubleshooting: https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html
