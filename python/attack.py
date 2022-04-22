import arduinoTarget
import whispererHost
import communication
import analysis
import visualise
import basicAnalysis
import numpy

def cumulative(arduino, cw):
  

  traceCount = 500
  traceInterval = 10

  #analyser.load("data/testing")

  visualiser = visualise.Visualise(traceInterval, traceCount)
  #visualiser.load("data/0-ohm-mean-40.pge")

  for i in range(0,1):
    arduino.setRandomKey()
    print(communication.blockToIntList(arduino.key))
    analyser = analysis.Analysis(communication.blockToIntList(arduino.key),2500)
    print("attack: "+str(i))
    for j in range(0,traceCount):
      (plaintext, _, trace) = cw.attackTarget()
      analyser.addTrace(numpy.array(trace[1000:3500]), communication.blockToIntList(plaintext))
      if(j%traceInterval==0):
        bestguess, pge = analyser.calc()
        print(str(j)+" traces:\nPGE sum = "+str(sum(pge)))
        print("Best Guess = "+communication.intListToString(bestguess))
        if (sum(pge)==0):
          break

    visualiser.addPGEs(analyser.getPGEs(traceInterval,traceCount))
    #visualiser.save("data/100-ohm-mean-100.pge")
  #visualiser.generatePGEGraphByIndex(0)
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

  arduino = arduinoTarget.ArduinoTarget()
  cw = whispererHost.whispererHost(arduino)
  cumulative(arduino, cw)

  #visualiser = visualise.Visualise(1000, 10)
  #visualiser.load("data/100-ohm-mean-100.pge")
  #print(len(visualiser.listOfPges))
  #visualiser.generateMeanPGEGraph()