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
  analysis = analyse.Analysis(communication.blockToIntList(arduino.key))
  for i in range(0,150):
    (plaintext, _, trace) = cw.attackTarget()
    plaintextArray.append(communication.blockToIntList(plaintext))
    traceArray.append(trace)
    analysis.addTrace(numpy.array(trace), communication.blockToIntList(plaintext))
  print("second")
  analyse.analyseResults(numpy.array(traceArray),plaintextArray,communication.blockToIntList(arduino.key))