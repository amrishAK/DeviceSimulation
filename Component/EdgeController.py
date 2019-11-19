from Component.Helper.JsonHandler import JsonHandler
from Component.Handler.eventHook import EventHook
from threading import Timer
from sys import getsizeof

class EdgeController (object) : 
    
    characteristicsPath = "Characteristics/EdgeController.json"
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
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Active']

    def ToShutDownMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['ShutDown']

    def ToLightSleepMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['LightSleep']

    def ToDeepSleepMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['DeepSleep']

    def UartTx(self,data):
        self.UartPowerConsumed(data)

    def UartRx(self,data):
        self.UartPowerConsumed(data)

    def UartPowerConsumed(self,data):
        bitSize = getsizeof(data) * 8
        time = (bitSize / self.ControllerChar['BitRate']['UART'])/3600.0 # bitrate is in seconds, convert it to hours
        power = time * float(self._inputVoltage) * float(self._coreCurrent) 
        self._batteryEvent.fire(powerDischarged=power,reason='MC UART')

    def WifiTx(self,data):
        self.WifiPowerConsumed(data)
        print('Wifi TX----->>> ', data)

    def WifiPowerConsumed(self,data,isTx = True,isVersionB = True):
        version = 'b' if isVersionB else 'g'
        _type = 'TX' if isTx else 'RX'
        bitSize = getsizeof(data) * 8
        time = (bitSize / self.ControllerChar['BitRate'][_type][version])/3600.0 # bitrate is in seconds, convert it to hours
        power = time * float(self._inputVoltage) * self.ControllerChar['Current'][_type][version] 
        self._batteryEvent.fire(powerDischarged=power,reason='Edge Controller ' + _type + ' ' + version)

    def TimerHit(self):
        time = 30/3600
        power = time * self._inputVoltage * self._coreCurrent
        self._batteryEvent.fire(powerDischarged=power,reason='MC Timer')
        self._timer = Timer(30,self.TimerHit)
        self._timer.start()