from machine import UART, PWM, Pin
import time

aileron_pin = 45
elavator_pin = 13
rudder_pin = 14
sbus_pin = 3

class SbusReceive:
    def __init__(self, pin):
        self.sbus = UART(1, 100000, rx=pin)
        self.sbus.init(100000, bits=8, parity=0, stop=2, invert=self.sbus.INV_RX)
        
        self.previousData = bytearray()
        self.dataDuplicated = False
        self.TIMEOUT_PERIODS = 26
        
    def get_sync(self):
        timeout_flag = 0
        
        while timeout_flag < self.TIMEOUT_PERIODS:
            timeout_flag += 1
            testbytes = self.sbus.read(2)
            
            if testbytes == b'\x00\x0f':
                return True
        return False
            
    def read_data(self):
            self.data = bytearray()
            testbytes = self.sbus.read(2)
            
            if testbytes != b'\x00\x0f':
                timeout = self.get_sync()
                if not timeout:
                    return None
            
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
        self.channels_percentages = [2, 4, 5, 6, 7]
        
    def find_duty_cycle(self, angle):
        duty_length = (angle/90)+1.5
        duty_cycle = duty_length*51.2
        return int(duty_cycle)
    
    def get_control_values(self, channel_values):
        aileron_degrees = (channel_values[0]-1000)*(9/1600)
        elavator_degrees = (channel_values[1]-1000)*(9/1600)
        rudder_degrees = (channel_values[3]-1000)*(9/160)
        
        throttle_percent = round((channel_values[2]-200)/16, 2)
        return aileron_degrees, elavator_degrees, rudder_degrees, throttle_percent
    
    def get_switch_values(self, channel_values):
        ch5 = (channel_values[4]-200)/16
        ch7 = (channel_values[6] -200)/16
        return ch5, ch7
    
    def get_aux_values(self, channel_values):
        aux1 = (channel_values[5]-200)/16
        aux2 = (channel_values[7]-200)/16
        return aux1, aux2
    
    def get_duty_cycles(self, channel_values):
        channels = 8*[0]
        
        for i in self.channels_angles:
            servo_angle = (channel_values[i]-1000)*(9/160)
            channels[i] = self.find_duty_cycle(servo_angle)
        
        for i in self.channels_percentages:
            channels[i] = (channel_values[i]-200)/16
        
        return channels


sbus = SbusReceive(sbus_pin)
channelvalues = ChannelValues()

aileron = PWM(Pin(aileron_pin), freq=50, duty_ns=1500)
elavator = PWM(Pin(elavator_pin), freq=50, duty_ns=1500)
rudder = PWM(Pin(rudder_pin), freq=50, duty_ns=1500)

while True:
    data = sbus.read_data()
    
    if data:
        channels = sbus.extract_channel_data()
        if channels:
            servo_throttle_angles = channelvalues.get_duty_cycles(channels)
            
            aileron.duty(servo_throttle_angles[0])
            elavator.duty(servo_throttle_angles[1])
            rudder.duty(servo_throttle_angles[3])
             
    else:
        time.sleep_ms(5)
             
    else:
        time.sleep_ms(5)
