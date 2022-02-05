import time
import serial
import serial.tools.list_ports
from common import errorAndExit
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
      errorAndExit("Arduino not found, is it connected?")
    
    try:
      self.serial.open()
      time.sleep(2)
    except Exception as err:
      if(err.args[0] == 16):
        errorAndExit("Cannot initialize serial connection to Arduino, is something else connected to "+self.serial.port+" ?")
      errorAndExit(err)
    
    self.setKey("abcdefghijklmnop")

  def setKey(self, key):
    blocks = communication.encodeInput(key, "K")
    if(len(blocks) != 1):
      errorAndExit("Key not equal to 128 bits")
    ret = self.sendBlock(blocks[0])
    if(blocks[0] != ret):
      errorAndExit("Key returned by Arduino not equal to set key")
    self.key = ret
    return ret

  def sendBlock(self, block):
    self.serial.write(block)
    return self.serial.readline()

if __name__ ==  "__main__":
  arduino = ArduinoTarget()
  print(arduino.key)