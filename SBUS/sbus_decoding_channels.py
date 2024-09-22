from machine import UART
import time

class SbusReceive:
    
    TIMEOUT_PERIODS = 26
    
    def __init__(self, port):
        self.sbus = UART(port, 100000)
        self.sbus.init(100000, bits=8, parity=0, stop=2, invert=self.sbus.INV_RX)
        
        self.previousData = bytearray()
        self.dataDuplicated = False
        self.channels = 16*[0]
            
    def read_data(self):
        timeout_flag = 0
        
        while timeout_flag < SbusReceive.TIMEOUT_PERIODS:
            timeout_flag += 1
            testbytes = self.sbus.read(2)
            
            if testbytes == b'\x00\x0f':
                self.data = bytearray()
                
                while len(self.data) < 23:
                    nextbytes = self.sbus.read(23 - len(self.data))
                    if nextbytes:
                        self.data += nextbytes
                
                if self.data == self.previousData:
                    self.dataDuplicated = True
                else:
                    self.dataDuplicated = False
                    self.previousData = self.data
                
                return self.data
        return None

    def extract_channel_data(self):
        if self.dataDuplicated:
            return
        
        channels = 16*[0]
        byte_in_sbus = 0
        bit_in_sbus = 0
        ch = 0
        bit_in_channel = 0
        
        for i in range(0, 175):
            if self.data[byte_in_sbus] & (1 << bit_in_sbus):
                channels[ch] |= (1 << bit_in_channel)            
            
            bit_in_sbus += 1
            bit_in_channel += 1
            
            if bit_in_sbus == 8:
                bit_in_sbus = 0
                byte_in_sbus += 1
                
            if bit_in_channel == 11:
                bit_in_channel = 0
                ch += 1
            
        self.channels = channels
        return channels[:8]


sbus = SbusReceive(1)

while True:
    data = sbus.read_data()
    
    if data:
        channels = sbus.extract_channel_data()
        if channels:
            print(channels)
    else:
        time.sleep_ms(5)
