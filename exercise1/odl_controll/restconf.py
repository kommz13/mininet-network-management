#!/usr/bin/python
import endpoints
import json
import requests

PROTOCOL_MAP = {
    "ICMP" : "1",
    "TCP" : "6",
    "UDP" : "17"
}

class Credentials:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    def auth(self):
        return (self.username, self.password)
    def headers(self):
        return self.header
    def socket(self):
        return (self.ip, self.port)
    
class TopologyIdentity:
    def __init__(self, switch, table, id = 0):
        self.switch = switch
        self.table = str(table)
        self.id = str(id)
    def openFlowSwitch(self):
        return "openflow:" + str(self.switch)


def sendRequest(credentials, url, method, data = None):
    if method == "PUT":
        if data != None: 
            response = requests.put(url = url, auth=credentials.auth(),headers=credentials.headers(), data = data)
        else:
            response = requests.put(url = url, auth=credentials.auth(),headers=credentials.headers())

    if method == "DELETE":
        if data != None: 
            response = requests.delete(url = url, auth=credentials.auth(),headers=credentials.headers(), data = data)
        else: 
            response = requests.delete(url = url, auth=credentials.auth(),headers=credentials.headers())

    if method == "GET":
        if data != None: 
            response = requests.get(url = url, auth=credentials.auth(),headers=credentials.headers(), data = data)
        else:
            response = requests.get(url = url, auth=credentials.auth(),headers=credentials.headers())

    if response.status_code / 100 == 2:
        print("response status: %d " % response.status_code)
        data = response.text
        return (response.status_code, data)
    else:
        print("response status: %d " % response.status_code)
        print(response.text)
        exit(0)



def getTopology(credentials):
    url = endpoints.getEndpoints()['topology']['url'] % credentials.socket()
    print(url)

    return sendRequest(credentials=credentials, url=url, method= endpoints.getEndpoints()['topology']['method'])

def getInventory(credentials):
    url = endpoints.getEndpoints()['inventory']['url'] % credentials.socket()
    print(url)

    return sendRequest(credentials=credentials, url=url, method = endpoints.getEndpoints()['inventory']['method'])    
   

def getFlowDetails(credentials, topologyIdentity):
    t1 = credentials.socket()
    t2 = (topologyIdentity.openFlowSwitch(), topologyIdentity.table, topologyIdentity.id)
    t = t1 + t2

    url = endpoints.getEndpoints()['flowdetails']['url'] % t
  
    print(url)

    return sendRequest(credentials=credentials, url=url, method = endpoints.getEndpoints()['flowdetails']['method'])
   

def addFlow(credentials, topologyIdentity, data):
    t1 = credentials.socket()
    t2 = (topologyIdentity.openFlowSwitch(), topologyIdentity.table, topologyIdentity.id)
    t = t1 + t2

    print(t)

    url = endpoints.getEndpoints()['addflow']['url'] % t
  
    print(url)

    payload = json.dumps(data)

    print(payload)

    return sendRequest(credentials=credentials, url=url, method = endpoints.getEndpoints()['addflow']['method'], data = payload)
   

def deleteFlow(credentials, topologyIdentity):
    t1 = credentials.socket()
    t2 = (topologyIdentity.openFlowSwitch(), topologyIdentity.table, topologyIdentity.id)
    t = t1 + t2

    url = endpoints.getEndpoints()['delflow']['url'] % t
  
    print(url)

    return sendRequest(credentials=credentials, url=url, method = endpoints.getEndpoints()['delflow']['method'])

def getFlowConfig(credentials, topologyIdentity):
    t1 = credentials.socket()
    t2 = (topologyIdentity.openFlowSwitch(), topologyIdentity.table)
    t = t1 + t2

    url = endpoints.getEndpoints()['flowconfig']['url'] % t
  
    print(url)

    return sendRequest(credentials=credentials, url=url, method = endpoints.getEndpoints()['flowconfig']['method'])


def getFlowOperational(credentials, topologyIdentity):
    t1 = credentials.socket()
    t2 = (topologyIdentity.openFlowSwitch(), topologyIdentity.table)
    t = t1 + t2

    url = endpoints.getEndpoints()['flowoperational']['url'] % t
  
    print(url)

    return sendRequest(credentials=credentials, url=url, method = endpoints.getEndpoints()['flowoperational']['method'])

