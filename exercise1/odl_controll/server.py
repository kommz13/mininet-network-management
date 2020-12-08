#!/usr/bin/python
import endpoints
import requests

_ip = ""
_port = ""
_username = ""
_password = ""
_headers = {'Content-Type': 'application/json',
            'Accept': 'application/json'}


def init(ip, port, username, password):
    global _ip, _port, _username, _password
    _ip = ip
    _port = port
    _username = username
    _password = password
    print("Initializing server with ip:%s and port:%s " % (ip, port))


def getTopology():
    global _ip, _port, _headers, _username, _password
    auth = (_username, _password)
    url = endpoints.getEndpoints()['topology']['url'] % (_ip, _port)
    print(url)

    response = requests.get(url, auth=auth,headers=_headers)
    data = "undefined"

    if response.status_code / 100 == 2:
        print("response status: %d " % response.status_code)
        data = response.text
        return (response.status_code, data)
    else:
        print("response status: %d " % response.status_code)
        print(response)
        exit(0)


    
