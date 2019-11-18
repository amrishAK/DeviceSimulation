from Component.Handler.eventHook import EventHook
from Component.Helper.JsonHandler import JsonHandler
from threading import Timer
import random

class Sensor(object) :
 
    _inputVoltage = 0
    _coreCurrent = 0
    _batteryEvent = EventHook()

    def __init__(self,sensorName,inputVoltage,timerVal):
        self._sensorName = sensorName
        self._timerVal = timerVal
        self.jsonHandler = JsonHandler()
        self.SensorChar = self.jsonHandler.LoadJson("Characteristics/"+ sensorName +".json")
        self._inputVoltage = inputVoltage
        self.TurnOn()

    def __del__(self):
        self.TurnOff()

    def TurnOn(self) :
        self.StartTimer()
        self.ToActiveMode()

    def TurnOff(self):
        self._timer.cancel()

    def ToActiveMode(self):
        self._coreCurrent = self.SensorChar['Current']['AciveMode']

    def I2CWrite(self):
        self.I2CPowerConsumed()

    def I2CPowerConsumed(self,isRead = True):
        _type = 'Read' if isRead else 'Write'
        time = (self.SensorChar['BitSize'] / self.SensorChar['BitRate'])/3600.0 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self._coreCurrent 
        self._batteryEvent.fire(powerDischarged=power,reason=(self._sensorName + ' I2C'))

    def TimerHit(self):
        time = self._timerVal/3600
        power = time * self._inputVoltage * self._coreCurrent
        self._batteryEvent.fire(powerDischarged=power,reason= (self._sensorName + " Timer"))
        self.StartTimer()

    def StartTimer(self):
        self._timer = Timer(self._timerVal,self.TimerHit)
        self._timer.start()