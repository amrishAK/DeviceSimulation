from Helper.JsonHandler import JsonHandler
from Handler.eventHook import EventHook
from threading import Timer

class MicroController (object) : 
    
    characteristicsPath = "Characteristics/MicroController.json"
    _inputVoltage = 0
    _coreCurrent = 0
    _batteryEvent = EventHook()
    _timer = Timer(30,TimerHit)

    def __init__ (self,inputVoltage) :
        self.jsonHandler = JsonHandler()
        self.ControllerChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self._inputVoltage = inputVoltage
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Run']

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
        time = (self.ControllerChar['BitSize'] / self.ControllerChar['BitRate'])/3600 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self._coreCurrent 
        self._batteryEvent.fire(powerDischarged=power)

    def TimerHit(self):
        time = 30/3600
        power = time * self._inputVoltage * self._coreCurrent
        self._batteryEvent.fire(powerDischarged=power)
        self._timer = Timer(30,self.TimerHit)
        self._timer.start()
    