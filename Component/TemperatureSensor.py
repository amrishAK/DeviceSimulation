from Component.Helper.JsonHandler import JsonHandler
from Component.Handler.eventHook import EventHook
from Component.Sensor import Sensor
from threading import Timer
import random

class TemperatureSensor (Sensor) :

    _interupt = EventHook()

    def __init__(self,inputVoltage):
        super().__init__("TemperatureSensor",3.0,30)
        self.sensingRange = self.SensorChar['SensingRange']

    def __del__(self):
        super().__del__()
        self._rTimer.cancel()

    def ToShutdownMode(self):
        self._coreCurrent = self.SensorChar['Current']['ShutdownMode']

    def SetRegister(self):
        print("SR")
        self.ToShutdownMode()
        self._rTimer = Timer(5,self.RHit)
        self._rTimer.start()

    def RHit(self):
        val = random.randint(34,40)
        if not (val >= 36 and val <= 38):
            self._temperature = val
            self._interupt.fire()
        time = 0.5/3600
        power = time * self._inputVoltage * self.SensorChar['Current']['AciveMode']
        self._batteryEvent.fire(powerDischarged=power,reason= (self._sensorName + " Timer"))
        self._rTimer = Timer(5,self.RHit)
        self._rTimer.start()
        
    def RI2CRead(self):
        self.I2CPowerConsumed()
        return int(self._temperature)

    def I2CRead(self):
        self.I2CPowerConsumed()
        return random.randint(self.sensingRange['Min'],self.sensingRange['Max'])
