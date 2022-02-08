import arduinoTarget
import whispererHost
import communication
import analyse
import analysis
import numpy

if __name__ ==  "__main__":
  import matplotlib.pylab as plt
  

  arduino = arduinoTarget.ArduinoTarget()
  cw = whispererHost.whispererHost(arduino)
  print(communication.blockToIntList(arduino.key))
  #traceArray = []
  #plaintextArray = []
  analysis = analysis.Analysis(communication.blockToIntList(arduino.key))

  pgeMean = []
  pgeMax = []
  pgeMin = []
  traceCount = 200 + 1

  for i in range(1,traceCount):
    (plaintext, _, trace) = cw.attackTarget()
    #plaintextArray.append(communication.blockToIntList(plaintext))
    #traceArray.append(trace)
    analysis.addTrace(numpy.array(trace), communication.blockToIntList(plaintext))
    if(i%10==0):
      print(str(i)+" traces")
      bestguess, pge = analysis.calc()
      pgeMean.append(numpy.mean(pge))
      pgeMax.append(numpy.max(pge))
      pgeMin.append(numpy.min(pge))

  print(bestguess)


  plt.figure()
  traceNum = list(range(10, traceCount, 10))
    
  plt.plot(traceNum, pgeMean, 'r', label="PGE Mean")
  plt.plot(traceNum, pgeMax, 'g', label="PGE Max")
  plt.plot(traceNum, pgeMin, 'b', label="PGE Min")
  plt.legend(loc="upper right")
  plt.title('Partial Guessing Entropy of AES-128 ECB')
  plt.xlabel('Trace Number')
  plt.ylabel('Partial Guessing Entropy')
  plt.show()

  
  #bestguess, pge = analyse.analyseResults(numpy.array(traceArray),plaintextArray,communication.blockToIntList(arduino.key))
  #print(bestguess)
  #print(pge)