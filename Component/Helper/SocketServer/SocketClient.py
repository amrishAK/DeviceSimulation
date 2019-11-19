import socket  

class SocketClient (object) :
    
    host = socket.gethostbyname(socket.gethostname())
    port = 63342   

    def Transmit(self,data):
        s = socket.socket() 
        s.connect((self.host,self.port))
        s.send(data.encode())
        s.close()


