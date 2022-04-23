import time
import serial
import serial.tools.list_ports
import communication

class ArduinoTarget():

  def __init__(self):
    self.serial = serial.Serial()
    self.serial.baudrate = 57600
    self.serial.timeout=1

    for port in serial.tools.list_ports.comports():
      if(port.manufacturer == "Arduino (www.arduino.cc)"):
        self.serial.port = port.device

    if(self.serial.port == None):
      print("FATAL ERROR: Arduino not found, is it connected?")
      exit()
    
    try:
      self.serial.open()
      time.sleep(2)
    except Exception as err:
      if(err.args[0] == 16):
        print("FATAL ERROR: Cannot initialize serial connection to Arduino, is something else connected to "+self.serial.port+" ?")
        exit()
      print("FATAL ERROR: "+str(err))
      exit()
    
    self.setKey("abcdefghijklmnop")

  def setKey(self, key):
    blocks = communication.encodeInput(key, "K")
    if(len(blocks) != 1):
      print("FATAL ERROR: Key not equal to 128 bits")
      exit()
    ret = self.sendBlock(blocks[0])
    if(blocks[0] != ret):
      print("FATAL ERROR: Key returned by Arduino not equal to set key")
      exit()
    self.key = ret
    return ret

  def setRandomKey(self):
    block = communication.getRandomBlock("K")
    ret = self.sendBlock(block)
    if(block != ret):
      print("FATAL ERROR: Key returned by Arduino not equal to set key")
      exit()
    self.key = ret
    return ret

  def sendBlock(self, block):
    self.serial.write(block)
    return self.serial.readline()

if __name__ ==  "__main__":
  arduino = ArduinoTarget()
  print(arduino.key)