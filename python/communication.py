import re
import math
import random

def hexStringToSerialEncode(message, startChar):
  messageBlocks = []
  
  for i in range(math.ceil(len(message)/32)):
    if(i*32+32 > len(message)):
      messageBlocks.append((startChar+(message[i*32:len(message)]+"0"*(32-(len(message)%32))+"\n").lower()).encode('utf-8'))
    else:
      messageBlocks.append((startChar+(message[i*32:i*32+32]+"\n").lower()).encode('utf-8'))
  return messageBlocks

def stringToSerialEncode(message, startChar):
  messageBlocks = []
  for i in range(math.ceil(len(message)/16)):
    messageBlock = startChar
    for j in range(16):
      if (i*16+j < len(message)):
        messageBlock+=format(ord(message[i*16+j]), '02x')
      else:
        messageBlock+="00"
    messageBlocks.append((messageBlock+"\n").encode('utf-8'))
  return messageBlocks

def isInputHexString(input):
  if(re.fullmatch('([a-fA-F0-9][a-fA-F0-9])*', input) == None):
    return False
  return True

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

def getRandomBlock(startChar):
  blockString = startChar
  for i in range(16):
    blockString+=format(random.randrange(0,256), '02x')
  blockString+="\n"
  return blockString.encode('utf-8')

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

def blockToIntList(block):
  output = []
  for i in range(1, len(block)-1, 2):
    output.append(int(chr(block[i])+chr(block[i+1]),16))
  return output

def intListToString(block):
  output = ""
  for i in range(0, len(block)):
    output+=chr(block[i])
  return repr(output)