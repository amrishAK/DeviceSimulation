from Component.EdgeController import EdgeController
from Component.Bluetooth import Bluetooth
from Component.Battery import Battery
from Component.TemperatureSensor import TemperatureSensor
from Component.Handler.eventHook import EventHook
from Component.Helper.JsonHandler import JsonHandler
from Component.Helper.Mqtt.MqttPublisher import MqttPublisher
import time
import sys

class EdgeNodeController (EdgeController) :

    _characteristicsPath = "Characteristics/TemperatureController.json"

    def Setup(self):
        self.bt = Battery(self._ControllerChar['Battery']['CurrentState']['Power'])
        self.ble = Bluetooth(3.0,30)
        self.ble.ToRxMode()

    def __init__(self):
        self.jsonHandler = JsonHandler()
        self._ControllerChar = self.jsonHandler.LoadJson(self._characteristicsPath)
        self.Setup()
        self.ConnectHandlers()
        self._mqttService = MqttPublisher("EdgeNode","DS/Node1/Temperature")
        super().__init__(3.0)

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
        self.bt.__del__()
        super().__del__()

    def ConnectHandlers(self):
        self.ble._batteryEvent.addHandler(self.bt.Discharging)
        self._batteryEvent.addHandler(self.bt.Discharging)
        self.ble._uartEvent.addHandler(self.UartRx)

    def Run(self):
        pass

    def UartRx(self,**kwargs):
        data = kwargs.get('data')
        self.UartPowerConsumed(data)
        print('RX --->>>', str(data))
        self.WifiPowerConsumed(data)
        self._mqttService.Publish(data)

