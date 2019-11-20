import paho.mqtt.client as publisher
import socket

class MqttPublisher (object):

    host = socket.gethostbyname(socket.gethostname())
    port = 1883

    def __init__(self,id_,topic):
        self._clientId = id_
        self._publishingTopic = topic

    def Publish(self,data,topic):
        _topic = self._publishingTopic + topic
        self._client = publisher.Client(self._clientId)
        self._client.connect(self.host,self.port)
        self._client.publish(topic,data)
        self._client.disconnect()
        

    