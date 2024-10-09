from machine import UART
import time

class GPSReceive:
    def __init__(self, tx_pin, rx_pin):
        self.gps = UART(2, baudrate=9600, tx=tx_pin, rx=rx_pin)
        
        self.data = {}
        self.NUM_NMEA_SENTENCES = 6
        
    def get_data(self):        
        # Reads up until a newline character, ensuring when I try to read lines later it starts reading at the start of a line - not in the middle of one
        self.gps.readline()
        num_sentences_read = 0
        
        while num_sentences_read < self.NUM_NMEA_SENTENCES:
            new_data = self.gps.readline()
            
            if new_data:
                while not b'\n' in new_data:
                    missed_bytes = self.gps.read(1)
                    if missed_bytes:
                        new_data += missed_bytes
                
                try:
                    new_data = new_data.decode('utf-8')
                    self.data[new_data[3:6]] = new_data
                    num_sentences_read += 1
                except:
                    return "DECODING ERROR"
        
        return self.data

gps = GPSReceive(10, 9)
while True:
    print(gps.get_data())
    time.sleep(1)
