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
    _isSingleHop = True
    _currentPort = 63342
    Memory = []

    def __init__ (self,inputVoltage,timerVal,isSingleHop=True,txPorts = [],serverPort=63342) :
        self._timerVal = timerVal
        self.jsonHandler = JsonHandler()
        self.BleChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self.serverPort = serverPort
        self._socketServer = SocketServer(serverPort)
        self._inputVoltage = inputVoltage
        self._txPorts = txPorts
        if len(self._txPorts) > 0:
            dict_ = self._txPorts[0]
            _,port = list(dict_.items())[0]
            self._currentPort = port

        self._isSingleHop = isSingleHop
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
        self._socketServer = SocketServer(self.serverPort)
        self._socketServer.Setup()
    
    def TurnOff (self):
        self._timer.cancel()

    def TurnOn (self):
        self.StartTimer()
        self.ToActiveMode()

    def PowerConsumedUART(self,data):
        dataSize = getsizeof(data) / 8
        time = (dataSize / self.BleChar['BitRate']['UART'])/3600.0 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self.BleChar['Current']['UART'] 
        self._batteryEvent.fire(powerDischarged=power,reason=('Bluetooth UART'))
    
    def PowerConsumed(self,data,isTX = True):
        type_ = 'TX'if isTX else 'RX' 
        dataSize = getsizeof(data) / 8
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
            self._socketClient.Transmit(str(data),self._currentPort)

        except ConnectionRefusedError:
            DataTransferAttempts = 0
            print("Tx------>>> connection failed port: ",self._currentPort)
            for node in self._txPorts :
                nodeId,port = list(node.items())[0]
                print("Tx------>>> Trying id : "+nodeId + " port: ",port)
                if port == self._currentPort :
                    continue
                else:
                    try:
                        DataTransferAttempts+=1
                        #if there is memory in storage transfer it
                        if(len(self.Memory)>0):
                            for storedData in self.Memory:
                                self._socketClient.Transmit(str(storedData),port)
                        else:
                            self._socketClient.Transmit(str(data),port)
                        self._currentPort = port
                        return
                    except ConnectionRefusedError:
                        print("Tx------>>> connection failed port: ",port)
                        continue

            print("No Node available to receive data")
            print("Saving data to buffer")
            #chekcs if buffer is full
            if(len(self.Memory)<5):
                self.Memory.append(data)
            else:
                print("Buffer is full oldest data point is now lost")
                del self.Memory[0]
                self.Memory.append(data)

    def Rx(self,**kwargs):
        data = kwargs.get('data')
        self.PowerConsumed(data,False)
        self.PowerConsumedUART(data)
        self._uartEvent.fire(data=data)

