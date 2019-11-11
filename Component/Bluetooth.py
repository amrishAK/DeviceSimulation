from Helper.JsonHandler import JsonHandler
from Battery import Battery
from sys import getsizeof

class Bluetooth(object) : 

    characteristicsPath = "Characteristics/Battery.json"
    _inputVoltage = 0
    _coreCurrent = 0

    def __init__ (self,inputVoltage) :
        self.jsonHandler = JsonHandler()
        self.BleChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self._inputVoltage = inputVoltage
        self._coreCurrent = self.BleChar['Current']['CoreActive']

    def ToIdleMode(self):
        self._coreCurrent = self.BleChar['Current']['CoreIdle']

    def ToActiveMode(self):
        self._coreCurrent = self.BleChar['Current']['CoreActive']
    
    def TurnOff (self):
        #update power consumension
        pass

    def TurnOn (self):
        #power drop for pairing s = br * d
        self.ToActiveMode()
    
    def PowerConsumedTx(self,dataSize):
        time = (dataSize / self.BleChar['BitRate'])/3600 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self.BleChar['Current']['TX'] 
        return power

    def PowerConsumedRx(self,dataSize):
        time = (dataSize / self.BleChar['BitRate'])/3600 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self.BleChar['Current']['RX']
        return power

    def Tx(self,data):
        bitSize = data.nbytes * 8
        self.PowerConsumedTx(bitSize)
        #using sockets to transfer
