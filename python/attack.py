import arduinoTarget
import whispererHost
import communication
import analysis
import visualise
import basicAnalysis
import numpy

def cumulative(arduino, cw):
  print(communication.blockToIntList(arduino.key))

  traceCount = 300
  traceInterval = 10

  #analyser.load("data/testing")

  visualiser = visualise.Visualise(traceInterval, traceCount)

  for i in range(0,1):
    analyser = analysis.Analysis(communication.blockToIntList(arduino.key),2500)
    print("attack: "+str(i))
    for j in range(0,traceCount):
      (plaintext, _, trace) = cw.attackTarget()
      analyser.addTrace(numpy.array(trace[1000:3500]), communication.blockToIntList(plaintext))
      if(j%traceInterval==0):
        bestguess, pge = analyser.calc()
        print(str(j)+" traces: PGE sum = "+str(sum(pge)))

    visualiser.addPGEs(analyser.pges)
    #visualiser.save("data/testing")

  print(bestguess)
  visualiser.generatePGEGraphByIndex(0)
  #analyser.save("data/equation")


def single(arduino, cw):
  print(communication.blockToIntList(arduino.key))
  traceArray = []
  plaintextArray = []

  traceCount = 200 + 1

  for i in range(1,traceCount):
    (plaintext, _, trace) = cw.attackTarget()
    plaintextArray.append(communication.blockToIntList(plaintext))
    traceArray.append(trace)

  bestguess, pge = basicAnalysis.analyse(numpy.array(traceArray),plaintextArray,communication.blockToIntList(arduino.key))
  print(bestguess)
  print(pge)


if __name__ ==  "__main__":

  #arduino = arduinoTarget.ArduinoTarget()
  #cw = whispererHost.whispererHost(arduino)
  #cumulative(arduino, cw)


  visualiser = visualise.Visualise(300, 10)
  visualiser.load("data/10-ohm-complete.pge")
  visualiser.generateMeanPGEGraph()