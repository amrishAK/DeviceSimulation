from Component.EdgeController import EdgeController
from Component.Bluetooth import Bluetooth
from Component.P2pBluetooth import P2pBluetooth
from Component.Battery import Battery
from Component.TemperatureSensor import TemperatureSensor
from Component.Handler.eventHook import EventHook
from Component.Helper.JsonHandler import JsonHandler
from Component.Helper.Mqtt.MqttPublisher import MqttPublisher
from Component.HeartRateSensor import HeartRateSensor
from threading import Timer
import time
import sys
import json

class GlucoseController (EdgeController) :

    _characteristicsPath = "Characteristics/TemperatureController.json"
    _sensorId = 'Gulcometer'
    def Setup(self):
        self.bt = Battery(self._ControllerChar['Battery']['CurrentState']['Power'])
        self.ble = P2pBluetooth(3.0,30,self._sensorId)
        self.SetP2P()
        self.sensor = HeartRateSensor(3.0)
        self.ble.ToRxMode()

    def __init__(self):
        self.jsonHandler = JsonHandler()
        self._ControllerChar = self.jsonHandler.LoadJson(self._characteristicsPath)
        self.Setup()
        self.ConnectHandlers()
        self._privateKey = self._ControllerChar['PrivateKey']
        mqtt = self._ControllerChar['Mqtt']
        self._mqttService = MqttPublisher(mqtt['Name'],mqtt['Topic'])
        self._LogData = []
        self._bulkPushTimer = Timer(150,self.BulkPushTimerHit)
        self._bulkPushTimer.start()
        super().__init__(3.0,self._sensorId)

        try:
            while(True):
                self.Run()
        except KeyboardInterrupt:
            self.BulkPushTimerHit()
            self._ControllerChar['Battery']['CurrentState']['Power'] = self.bt.GetCurrentCharge()
            self.__del__()
            exit(1)
    
    def __del__(self):
        self.jsonHandler.WriteJson(self._characteristicsPath,self._ControllerChar)
        self.ble.__del__()
        self.bt.__del__()
        super().__del__()

    def SetP2P(self):
        self._p2pTimer = Timer(10,self.P2pTimerHit)
        self._p2pTimer.start()

    def P2pTimerHit(self):
        self.ble.BroadCasting(self.bt.GetCurrentCharge())
        self._p2pTimer = Timer(10,self.P2pTimerHit)
        self._p2pTimer.start()


    def ConnectHandlers(self):
        self.ble._batteryEvent.addHandler(self.bt.Discharging)
        self.sensor._batteryEvent.addHandler(self.bt.Discharging)
        self._batteryEvent.addHandler(self.bt.Discharging)
        self.ble._uartEvent.addHandler(self.UartRx)

    def Run(self):
        self.PushAll()

    def PushAll(self):
        time.sleep(3)
        temp = self.ReadTemperature()
        print('OxyMeter--->>',temp)
        time.sleep(1)
        #time.sleep(3)
        self.WifiTx(self.Encrypt(temp),'HeartRate')

    def Push(self):
        pass

    def UartRx(self,**kwargs):
        data = kwargs.get('data')
        self.UartPowerConsumed(data)
        print('RX --->>>', str(data))
        dataArray = str(data).split('|')
        
        if dataArray[2] == '0' :
            self.WifiTx(dataArray[0],dataArray[1])
        else:
            self._LogData.append(data)
            pass

    def WifiTx(self,data,topic):
        self.WifiPowerConsumed(data)
        self._mqttService.Publish(data,topic)

    def WifiBulkPush(self):
        data = self._LogData
        self.WifiPowerConsumed(data,True,False)
        data = {"Data" : data}
        self._mqttService.Publish(json.dumps(data),'BulkPush')
        self._LogData = []

    def BulkPushTimerHit(self):
        if len(self._LogData) > 0 :
            self.WifiBulkPush()
        self._bulkPushTimer = Timer(150,self.BulkPushTimerHit)
        self._bulkPushTimer.start()

    def ReadTemperature(self):
        self.I2CRead()
        return self.sensor.I2CRead()


if __name__ == "__main__":
    GlucoseController()


