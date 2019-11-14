from Component.Helper.JsonHandler import JsonHandler
import datetime

class Battery (object) : 
    
    characteristicsPath = "Characteristics/Battery.json"

    def __init__ (self) : 
        self.jsonHandler = JsonHandler()
        self.BatteryChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self.InitialState()
        
    def __del__ (self):
        self.BatteryChar['Logs'] = self._logs
        self.jsonHandler.WriteJson(self.characteristicsPath,self.BatteryChar)

    def InitialState(self):
        #battery power usually in mAh
        # Voltage * Amps * hours = Wh
        InitialState =  self.BatteryChar['InitialState']
        wattHr = InitialState['AmpHours'] * InitialState['Voltage']
        self.BatteryChar['InitialState']['Power'] = wattHr
        self._logs = self.BatteryChar['Logs']

    def Discharging(self,**kwargs):
        powerDischarged = kwargs.get('powerDischarged')
        currentPower = self.BatteryChar['State']['Power']
        self.BatteryChar['State']['Power'] = currentPower - powerDischarged
        currentTimeStamp = datetime.datetime.now()
        date = currentTimeStamp.strftime('%m/%d/%Y') + " " + currentTimeStamp.strftime('%I:%M:%S %p') 
        log = {'Power' : self.BatteryChar['State']['Power'], 'Reason' : kwargs.get('reason'), 'TimeStamp' : date }
        self._logs.append(log)

    def Charging(self,**kwargs):
        powerCharging = kwargs.get('powerDischarged')
        currentPower = self.BatteryChar['State']['Power']
        self.BatteryChar['State']['Power'] = currentPower + powerCharging
        
    def GetOutputVoltage(self):
        return self.BatteryChar['InitialState']['Voltage']