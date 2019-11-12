from Helper.JsonHandler import JsonHandler

class MicroController (object) : 
    
    characteristicsPath = "Characteristics/MicroController.json"
    _inputVoltage = 0
    _coreCurrent = 0

    def __init__ (self,inputVoltage) :
        self.jsonHandler = JsonHandler()
        self.ControllerChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self._inputVoltage = inputVoltage
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Run']

 
    def TurnOn(self) :
        self.ToActiveMode()

    def TurnOff(self):
        #updatePower
        pass   
    
    def ToActiveMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Run']

    def ToIdleMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Idle']

    def ToSleepMode(self):
        self._coreCurrent = self.ControllerChar['Current']['Mode']['Sleep']

    def I2CRead(self):
        Temp = 12
        self.I2CPowerConsumed()
        return Temp

    def I2CWrite(self):
        self.I2CPowerConsumed()

    def I2CPowerConsumed(self):
        time = (self.ControllerChar['BitSize'] / self.ControllerChar['BitRate'])/3600 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self._coreCurrent 
        return power
    