# MODULES

import requests

# CONSTS

DEFAULT_PORT = 8123
TOKEN_FILENAME = "token"

ENTITY_STATE_ENDPOINT = "/api/states/{}" # entity_id
SERVICE_ENDPOINT= "/api/services/{}/{}" # domain, service

# CLASS

class HomeAssistant():
    def __init__(self, address, port=consts.DEFAULT_PORT, ssl=False):
        self.address = address
        self.port = port
        self.url = address + ":" + str(port) 

        if ssl:
            self.url = "https://" + self.url
        else:
            self.url = "http://" + self.url

        self.token = None


    def GetHeaders(self):
        if not self.token:
            print("You have to set a token !")
            return None

        headers = {
            "Authorization": "Bearer " + self.token,
            "content-type": "application/json",
        }

        return headers

    def Post(self, endpoint, payload):
        url = self.url+endpoint
        response = requests.post(url, headers=self.GetHeaders(), json=payload)
        return response

    def Get(self, endpoint):
        url = self.url+endpoint
        response = requests.get(url, headers=self.GetHeaders())
        return response

    def GetEntityState(self, entity_id):
        req = self.Get(consts.ENTITY_STATE_ENDPOINT.format(entity_id))
        if req.status_code == 200:
            return req.json()
        else:
            print("Error during request. Status code:",req.status_code)
            return None
            
    def SetEntityState(self, entity_id, payload):
        req = self.Post(consts.ENTITY_STATE_ENDPOINT.format(entity_id),payload)
        if req.status_code == 200:
            return req.json()
        else:
            print("Error during request. Status code:",req.status_code)
            return None
            
    def CallService(self, domain, service, data):
        req = self.Post(consts.SERVICE_ENDPOINT.format(domain,service),data)
        if req.status_code == 200:
            return req.json()
            # The result will include any states that changed while the service was being executed, 
            # even if their change was the result of something else happening in the system.
        else:
            print("Error during request. Status code:",req.status_code)
            return None
            

    def SetTokenFromFile(self,filename):
        with open(filename,"r") as f:
            self.token = f.readline().strip()

    def SetToken(self, token):
        self.token = token
