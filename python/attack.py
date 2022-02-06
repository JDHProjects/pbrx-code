import arduinoTarget
import whispererHost
import communication
import analyse
import numpy

if __name__ ==  "__main__":
  arduino = arduinoTarget.ArduinoTarget()
  cw = whispererHost.whispererHost(arduino)
  print(communication.blockToIntList(arduino.key))
  traceArray = []
  plaintextArray = []
  for i in range(0,100):
    (plaintext, _, trace) = cw.attackTarget()
    plaintextArray.append(communication.blockToIntList(plaintext))
    traceArray.append(trace)
  analyse.analyseResults(numpy.array(traceArray),plaintextArray)