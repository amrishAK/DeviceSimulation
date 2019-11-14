from Helper.JsonHandler import JsonHandler

class Battery (object) : 
    
    characteristicsPath = "Characteristics/Battery.json"

    def __init__ (self) : 
        self.jsonHandler = JsonHandler()
        self.BatteryChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        self.InitialState()
        
    def __del__ (self):
        self.jsonHandler.WriteJson(self.characteristicsPath,self.BatteryChar)

    def InitialState(self):
        #battery power usually in mAh
        # Voltage * Amps * hours = Wh
        InitialState =  self.BatteryChar['InitialState']
        wattHr = InitialState['AmpHours'] * InitialState['Voltage']
        self.BatteryChar['InitialState']['Power'] = wattHr
        self.BatteryChar['State']['Power'] = wattHr

    def Discharging(self,**kwargs):
        powerDischarged = kwargs.get('powerDischarged')
        currentPower = self.BatteryChar['State']['Power']
        self.BatteryChar['State']['Power'] = currentPower - powerDischarged

    def Charging(self,**kwargs):
        powerCharging = kwargs.get('powerDischarged')
        currentPower = self.BatteryChar['State']['Power']
        self.BatteryChar['State']['Power'] = currentPower + powerCharging
        
    def GetOutputVoltage(self):
        return self.BatteryChar['InitialState']['Voltage']