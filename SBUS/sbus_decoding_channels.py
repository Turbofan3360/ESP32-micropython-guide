from machine import UART
import time

class SbusReceive:
    
    TIMEOUT_PERIODS = 26
    
    def __init__(self, port):
        self.sbus = UART(port, 100000)
        self.sbus.init(100000, bits=8, parity=0, stop=2, invert=self.sbus.INV_RX)
        
        self.data = bytearray(23)
        self.previousData = bytearray(23)
        self.dataDuplicate = False
        self.channels = 16*[0]
            
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
                
                if self.data == self.previousData:
                    self.dataDuplicate = True
                else:
                    self.dataDuplicate = False
                    self.previousData = self.data
                
                return self.data
        return None

    def extract_channel_data(self):
        if self.dataDuplicate:
            return "Duplicate"
        
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
        return channels


sbus = SbusReceive(1)

while True:
    data = sbus.read_data()
    
    if data == None:
        time.sleep_ms(100)
    else:
        channels = sbus.extract_channel_data()
        print(channels)
