import socket  
from Component.Handler.eventHook import EventHook
import threading

class SocketServer (object):
    port = 63342       
    host = socket.gethostbyname(socket.gethostname()) 
     
    _socketHandler = EventHook()
    _isSocketUp = False
    
    def __del__(self):
        if self._isSocketUp:
            self.SocketClosing()
        
    def SocketClosing(self):
        self.s.close()
        self._isSocketUp = False
        self.backgroundThread.join()

    def Setup(self):
        self.s = socket.socket()
        self.s.bind((self.host, self.port))         
        self.s.listen(5)
        self._isSocketUp = True
        self.backgroundThread = threading.Thread(target=self.Run, args=())
        self.backgroundThread.daemon = True
        self.backgroundThread.start()

    def Run(self): 
        while(self._isSocketUp):
            conn, _ = self.s.accept()  
            data=conn.recv(1024)
            data = data.decode()
            self._socketHandler.fire(data=data)
