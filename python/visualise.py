import numpy as np
import pickle
import math
import matplotlib.pylab as plt

class Visualise:
  def __init__(self, tInterval, tNum):
    self.listOfPges = []
    self.tNums = list(range(0,tNum,tInterval))


  def addPGEs(self, pges):
    if(len(self.tNums) != len(pges)):
      print("FATAL ERROR: PGE interval not equal to existing data")
      exit()
    self.listOfPges.append(pges)


  def generateAllPGEGraph(self, saveName="", title='Partial Guessing Entropy of AES-128 ECB', xLabel='Trace Number', yLabel='Partial Guessing Entropy', xLimit=-1):
    plt.figure()
    plt.autoscale(False)

    for pges in self.listOfPges:
      pgeMean = []
      pgeMax = []
      pgeMin = []
      for i in range(0, len(self.tNums)):
        pgeMean.append(np.mean(pges[i]))
        pgeMax.append(np.max(pges[i]))
        pgeMin.append(np.min(pges[i]))
      
      plt.plot(self.tNums, pgeMean, 'r')
      plt.plot(self.tNums, pgeMax, 'g')
      plt.plot(self.tNums, pgeMin, 'b')


    plt.legend(["PGE Mean", "PGE Max", "PGE Min"], loc="upper right")
    if (xLimit == -1):
      plt.xlim(0, self.tNums[-1])
    else:
      plt.xlim(0, xLimit)
    plt.ylim(0, 256)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    if(saveName!=""):
      plt.savefig(saveName)
      return
    plt.show()


  def generateMeanPGEGraph(self, saveName="", title='Partial Guessing Entropy of AES-128 ECB', xLabel='Trace Number', yLabel='Mean Partial Guessing Entropy', xLimit=-1):
    inTitle=title+'\nMean of '+str(len(self.listOfPges))+' Attacks'
    self._GeneratePGEGraph(np.mean(np.array(self.listOfPges), axis=0), saveName, inTitle, xLabel, yLabel, xLimit)


  def generatePGEGraphByIndex(self, index, saveName="", title='Partial Guessing Entropy of AES-128 ECB', xLabel='Trace Number', yLabel='Partial Guessing Entropy', xLimit=-1):
    if(index<0 or index > len(self.listOfPges)):
      print("FATAL ERROR: PGE index out of range")
      exit()
    self._GeneratePGEGraph(self.listOfPges[index], saveName, title, xLabel, yLabel, xLimit)

  def _GeneratePGEGraph(self, pges, saveName, title, xLabel, yLabel, xLimit):
    pgeMean = []
    pgeMax = []
    pgeMin = []
    for i in range(0, len(self.tNums)):
      pgeMean.append(np.mean(pges[i]))
      pgeMax.append(np.max(pges[i]))
      pgeMin.append(np.min(pges[i]))
    plt.figure()
    plt.autoscale(False)

    plt.plot(self.tNums, pgeMean, 'r', label="PGE Mean")
    plt.plot(self.tNums, pgeMax, 'g', label="PGE Max")
    plt.plot(self.tNums, pgeMin, 'b', label="PGE Min")
    plt.legend(loc="upper right")
    if (xLimit == -1):
      plt.xlim(0, self.tNums[-1])
    else:
      plt.xlim(0, xLimit)
    plt.ylim(0, 256)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    if(saveName!=""):
      plt.savefig(saveName)
      return
    plt.show()

  def heatmapAtIndex(self, index, saveName="", title=""):
    outputData = []
    outputRow = []
    xy = math.floor(math.sqrt(len(self.listOfPges)))
    if(index not in self.tNums):
      print("FATAL ERROR: Index not in PGE list")
      exit()
    realIndex = self.tNums.index(index)
    for i in range(0,xy**2):
      if (i > 0 and i % xy == 0):
        outputData.append(outputRow)
        outputRow = []
      outputRow.append(sum(self.listOfPges[i][realIndex]))
    outputData.append(outputRow)

    fig, ax = plt.subplots()
    im = ax.imshow(outputData)
    plt.imshow(outputData, cmap='jet')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.colorbar()
    plt.title((title))
    if(saveName!=""):
      plt.savefig(saveName)
      return
    plt.show()

  def bestWorstAverage(self):
    minimum = -1
    maximum = 0
    resultsList = []
    for pge in self.listOfPges:
      firstZero = pge.index([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
      resultsList.append(firstZero)
      if minimum > firstZero or minimum == -1:
        minimum = firstZero
      if maximum < firstZero:
        maximum = firstZero
    
    return (self.tNums[minimum], self.tNums[maximum], self.tNums[round(np.mean(resultsList))])

  def save(self, filename):
    visualiseSave = []
    visualiseSave.append(self.listOfPges)
    visualiseSave.append(self.tNums)
    with open(filename, 'wb') as writeFile:
      pickle.dump(visualiseSave, writeFile)

  def load(self, filename):
    visualiseLoad = []
    with open (filename, 'rb') as readFile:
      visualiseLoad = pickle.load(readFile)
    self.listOfPges = visualiseLoad[0]
    self.tNums = visualiseLoad[1]

if __name__ ==  "__main__":
  visualiser = Visualise(1000, 10)
  ohm="0"
  symbol=ohm+"$\Omega$"
  if(ohm == "0"):
    symbol="No"

  visualiser.load("results/"+ohm+"-ohm-mean-100.pge")
  (best, worst, average) = visualiser.bestWorstAverage()
  print(ohm+" OHM RESULTS\n-------------\nbest: "+str(best)+"\nworst: "+str(worst)+"\naverage:"+str(average))
  
  visualiser.heatmapAtIndex(average, title="Heatmap of PGE Sum of AES-128 ECB - "+symbol+" Shunt Resistor\nAfter Analysis of "+str(average)+" Power Traces")
  visualiser.generatePGEGraphByIndex(1, title="Partial Guessing Entropy of AES-128 ECB - "+symbol+" Shunt Resistor", xLimit=average+50)
  visualiser.generateMeanPGEGraph(title="Partial Guessing Entropy of AES-128 ECB - "+symbol+" Shunt Resistor", xLimit=average+50)