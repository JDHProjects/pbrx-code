import chipwhisperer

import communication
from common import errorAndExit
import arduinoTarget

class whispererHost():
  def __init__(self, target):
    self.scope = chipwhisperer.scope()
    self.scope.default_setup()
    self.scope.clock.clkgen_freq = 16000000
    self.scope.adc.samples = 5000
    self.target = target

  def attackTarget(self):
    plaintext = communication.getRandomBlock("P")
    self.scope.arm()
    receive = self.target.sendBlock(plaintext)
    ret = self.scope.capture()

    if ret:
      errorAndExit("Timeout happened during capture")

    wave = self.scope.get_last_trace()
    if len(wave) >= 1:
      return (plaintext, receive, wave)
    else:
      errorAndExit("Trace empty")


if __name__ ==  "__main__":
  import matplotlib.pylab as plt

  arduino = arduinoTarget.ArduinoTarget()
  cw = whispererHost(arduino)

  plt.figure(figsize=(16, 8), dpi=80)
  plt.plot(cw.attackTarget()[2][1000:2500], 'r')
  plt.plot(cw.attackTarget()[2][1000:2500], 'g')
  plt.plot(cw.attackTarget()[2][1000:2500], 'b')
  plt.show()
  input()
  plt.close()
