from Component.Helper.JsonHandler import JsonHandler
import datetime

class Battery (object) : 
    
    logPath = "Characteristics/BatteryLog.json"

    def __init__ (self,currentBatteryPower) : 
        self._currentBatteryPower = currentBatteryPower
        self.jsonHandler = JsonHandler()
        self.BatteryLog = self.jsonHandler.LoadJson(self.logPath)
        self._logs = self.BatteryLog['Log']
        
    def __del__ (self):
        self.BatteryLog['Log'] = self._logs
        self.jsonHandler.WriteJson(self.logPath,self.BatteryLog)

    def Discharging(self,**kwargs):
        powerDischarged = kwargs.get('powerDischarged')
        self._currentBatteryPower = self._currentBatteryPower - powerDischarged
        log = {'CurrentPower' : self._currentBatteryPower, 
                'PowerConsumed' : powerDischarged,
                'Reason' : kwargs.get('reason'),
                'TimeStamp' : (datetime.datetime.now()).strftime('%m/%d/%Y %I:%M:%S %p') }
        self._logs.append(log)

    def Charging(self,**kwargs):
        powerCharging = kwargs.get('powerDischarged')
        self._currentBatteryPower = self._currentBatteryPower + powerCharging
            
    def GetCurrentCharge(self):
        return self._currentBatteryPower