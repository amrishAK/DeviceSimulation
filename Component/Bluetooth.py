from Component.Helper.JsonHandler import JsonHandler
from Component.Handler.eventHook import EventHook
from Component.Helper.SocketServer.SocketClient import SocketClient
from threading import Timer
from sys import getsizeof

class Bluetooth(object) : 

    characteristicsPath = "Characteristics/Bluetooth.json"
    _inputVoltage = 0
    _coreCurrent = 0
    _batteryEvent = EventHook()

    def __init__ (self,inputVoltage,timerVal) :
        self._timerVal = timerVal
        self._socketClient = SocketClient()
        self.jsonHandler = JsonHandler()
        self.BleChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self._inputVoltage = inputVoltage
        self.TurnOn()
    
    def __del__(self):
        self.TurnOff()

    def ToIdleMode(self):
        self._coreCurrent = self.BleChar['Current']['CoreIdle']

    def ToActiveMode(self):
        self._coreCurrent = self.BleChar['Current']['CoreActive']
    
    def TurnOff (self):
        self._timer.cancel()

    def TurnOn (self):
        self.StartTimer()
        self.ToActiveMode()
    
    def PowerConsumed(self,data,isTX = True):
        type_ = 'TX'if isTX else 'RX' 
        dataSize = getsizeof(data) * 8
        time = (dataSize / self.BleChar['BitRate'])/3600.0 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self.BleChar['Current'][type_] 
        self._batteryEvent.fire(powerDischarged=power,reason=('Bluetooth ' + type_))

    def TimerHit(self):
        time = 30/3600 
        power = time * self._inputVoltage * self._coreCurrent
        self._batteryEvent.fire(powerDischarged=power,reason='Bluetooth Timer')
        self.StartTimer()
    
    def StartTimer(self):
        self._timer = Timer(self._timerVal,self.TimerHit)
        self._timer.start()

    def Tx(self,data):
        self.PowerConsumed(data)
        #encode it
        print("Tx --->>> " + str(data))
        try:
            self._socketClient.Transmit(str(data))
        except Exception as exp:
            print("failed due to " + str(exp))

