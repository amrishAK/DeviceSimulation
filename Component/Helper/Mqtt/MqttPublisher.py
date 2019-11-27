import paho.mqtt.client as publisher
import socket

class MqttPublisher (object):

    host ='10.6.42.165'
    host1 ='10.6.45.78'
#socket.gethostbyname(socket.gethostname())
    port = 1883

    def __init__(self,id_,topic):
        self._clientId = id_
        self._publishingTopic = topic

    def Publish(self,data,topic):
        _topic = self._publishingTopic + topic
        self._client=self.createCLien(self.host)
        self._client.publish(_topic,data)
        self._client.disconnect()

    def createCLien(self,ip,isSecond = False):
        try:
            client = publisher.Client(self._clientId)
            client.connect(ip,self.port)
            return client
        except:
            if not isSecond:
                self.host,self.host1=self.host1,self.host
                return self.createCLien(self.host,True)



    