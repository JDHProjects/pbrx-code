import chipwhisperer

import communication
from common import errorAndExit
import arduinoTarget

class whispererHost():
  def __init__(self, target):
    self.scope = chipwhisperer.scope()
    self.scope.default_setup()
    self.scope.clock.clkgen_freq = 16000000
    self.target = target

  def attackTarget(self):
    self.scope.arm()
    receive = self.target.sendBlock(communication.getRandomBlock("P"))
    ret = self.scope.capture()

    if ret:
      errorAndExit("Timeout happened during capture")

    wave = self.scope.get_last_trace()
    if len(wave) >= 1:
      return (receive, wave)
    else:
      errorAndExit("Trace empty")


import matplotlib.pylab as plt

if __name__ ==  "__main__":
  arduino = arduinoTarget.ArduinoTarget()
  cw = whispererHost(arduino)

  plt.figure(figsize=(16, 8), dpi=80)
  plt.plot(cw.attackTarget()[1], 'r')
  plt.plot(cw.attackTarget()[1], 'g')
  plt.plot(cw.attackTarget()[1], 'b')
  plt.show()
  input()
  plt.close()