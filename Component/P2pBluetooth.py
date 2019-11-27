from Component.Helper.JsonHandler import JsonHandler
from Component.Handler.eventHook import EventHook
from Component.Helper.SocketServer.SocketClient import SocketClient
from Component.Helper.SocketServer.SocketServer import SocketServer
from Component.Bluetooth import Bluetooth
from threading import Timer
import time
from sys import getsizeof
from operator import itemgetter

class P2pBluetooth(Bluetooth):

    _characteristicsPath = "Characteristics/RoutingTable.json"

    def __init__(self,inputVoltage,timerVal,SensorID):
        self.jsonHandler = JsonHandler()
        routingTable = self.jsonHandler.LoadJson(self._characteristicsPath)
        self._routingTable = routingTable[SensorID]
        super().__init__(inputVoltage,timerVal,False,self._routingTable['Tx'],self._routingTable['Port'])
        self._sensorID = SensorID
        print(self._routingTable)
        if 'Flooding' in self._routingTable:
            self.NodePortList = self._routingTable['Flooding']
        self.NodeBatteryLevelList = []
        self._broadCasting = False
        self._broadCastingNodes = self._routingTable['BroadCastingNodes']
        self.P2pConnectHandlers()

    def __del__(self):
        super().__del__()

    def P2pConnectHandlers(self):
        self._socketServer._p2pHandler.addHandler(self.P2pRx)

    def P2pRx(self,**kwargs):
        data = kwargs.get('data')
        dataArray = str(data).split('-')
        print( self.NodePortList)
        result,nodeId,port = self.GetNodeId(dataArray[1])
        print(result,nodeId,port)
        if result :
            self.NodeBatteryLevelList.append({'Id' : nodeId,'Port' : port, 'BatteryLevel' : dataArray[0]})
        if self._broadCastingNodes == len(self.NodeBatteryLevelList):
            a = sorted(self.NodeBatteryLevelList, key=itemgetter('BatteryLevel'), reverse=True)
            a = a[0]
            print("Chossen Sensor is ", a['Id'])
            if a['Id'] != self._sensorID:
                self.ToActiveMode()
    

    def GenearteBatteryLevelDict(self,index):
        array = []
        for node in self.NodePortList:
            nodeId,port = list(node.items())[0]
            array.append({'Id' : nodeId,'Port' : port, 'BatteryLevel' : 0})
        return array

    def GetNodeId(self,key):
        nodeId = ''
        port = ''
        result = False
        for node in self.NodePortList:
            if key in node:
                nodeId,port = list(node.items())[0]
                result = True
                return result,nodeId,port
        return result,nodeId,port
    
    def BroadCasting(self,Batterydata):
        self._broadCasting = True
        self.NodeBatteryLevelList = []
        self._broadCastingNodes = self._routingTable['BroadCastingNodes']
        if not self._socketServer._isSocketUp:
            self.ToRxMode()
        time.sleep(0.25)
        #loops through each port in priority list and contacts them
        # 
        for node in self.NodePortList:
            _,port = list(node.items())[0]
            data = str(Batterydata) + "-" + self._sensorID
            self.PowerConsumed(data)
            try:
                self._socketClient.Transmit(data,port)
            except ConnectionRefusedError:
                self._broadCastingNodes -= self._broadCastingNodes
                print("failed on port "+str(port))

        if self._broadCastingNodes == 0:
            pass
        self._broadCasting = False
