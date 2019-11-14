from Component.MicroController import MicroController
from Component.Bluetooth import Bluetooth
from Component.Battery import Battery
from Component.TemperatureSensor import TemperatureSensor
from Component.Handler.eventHook import EventHook
import time
import sys

class TemperatureController (MicroController) :

    checker = True

    def __init__(self):
        self.Setup()
        self.ConnectHandlers()
        super().__init__(3.0)

        try:
            while(self.checker):
                self.Run()
        except KeyboardInterrupt:
            self.__del__()
            exit(1)
    
    def __del__(self):
        self.ble.__del__()
        self.ts.__del__()
        self.bt.__del__()
        super().__del__()

    def ConnectHandlers(self):
        self.ble._batteryEvent.addHandler(self.bt.Discharging)
        self.ts._batteryEvent.addHandler(self.bt.Discharging)
        super()._batteryEvent.addHandler(self.bt.Discharging)

    def Setup(self):
        self.bt = Battery()
        self.ble = Bluetooth(3.0)
        self.ts = TemperatureSensor(3.0)

    def Run(self):
        time.sleep(3)
        temp = self.ReadTemperature()
        time.sleep(3)
        self.WriteBluetooth(temp)
        time.sleep(3)

    def ReadTemperature(self):
        super().I2CWrite()
        self.ts.I2CWrite()
        super().I2CRead()
        return self.ts.I2CRead()

    def WriteBluetooth(self,data):
        super().I2CWrite()
        self.ble.Tx(data)