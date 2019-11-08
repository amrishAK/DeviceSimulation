import json

class JsonHandler (object):
    def LoadJson(self,path):
        with open(path, 'r') as file:
            return json.loads(file.read())

    def WriteJson(self,path,data):
        with open(path, 'w') as file:
            json.dump(data,file,sort_keys=True,indent=4)