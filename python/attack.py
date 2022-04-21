import arduinoTarget
import whispererHost
import communication
import analysis
import visualise
import basicAnalysis
import numpy

def cumulative(arduino, cw):
  

  traceCount = 20000
  traceInterval = 50

  #analyser.load("data/testing")

  visualiser = visualise.Visualise(traceInterval, traceCount)
  visualiser.load("data/0-ohm-mean-100.pge")

  for i in range(0,90):
    arduino.setRandomKey()
    print(communication.blockToIntList(arduino.key))
    analyser = analysis.Analysis(communication.blockToIntList(arduino.key),2500)
    print("attack: "+str(i))
    for j in range(0,traceCount):
      (plaintext, _, trace) = cw.attackTarget()
      analyser.addTrace(numpy.array(trace[1000:3500]), communication.blockToIntList(plaintext))
      if(j%traceInterval==0):
        bestguess, pge = analyser.calc()
        print(str(j)+" traces: PGE sum = "+str(sum(pge)))
        if (sum(pge)==0):
          break
      

    visualiser.addPGEs(analyser.getPGEs(traceInterval,traceCount))
    visualiser.save("data/0-ohm-mean-100.pge")

  #visualiser.generateMeanPGEGraph()
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
  #cw = whispererHost.WhispererHost(arduino)
  #cumulative(arduino, cw)


  visualiser = visualise.Visualise(20000, 50)
  visualiser.load("data/0-ohm-mean-40.pge")
  print(len(visualiser.listOfPges))
  visualiser.generateMeanPGEGraph()