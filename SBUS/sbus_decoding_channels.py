from machine import UART
import time

class SbusReceive:
    
    TIMEOUT_PERIODS = 26
    
    def __init__(self, port):
        self.sbus = UART(port, 100000)
        self.sbus.init(100000, bits=8, parity=0, stop=2, invert=self.sbus.INV_RX)
        
        self.previousData = bytearray()
        self.dataDuplicated = False
            
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
            
        return channels

class ChannelValues:
    def __init__(self):
        self.channels_angles = [0, 1, 3]
        self.channels_percent = [2, 4, 5, 6, 7]
    
    def get_control_values(self, channel_values):
        aileron_degrees = round((channel_values[0]-1000)*(9/80), 2)
        elavator_degrees = round((channel_values[1]-1000)*(9/80), 2)
        rudder_degrees = round((channel_values[3]-1000)*(9/80), 2)
        
        throttle_% = round((channel_values[2]-200)/16, 2)
        return aileron_degrees, elavator_degrees, rudder_degrees, throttle_%
    
    def get_switch_values(self, channel_values):
        ch5 = (channel_values[4]-200)/16
        ch7 = (channel_values[6] -200)/16
        return ch5, ch7
    
    def get_aux_values(self, channel_values):
        aux1 = round((channel_values[5]-200)/16, 2)
        aux2 = round((channel_values[7]-200)/16, 2)
        return aux1, aux2
    
    def get_values(self, channel_values):
        channels = 8*[0]
        
        for i in self.channels_angles:
            channels[i] = round((channel_values[i]-1000)*(9/80), 2)
        
        for i in self.channels_percent:
            channels[i] = round((channel_values[i]-200)/16, 2)
        
        return channels


sbus = SbusReceive(1)

while True:
    data = sbus.read_data()
    
    if data:
        channels = sbus.extract_channel_data()
        if channels:
            print(channels)
    else:
        time.sleep_ms(5)
