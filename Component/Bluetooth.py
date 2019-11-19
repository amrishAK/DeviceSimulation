from Component.Helper.JsonHandler import JsonHandler
from Component.Handler.eventHook import EventHook
from Component.Helper.SocketServer.SocketClient import SocketClient
from Component.Helper.SocketServer.SocketServer import SocketServer
from threading import Timer
import time
from sys import getsizeof

class Bluetooth(object) : 

    characteristicsPath = "Characteristics/Bluetooth.json"
    _inputVoltage = 0
    _coreCurrent = 0
    _batteryEvent = EventHook()
    _uartEvent = EventHook()
    _socketClient = SocketClient()
    _socketServer = SocketServer()

    def __init__ (self,inputVoltage,timerVal) :
        self._timerVal = timerVal
        self.jsonHandler = JsonHandler()
        self.BleChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self._inputVoltage = inputVoltage
        self.TurnOn()
        self.ConnectHandlers()
    
    def __del__(self):
        self.TurnOff()

    def ConnectHandlers(self):
        self._socketServer._socketHandler.addHandler(self.Rx)

    def ToIdleMode(self):
        self._coreCurrent = self.BleChar['Current']['CoreIdle']
        if self._socketServer._isSocketUp:
            self._socketServer.SocketClosing()

    def ToActiveMode(self):
        self._coreCurrent = self.BleChar['Current']['CoreActive']
        if self._socketServer._isSocketUp:
            self._socketServer.SocketClosing()

    def ToRxMode(self):
        self._coreCurrent = self.BleChar['Current']['RX']
        self._socketServer.Setup()
    
    def TurnOff (self):
        self._timer.cancel()

    def TurnOn (self):
        self.StartTimer()
        self.ToActiveMode()

    def PowerConsumedUART(self,data):
        dataSize = getsizeof(data) * 8
        time = (dataSize / self.BleChar['BitRate']['UART'])/3600.0 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self.BleChar['Current']['UART'] 
        self._batteryEvent.fire(powerDischarged=power,reason=('Bluetooth UART'))
    
    def PowerConsumed(self,data,isTX = True):
        type_ = 'TX'if isTX else 'RX' 
        dataSize = getsizeof(data) * 8
        time = (dataSize / self.BleChar['BitRate']['BLE'])/3600.0 # bitrate is in seconds, convert it to hours
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
        self.PowerConsumedUART(data)
        time.sleep(0.25)
        self.PowerConsumed(data)
        #encode it
        print("Tx --->>> " + str(data))
        try:
            self._socketClient.Transmit(str(data))
        except Exception as exp:
            print("failed due to " + str(exp))

    def Rx(self,**kwargs):
        data = kwargs.get('data')
        self.PowerConsumed(data,False)
        self.PowerConsumedUART(data)
        self._uartEvent.fire(data=data)

