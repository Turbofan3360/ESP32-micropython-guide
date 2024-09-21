from machine import UART
import time

class SbusReceive:
    
    TIMEOUT_PERIODS = 26
    
    def __init__(self, port):
        self.sbus = UART(port, 100000)
        self.sbus.init(100000, bits=8, parity=0, stop=2, invert=self.sbus.INV_RX)
        
        self.data = bytearray(23)
            
    def read_data(self):
        timeout_flag = 0
        
        while timeout_flag < SbusReceive.TIMEOUT_PERIODS:
            timeout_flag += 1
            testbytes = self.sbus.read(2)
            
            if testbytes == b'\x00\x0f':
                time.sleep_ms(50)
                if self.sbus.any() < 23:
                    pass
                
                self.data = self.sbus.read(23)
                return self.data
        return None


sbus = SbusReceive(1)

while True:
    data = sbus.read_data()
    
    if data == None:
        print("No data")
    else:
        print(data)
