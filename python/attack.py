import arduinoTarget
import whispererHost
import communication
import analysis
import basicAnalyse
import numpy

def cumulative(arduino, cw):
  print(communication.blockToIntList(arduino.key))

  traceCount = 150 + 1
  analyser = analysis.Analysis(communication.blockToIntList(arduino.key))
  #analyser.load("data/equation")
  
  for i in range(1,traceCount):
    (plaintext, _, trace) = cw.attackTarget()
    analyser.addTrace(numpy.array(trace), communication.blockToIntList(plaintext))
    if(i%10==0):
      print(str(i)+" traces")
    bestguess, _ = analyser.calc()

  print(bestguess)
  #analyser.save("data/equation")
  analyser.generatePGEGraph()


def single(arduino, cw):
  print(communication.blockToIntList(arduino.key))
  traceArray = []
  plaintextArray = []

  traceCount = 200 + 1

  for i in range(1,traceCount):
    (plaintext, _, trace) = cw.attackTarget()
    plaintextArray.append(communication.blockToIntList(plaintext))
    traceArray.append(trace)

  bestguess, pge = basicAnalyse.analyseResults(numpy.array(traceArray),plaintextArray,communication.blockToIntList(arduino.key))
  print(bestguess)
  print(pge)


if __name__ ==  "__main__":
  
  arduino = arduinoTarget.ArduinoTarget()

  cw = whispererHost.whispererHost(arduino)

  single(arduino, cw)