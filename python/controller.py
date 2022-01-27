import serial
import serial.tools.list_ports
import time
import math
import re
from enum import Enum

class command(Enum):
  UNSET = 0,
  PLAINTEXT = 1,
  CIPHERTEXT = 2,
  KEY = 3,
  DECODE = 4,
  ENCODE = 5,
  EXIT= 6,


commandChars = {
  command.UNSET : 'U',
  command.PLAINTEXT : 'P',
  command.CIPHERTEXT : 'C',
  command.KEY : 'K',
  command.EXIT : 'X',
}

def errorAndExit(err):
  print("FATAL ERROR: "+str(err))
  exit()

def getCommandInput():
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

def connectToArduino():
  ser = serial.Serial()
  ser.baudrate = 9600
  ser.timeout=1

  for port in serial.tools.list_ports.comports():
    if(port.manufacturer == "Arduino (www.arduino.cc)"):
      ser.port = port.device

  if(ser.port == None):
    errorAndExit("Arduino not found, is it connected?")

  try:
    ser.open()
    time.sleep(2)
  except Exception as err:
    if(err.args[0] == 16):
      errorAndExit("Cannot initialize serial connection to Arduino, is something else connected to "+ser.port+" ?")
    errorAndExit(err)
  return ser


def isInputHexString(input):
  if(re.fullmatch('([a-fA-F0-9][a-fA-F0-9])*', input) == None):
    return False
  return True


def hexStringToSerialEncode(message, startChar):
  messageBlocks = []

  for i in range(math.ceil(len(message)/32)):
    if(i*32+32 > len(message)):
      messageBlocks.append((startChar+(message[i*32:len(message)]+"0"*(32-(len(message)%32))+"\n").lower()).encode('utf-8'))
    else:
      messageBlocks.append((startChar+(message[i*32:i*32+32]+"\n").lower()).encode('utf-8'))
  return messageBlocks

def stringToHexString(message):
  hexString = ""
  for character in message:
    hexString += hex(ord(character))[2:]
  return hexString

def hexStringToString(message):
  string = ""

  for i in range(0, len(message)-1, 2):
    string+=chr(int(message[i:i+2],16))
  return string

def stringToSerialEncode(message, startChar):
  messageBlocks = []

  for i in range(math.ceil(len(message)/16)):
    messageBlock = startChar
    for j in range(16):
      if (i*16+j < len(message)):
        messageBlock+=hex(ord(message[i*16+j]))[2:]
      else:
        messageBlock+="00"
    messageBlocks.append((messageBlock+"\n").encode('utf-8'))
  return messageBlocks


def encodeInput(input, startChar):
  if(isInputHexString(input)):
    return hexStringToSerialEncode(input, startChar)
  return stringToSerialEncode(input, startChar)


def serialEncodeToString(messageBlocks):
  message = ""
  for block in messageBlocks:
    for i in range(1, len(block)-1, 2):
      if(int(block[i:i+2], 16) != 0x00):
        message+=chr(int(block[i:i+2],16))
    
  return repr(message)

def serialEncodeToHexString(messageBlocks):
  message = ""
  for block in messageBlocks:
    for i in range(1, len(block)-1):

      message+=chr(block[i])
    
  return repr(message)

def sendPlaintext():
  sendBlocks = encodeInput(input(), "P")
  receiveBlocks = []
  for block in sendBlocks:
    ser.write(block)
    receiveBlocks.append(ser.readline())

  print(serialEncodeToHexString(receiveBlocks))


def sendCiphertext():
  sendBlocks = encodeInput(input(), "C")
  receiveBlocks = []
  for block in sendBlocks:
    ser.write(block)
    receiveBlocks.append(ser.readline())

  print(serialEncodeToString(receiveBlocks))

def sendKey():
  sendBlocks = encodeInput(input(), "K")
  receiveBlocks = []
  for block in sendBlocks:
    ser.write(block)
    receiveBlocks.append(ser.readline())

  print(serialEncodeToHexString(receiveBlocks))

ser = connectToArduino()
currentCommand = getCommandInput()

while(currentCommand != command.EXIT):
  if (currentCommand == command.PLAINTEXT):
    sendPlaintext()
  elif (currentCommand == command.CIPHERTEXT):
    sendCiphertext()
  elif (currentCommand == command.KEY):
    encodeInput(input(), "P")
  elif (currentCommand == command.ENCODE):
    print(stringToHexString(input()))
  elif (currentCommand == command.DECODE):
    print(hexStringToString(input()))
  

  currentCommand = getCommandInput()