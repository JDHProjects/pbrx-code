import numpy as np
import pickle
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


  def generateAllPGEGraph(self, saveName="", title='Partial Guessing Entropy of AES-128 ECB', xLabel='Trace Number', yLabel='Partial Guessing Entropy'):
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
    plt.xlim(0, self.tNums[-1])
    plt.ylim(0, 256)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    if(saveName!=""):
      plt.savefig(saveName)
      return
    plt.show()


  def generateMeanPGEGraph(self, saveName="", title='Partial Guessing Entropy of AES-128 ECB (Mean of 100 Attacks)', xLabel='Trace Number', yLabel='Mean Partial Guessing Entropy'):
    inTitle='Partial Guessing Entropy of AES-128 ECB (Mean of '+str(len(self.listOfPges))+' Attacks)'
    self._GeneratePGEGraph(np.mean(np.array(self.listOfPges), axis=0), saveName, inTitle, xLabel, yLabel)


  def generatePGEGraphByIndex(self, index, saveName="", title='Partial Guessing Entropy of AES-128 ECB', xLabel='Trace Number', yLabel='Partial Guessing Entropy'):
    if(index<0 or index > len(self.listOfPges)):
      print("FATAL ERROR: PGE index out of range")
      exit()
    self._GeneratePGEGraph(self.listOfPges[index], saveName, title, xLabel, yLabel)


  def _GeneratePGEGraph(self, pges, saveName, title, xLabel, yLabel):
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
    plt.xlim(0, self.tNums[-1])
    plt.ylim(0, 256)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    if(saveName!=""):
      plt.savefig(saveName)
      return
    plt.show()

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
  visualiser.load("results/100-ohm-mean-100.pge")
  visualiser.generateMeanPGEGraph()