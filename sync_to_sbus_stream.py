from machine import UART

class sbus_receive:
    def __init__(self, port):
        self.sbus = UART(port, 100000)
        self.sbus.init(100000, bits=8, parity=0, stop=2, invert=self.sbus.INV_RX)
        
        self.data = bytearray(23)
        self.testBytes = bytearray(2)
        self.timeout_flag = 0
        
    def read_data(self):
        while self.timeout_flag < 26:
            self.timeout_flag += 1
            print("Searching...")
            self.testBytes = self.sbus.read(2)
            
            if self.testBytes == b'\x00\x0f':
                print("Found stop and start byte...")
                
                while self.sbus.any() < 23:
                    pass
                
                self.data = self.sbus.read(23)
                return self.data
        
        return None

sbus = sbus_receive(1)
data = sbus.read_data()
if data != None:
    print(data)
else:
    print("No data")
