from Helper.JsonHandler import JsonHandler
from Handler.eventHook import EventHook
from threading import Timer
import random

class TemperatureSensor (object) :

    characteristicsPath = "Characteristics/Battery.json"
    _inputVoltage = 0
    _coreCurrent = 0
    _batteryEvent = EventHook()
    _timer = Timer(30,TimerHit)

    def __init__(self,inputVoltage):
        self.jsonHandler = JsonHandler()
        self.SensorChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self.sensingRange = self.SensorChar['SensingRange']
        self._inputVoltage = inputVoltage
        self.TurnOn()

    def TurnOn(self) :
        self._timer = Timer(30,self.TimerHit)
        self._timer.start()
        self.ToActiveMode()

    def TurnOff(self):
        self._timer.cancel()

    def ToActiveMode(self):
        self._coreCurrent = self.SensorChar['Current']['AciveMode']

    def ToShutdownMode(self):
        self._coreCurrent = self.SensorChar['Current']['ShutdownMode']

    def I2CRead(self):
        self.I2CPowerConsumed()
        return random.randint(self.sensingRange['Min'],self.sensingRange['Max'])

    def I2CWrite(self):
        self.I2CPowerConsumed()

    def I2CPowerConsumed(self):
        time = (self.SensorChar['BitSize'] / self.SensorChar['BitRate'])/3600 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self._coreCurrent 
        self._batteryEvent.fire(powerDischarged=power)

    def TimerHit(self):
        time = 30/3600
        power = time * self._inputVoltage * self._coreCurrent
        self._batteryEvent.fire(powerDischarged=power)
        self._timer = Timer(30,self.TimerHit)
        self._timer.start()