import chipwhisperer
import communication

class WhispererHost():
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
      print("FATAL ERROR: Timeout happened during capture")
      exit()

    wave = self.scope.get_last_trace()
    if len(wave) >= 1:
      return (plaintext, receive, wave)
    else:
      print("FATAL ERROR: Trace empty")
      exit()


if __name__ ==  "__main__":
  import matplotlib.pylab as plt
  import arduinoTarget

  arduino = arduinoTarget.ArduinoTarget()
  cw = WhispererHost(arduino)

  plt.figure(figsize=(16, 8), dpi=80)
  plt.plot(cw.attackTarget()[2][1000:2500], 'r')
  plt.plot(cw.attackTarget()[2][1000:2500], 'g')
  plt.plot(cw.attackTarget()[2][1000:2500], 'b')
  plt.show()
