import serial
# from enum import Enum
#
# class LASER_CHANNEL( Enum ):
#     POWER_01 = '0'
#     POWER_02 = '1'
#     POWER_03 = '2'
#     POWER_04 = '3'
#     CURRENT_01 ='A'
#     CURRENT_02 ='B'


class PiPico:
    def __init__(self,port,baudrate=76800,timeout=1):

        try:
            self.inst = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            self.inst.isOpen()  # try to open port, if possible print message and proceed with 'while True:'
            print("port is opened!")

        except IOError:  # if port is already opened, close it and open it again and print message
            self.inst.close()
            self.inst.open()
            print("port was already open, was closed and opened again!")

        
    def close(self):
        # close device
        if( self.inst is not None ):
            self.inst.close()
            self.inst = None

        return True
        
    def read(self,channel):
        
        try:
            variable = channel.value
        except:
            variable = channel
        try:
            self.inst.write(str.encode("0%c00000\r"%str (variable)) )
            self.line = self.inst.read(6)
        
        except:
            print ("read Error closing Serialport. CH",variable)
            self.close()
            return 0
            
        return self.line
        
    def write(self,channel, value):
        
        #Variable = Char to Select Variable
        #Value = Int to send 0-4095
        # 0-4 Laserchannel
        # A-B Lasercurrent
        try:
            variable = channel.value 
        except:
            variable = channel
        if(value>=65535):
            value=65535
        try:
            self.inst.write(str.encode("1%c%05d\r"%(str (variable), value)))
            self.line = self.inst.read(2)
        except Exception as e:
            print( e )
            print ("write Error closing Serialport. CH",variable)
            self.close()
            return 0
            
        return self.line
    
    def read_ADC(self,channel):
        
        
        if (channel == 0):
            variable = self.read("a")
        elif (channel == '0'):
            variable = self.read("a")
        elif (channel == 1):
            variable = self.read("b")
        elif (channel == '1'):
            variable = self.read("b")
        else:
            print ("read ADC Error wrong channel selected. CH",channel)
            return 0
            
        return variable
    
    def write_PWM(self,channel, value):
        
        
        if (channel == 0):
            variable = self.write("c",value)
        elif (channel == '0'):
            variable = self.write("c",value)
        elif (channel == 1):
            variable = self.write("d",value)
        elif (channel == '1'):
            variable = self.write("d",value)
        else:
            print ("write PWM Error wrong channel selected. CH",channel)
            return 0
            
        return variable
    
    def read_PWM(self,channel):
        
        
        if (channel == 0):
            variable = self.read("c")
        elif (channel == '0'):
            variable = self.read("c")
        elif (channel == 1):
            variable = self.read("d")
        elif (channel == '1'):
            variable = self.read("d")
        else:
            print ("read PWM Error wrong channel selected. CH",channel)
            return 0
            
        return variable
    
    def set_Pin(self,channel):
        
        
        if (channel == 0):
            variable = self.write("e",1)
        elif (channel == '0'):
            variable = self.write("e",1)
        elif (channel == 1):
            variable = self.write("f",1)
        elif (channel == '1'):
            variable = self.write("f",1)
        else:
            print ("set Pin Error wrong channel selected. CH",channel)
            return 0
            
        return variable
    
    def clear_Pin(self,channel):
        
        if (channel == 0):
            variable = self.write("e",0)
        elif (channel == '0'):
            variable = self.write("e",0)
        elif (channel == 1):
            variable = self.write("f",0)
        elif (channel == '1'):
            variable = self.write("f",0)
        else:
            print ("clear Pin Error wrong channel selected. CH",channel)
            return 0
            
        return True
    
    
    def read_Pin(self,channel):
        
        
        if (channel == 0):
            variable = self.read("e")
        elif (channel == '0'):
            variable = self.read("e")
        elif (channel == 1):
            variable = self.read("f")
        elif (channel == '1'):
            variable = self.read("f")
        else:
            print ("read Pin Error wrong channel selected. CH",channel)
            return 0
            
        return variable

    def __del__(self):
        self.inst.close()

