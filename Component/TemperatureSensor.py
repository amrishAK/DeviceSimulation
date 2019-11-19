from Component.Helper.JsonHandler import JsonHandler
from Component.Handler.eventHook import EventHook
from Component.Sensor import Sensor
from threading import Timer
import random

class TemperatureSensor (Sensor) :

    def __init__(self,inputVoltage):
        super().__init__("TemperatureSensor",3.0,30)
        self.sensingRange = self.SensorChar['SensingRange']

    def __del__(self):
        super().__del__()

    def ToShutdownMode(self):
        self._coreCurrent = self.SensorChar['Current']['ShutdownMode']

    def I2CRead(self):
        self.I2CPowerConsumed()
        return random.randint(self.sensingRange['Min'],self.sensingRange['Max'])
