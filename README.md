# ESP32-micropython-setup-guide

Flashing Micropython firmware to chip:

After looking around, I found many old/deprecated IDEs people have used. Eventually, I found that the Thonny IDE is the best option. After trying to flash firmware to the chip, I encountered “Errno 13”, which I found a solution to here: https://github.com/thonny/thonny/issues/2360. I then continued, but came across another issue - error message: A fatal error occurred: Failed to connect to Espressif device: No serial data received. For troubleshooting steps visit: https://docs.espressif.com/projects/esptool/en/latest/troubleshooting.html Erase command returned with error code 2

I realised this was due to my USB cable being plugged into the USB-OTG port rather than the USB-UART (one of my boards had a faulty USB-UART). This solved my problem.

I then encountered issues when trying to flash firmware to the chip - the stub flashers (.JSON files) for the “esptool” package installed via apt repositories were incomplete, not containing the required stub flashers for an ESP-32-S3 model.

After struggling to install esptool via github (https://github.com/espressif/esptool), which contained the required stub flashers, due to install scripts being faulty, I used pip3 to install it - forcing pip to install (despite it wanting me to use apt as is standard in newer Ubuntu versions) via: pip3 install esptool --break-system-packages

This then allowed me to flash micropython firmware via the Thonny IDE to the board. To do this, enter Thonny and go to Tools > Options > Interpreter (if you have esptool downloaded as well, you will need to select the three lines next to the install button > Select local MicroPython Image to choose your downloaded firmware). Download the latest micropython firmware at https://micropython.org/download/?port=esp32 and then flash it to the board. I also installed the Thonny ESP32 plugin for future use.

NOTE: If you want OCTAL SPIRAM/PSRAM support, scroll further down on the download page to find firmwares that support it

To test the installation, you can connect your board via USB-UART, then enter Thonny Options > Interpreter (as seen above in the image with installation of micropython). Select the port, and hit “OK” to connect your board. You should be able to see in the shell that it is connected - type “help()” to confirm this and get an output from your ESP32.

Useful Links:

Incredibly useful micropython docs: https://docs.micropython.org/en/latest/esp32/quickref.html

Design guidelines for custom PCBs with ESP32: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/index.html

Custom PCB design review by ESP32 company creator: https://www.espressif.com/en/contact-us/circuit-schematic-pcb-design-review

ESP32 troubleshooting: https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html
