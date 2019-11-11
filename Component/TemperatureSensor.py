from Helper.JsonHandler import JsonHandler

class TemperatureSensor (object) :

    characteristicsPath = "Characteristics/Battery.json"
    _inputVoltage = 0
    _coreCurrent = 0

    def __init__(self,inputVoltage):
        self.jsonHandler = JsonHandler()
        self.SensorChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self._inputVoltage = inputVoltage
        self._coreCurrent = self.SensorChar['Current']['AciveMode']


    def TurnOn(self) :
        self.ToActiveMode()

    def TurnOff(self):
        #updatePower
        pass

    def ToActiveMode(self):
        self._coreCurrent = self.SensorChar['Current']['AciveMode']

    def ToShutdownMode(self):
        self._coreCurrent = self.SensorChar['Current']['ShutdownMode']

    def I2CRead(self):
        Temp = 12
        self.I2CPowerConsumed()
        return Temp

    def I2CWrite(self):
        self.I2CPowerConsumed()

    def I2CPowerConsumed(self):
        time = (self.SensorChar['BitSize'] / self.SensorChar['BitRate'])/3600 # bitrate is in seconds, convert it to hours
        power = time * self._inputVoltage * self._coreCurrent 
        return power