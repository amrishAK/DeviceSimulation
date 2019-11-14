from Helper.JsonHandler import JsonHandler
from Handler.eventHook import EventHook
from threading import Timer
from sys import getsizeof

class Bluetooth(object) : 

    characteristicsPath = "Characteristics/Battery.json"
    _inputVoltage = 0
    _coreCurrent = 0
    _batteryEvent = EventHook()
    _timer = Timer(30,TimerHit)

    def __init__ (self,inputVoltage) :
        self.jsonHandler = JsonHandler()
        self.BleChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self._inputVoltage = inputVoltage
        self.TurnOn()

    def ToIdleMode(self):
        self._coreCurrent = self.BleChar['Current']['CoreIdle']

    def ToActiveMode(self):
        self._coreCurrent = self.BleChar['Current']['CoreActive']
    
    def TurnOff (self):
        self._timer.cancel()

    def TurnOn (self):
        #power drop for pairing s = br * d
        self._timer = Timer(30,self.TimerHit)
        self._timer.start()
        self.ToActiveMode()
    
    def PowerConsumed(self,data,isTX = True):
        type_ = 'TX'if isTX else 'RX' 
        dataSize = data.nbytes * 8
        time = (dataSize / self.BleChar['BitRate'])/3600 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self.BleChar['Current'][type_] 
        self._batteryEvent.fire(powerDischarged=power)

    def TimerHit(self):
        time = 30/3600
        power = time * self._inputVoltage * self._coreCurrent
        self._batteryEvent.fire(powerDischarged=power)
        self._timer = Timer(30,self.TimerHit)
        self._timer.start()

    def Tx(self,data):
        self.PowerConsumed(data)
        #using sockets to transfer

