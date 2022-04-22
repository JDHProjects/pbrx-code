import arduinoTarget
import communication
import whispererHost
from common import errorAndExit

from enum import Enum
class command(Enum):
  UNSET = 0,
  PLAINTEXT = 1,
  CIPHERTEXT = 2,
  KEY = 3,
  DECODE = 4,
  ENCODE = 5,
  EXIT= 6,


class UI():
  def __init__(self, arduino, cw):
    self.cw = cw,
    self.arduino = arduino

  def getCommandInput(self):
    counter = 0 
    while (counter < 10):
      counter+=1
      userInput = input("Please enter your command selection: ")
      if((userInput.upper() == "PLAINTEXT") or (userInput.upper() == "PLAIN") or (userInput.upper() == "P")):
        return command.PLAINTEXT
      elif((userInput.upper() == "CIPHERTEXT") or (userInput.upper() == "CIPHER") or (userInput.upper() == "C")):
        return command.CIPHERTEXT
      elif((userInput.upper() == "KEY") or (userInput.upper() == "K")):
        return command.KEY
      elif((userInput.upper() == "EXIT") or (userInput.upper() == "X")):
        exit()
      elif((userInput.upper() == "ENCODE") or (userInput.upper() == "E")):
        return command.ENCODE
      elif((userInput.upper() == "DECODE") or (userInput.upper() == "D")):
        return command.DECODE
      print("Command not recognised")
    errorAndExit("Invalid input entered 10 times, exiting")
  
  def mainLoop(self):
    currentCommand = self.getCommandInput()

    while(currentCommand != command.EXIT):
      if (currentCommand == command.PLAINTEXT):
        self.sendPlaintext()
      elif (currentCommand == command.CIPHERTEXT):
        self.sendCiphertext()
      elif (currentCommand == command.KEY):
        self.arduino.setKey(input())
        print("Key set to: "+str(self.arduino.key))
      elif (currentCommand == command.ENCODE):
        print(communication.stringToHexString(input()))
      elif (currentCommand == command.DECODE):
        print(communication.hexStringToString(input()))
      currentCommand = self.getCommandInput()

  def sendCiphertext(self):
    sendBlocks = communication.encodeInput(input(), "C")
    receiveBlocks = []
    for block in sendBlocks:
      receiveBlocks.append(self.arduino.sendBlock(block))

    print(communication.serialEncodeToString(receiveBlocks))

  def sendPlaintext(self):
    sendBlocks = communication.encodeInput(input(), "P")
    receiveBlocks = []
    for block in sendBlocks:
      receiveBlocks.append(self.arduino.sendBlock(block))
    print(communication.serialEncodeToHexString(receiveBlocks))

if __name__ ==  "__main__":
  arduino = arduinoTarget.ArduinoTarget()
  cw = whispererHost.WhispererHost(arduino)
  ui = UI(arduino, cw)

  ui.mainLoop()