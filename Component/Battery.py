# Voltage * Amps * hours = Wh
from Helper.JsonHandler import JsonHandler

class Battery (object) : 
    
    characteristicsPath = "Characteristics/Battery.json"
    count = 1
    def __init__ (self) : 
        self.jsonHandler = JsonHandler()
        self.BatteryChar = self.jsonHandler.LoadJson(self.characteristicsPath)
        #battery power usually in mAh
        InitialState =  self.BatteryChar['InitialState']
        wattHr = InitialState['AmpHours'] * InitialState['Voltage'] * 1000
        self.BatteryChar['InitialState']['Power'] = wattHr
        self.BatteryChar['State']['Power'] = wattHr
        self.Discharging(257)
        
    def __del__ (self):
        self.jsonHandler.WriteJson(self.characteristicsPath,self.BatteryChar)

    def Discharging(self,powerDischarged):
        currentPower = self.BatteryChar['State']['Power']
        self.BatteryChar['State']['Power'] = currentPower - powerDischarged

    def Charging(self,powerCharging):
        currentPower = self.BatteryChar['State']['Power']
        self.BatteryChar['State']['Power'] = currentPower + powerCharging
        

        
if __name__ == "__main__":
    Battery()