from Component.MicroController import MicroController
from Component.Bluetooth import Bluetooth
from Component.P2pBluetooth import P2pBluetooth
from Component.Battery import Battery
from Component.TemperatureSensor import TemperatureSensor
from Component.Handler.eventHook import EventHook
from Component.Helper.JsonHandler import JsonHandler
import time
import sys

class TemperatureController (MicroController) :

    _characteristicsPath = "Characteristics/TemperatureController.json"
    _sensorId = 'Temperature'

    def Setup(self):
        self.bt = Battery(self._ControllerChar['Battery']['CurrentState']['Power'])
        self.ble = P2pBluetooth(3.0,30,self._sensorId)
        self.ts = TemperatureSensor(3.0)

    def __init__(self):
        self.jsonHandler = JsonHandler()
        self._ControllerChar = self.jsonHandler.LoadJson(self._characteristicsPath)
        self.Setup()
        self.ConnectHandlers()
        super().__init__(3.0,self._sensorId)

        #Change Mode -->>
        self.ts.SetRegister()

        try:
            while(True):
                self.Run()
        except KeyboardInterrupt:
            self._ControllerChar['Battery']['CurrentState']['Power'] = self.bt.GetCurrentCharge()
            self.__del__()
            exit(1)
    
    def __del__(self):
        self.jsonHandler.WriteJson(self._characteristicsPath,self._ControllerChar)
        self.ble.__del__()
        self.ts.__del__()
        self.bt.__del__()
        super().__del__()

    def ConnectHandlers(self):
        self.ble._batteryEvent.addHandler(self.bt.Discharging)
        self.ts._batteryEvent.addHandler(self.bt.Discharging)
        self.ts._interupt.addHandler(self.ReceiveInterupt)
        self._batteryEvent.addHandler(self.bt.Discharging)

    def Run(self):
        pass

    def ReceiveInterupt(self):
        self.I2CRead()
        data =  self.ts.RI2CRead()
        self.WriteBluetooth(data)

    def ReadTemperature(self):
        self.I2CRead()
        return self.ts.I2CRead()

    def WriteBluetooth(self,data):
        data = self.Encrypt(data)
        data = str(data) + '|Temperature|1'
        self.UartPowerConsumed(data)
        self.ble.Tx(data)
