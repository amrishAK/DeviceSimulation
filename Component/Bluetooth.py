from Helper.JsonHandler import JsonHandler
from Battery import Battery

class Bluetooth(object) : 

    characteristicsPath = "Characteristics/Battery.json"

    def __init__ (self) :
        self.jsonHandler = JsonHandler()
        self.BleChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self.battery = Battery()
        self.battery.Discharging(self.PowerConsumedTx(0.02))

    def PowerConsumedTx(self,dataSize):
        time = self.BleChar['BitRate'] * dataSize
        power = time * self.BleChar['Voltage']['Input'] * self.BleChar['Current']['TX'] 
        return power

    def PowerConsumedRx(self,dataSize):
        time = self.BleChar['BitRate'] * dataSize
        power = time * self.BleChar['Voltage']['Input'] * self.BleChar['Current']['RX']
        return power