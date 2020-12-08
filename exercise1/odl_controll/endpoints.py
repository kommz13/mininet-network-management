#!/usr/bin/python

endpoints = {
    'topology': {
        'url': "http://%s:%s/restconf/operational/network-topology:network-topology",
        'method': "GET"
    },
    'inventory': {
        'url': "http://%s:%s/restconf/operational/opendaylight-inventory:nodes",
        'method': "GET"
    },
    'flowdetails': {
        'url': "http://%s:%s/restconf/config/opendaylight-inventory:nodes/node/%s/table/%s/flow/%s",
        'method': "GET"
    },
    'addflow': {
        'url': "http://%s:%s/restconf/config/opendaylight-inventory:nodes/node/%s/table/%s/flow/%s",
        'method': "PUT"
    },
    'delflow': {
        'url': "http://%s:%s/restconf/config/opendaylight-inventory:nodes/node/%s/table/%s/flow/%s",
        'method': "DELETE"
    },   
    'flowconfig': {
        'url': "http://%s:%s/restconf/config/opendaylight-inventory:nodes/node/%s/table/%s",
        'method': "GET"
    },   
    'flowoperational': {
        'url': "http://%s:%s/restconf/operational/opendaylight-inventory:nodes/node/%s/table/%s",
        'method': "GET"
    }
}

def getEndpoints():
    return endpoints