from Component.Helper.JsonHandler import JsonHandler
from Component.Handler.eventHook import EventHook
from threading import Timer
from sys import getsizeof


class MicroController (object) : 
    
    characteristicsPath = "Characteristics/MicroController.json"
    _batteryEvent = EventHook()

    def __init__ (self,inputVoltage) :
        self.jsonHandler = JsonHandler()
        self.ControllerChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self._inputVoltage = inputVoltage
        self.TurnOn()

    def __del__(self):
        self.TurnOff()

    def TurnOn(self) :
        self._timer = Timer(30,self.TimerHit)
        self._timer.start()
        self.ToActiveMode()

    def TurnOff(self):
        self._timer.cancel() 
    
    def ToActiveMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Run']

    def ToIdleMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Idle']

    def ToSleepMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Sleep']

    def I2CRead(self):
        self.I2CPowerConsumed()

    def I2CWrite(self):
        self.I2CPowerConsumed()

    def I2CPowerConsumed(self):
        time = (self.ControllerChar['BitSize'] / self.ControllerChar['BitRate']['I2C'])/3600.0 # bitrate is in seconds, convert it to hours
        power = time * float(self._inputVoltage) * float(self._coreCurrent) 
        self._batteryEvent.fire(powerDischarged=power,reason='MC I2C')
    
    def UartPowerConsumed(self,data):
        bitSize = getsizeof(data) / 8
        time = (bitSize / self.ControllerChar['BitRate']['UART'])/3600.0 # bitrate is in seconds, convert it to hours
        power = time * float(self._inputVoltage) * float(self._coreCurrent) 
        self._batteryEvent.fire(powerDischarged=power,reason='MC I2C')

    def TimerHit(self):
        time = 30/3600
        power = time * self._inputVoltage * self._coreCurrent
        self._batteryEvent.fire(powerDischarged=power,reason='MC Timer')
        self._timer = Timer(30,self.TimerHit)
        self._timer.start()
    