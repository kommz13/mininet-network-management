#!/usr/bin/python
import endpoints
import requests
import json
import restconf

_ip = ""
_port = ""
_username = ""
_password = ""
_credentials=  {}
_ids = []

def init(ip, port, username, password):
    global _ip, _port, _username, _password, _credentials
    _ip = ip
    _port = port
    _username = username
    _password = password
    _credentials = restconf.Credentials(ip, port, username, password )
    
    print("Initializing server with ip:%s and port:%s " % (ip, port))

def cleanUp():  
    global _ids  
    print("\nCleaning server with ip:%s and port:%s " % (_ip, _port))
    for ti in _ids:
        print("Deleting identity: ")
        print(ti)
        restconf.deleteFlow(_credentials, ti)
    _ids = []

def getTopology():
    return restconf.getTopology(_credentials)


def removeAction(topologyIdentity):
    restconf.deleteFlow(_credentials, topologyIdentity)
    _ids.remove(topologyIdentity)


def addBlockAction(switch, table, flow_id, protocol = None, ip4_src = None, ip4_dest = None, tcp_src_port = None, tcp_dest_port = None, udp_src_port = None, udp_dest_port = None, mac_src = None, mac_dest = None, in_port = None, out_port = None):
    data = {}

    data["flow"] = {}
    data["flow"]["id"] = flow_id
    data["flow"]["table_id"] = table
    data["flow"]["flow-name"] = "name_" + str(flow_id)
    data["flow"]["priority"] = "1000"
    data["flow"]["hard-timeout"] = 0
    data["flow"]["idle-timeout"] = 0
    data["flow"]["cookie"]  = 0
    data["flow"]["instructions"]  = {}
    data["flow"]["instructions"]["instruction"] = { }
    data["flow"]["instructions"]["instruction"]["order"]  = 0
    data["flow"]["instructions"]["instruction"]["apply-actions"]  = {}
    data["flow"]["instructions"]["instruction"]["apply-actions"]["action"]  = {}
    data["flow"]["instructions"]["instruction"]["apply-actions"]["action"]["order"]  = 0
    data["flow"]["instructions"]["instruction"]["apply-actions"]["action"]["drop-action"]  = {}
    data["flow"]["match"] = {}
    data["flow"]["match"]["ethernet-match"] = {}
    data["flow"]["match"]["ethernet-match"]["ethernet-type"] = {}
    data["flow"]["match"]["ethernet-match"]["ethernet-type"]["type"] = "2048"

    if protocol != None:
        data["flow"]["match"]["ip-match"] = {}
        data["flow"]["match"]["ip-match"]["ip-protocol"] = restconf.PROTOCOL_MAP[protocol]

    if mac_src != None:
        data["flow"]["match"]["ethernet-match"]["ethernet-source"] = {}
        data["flow"]["match"]["ethernet-match"]["ethernet-source"]["address"] = mac_src

    if mac_dest != None:
        data["flow"]["match"]["ethernet-match"]["ethernet-destination"] = {}
        data["flow"]["match"]["ethernet-match"]["ethernet-destination"]["address"] = mac_dest
        

    if ip4_src != None:
         data["flow"]["match"]["ipv4-source"] = ip4_src

    if ip4_dest != None:
         data["flow"]["match"]["ipv4-destination"] = ip4_dest

    if tcp_src_port != None:
        data["flow"]["match"]["tcp-source-port"] = tcp_src_port

    if tcp_dest_port != None:
        data["flow"]["match"]["tcp-destination-port"] = tcp_dest_port

    if udp_src_port != None:
        data["flow"]["match"]["udp-source-port"] = udp_src_port

    if udp_dest_port != None:
        data["flow"]["match"]["udp-destination-port"] = udp_dest_port

    if in_port != None:
        data["flow"]["match"]["in-port"] = in_port

    if out_port != None:
        data["flow"]["match"]["out_port"] = out_port
   


    topologyIdentity = restconf.TopologyIdentity(switch, 0, flow_id)

    res = restconf.addFlow(_credentials, topologyIdentity, data)

    _ids.append(topologyIdentity)

    t1 = res
    t2 = (topologyIdentity,)
    t = t1 + t2

    return t

def addAllowAction(switch, table, flow_id, protocol = None, ip4_src = None, ip4_dest = None, tcp_src_port = None, tcp_dest_port = None, udp_src_port = None, udp_dest_port = None, mac_src = None, mac_dest = None, in_port = None, out_port = None):
    global _ids
    data = {}

    data["flow"] = {}
    data["flow"]["id"] = flow_id
    data["flow"]["table_id"] = table
    data["flow"]["flow-name"] = "name_" + str(flow_id)
    data["flow"]["priority"] = "1000"
    data["flow"]["hard-timeout"] = 0
    data["flow"]["idle-timeout"] = 0
    data["flow"]["cookie"]  = 0
    data["flow"]["instructions"]  = {}
    data["flow"]["instructions"]["instruction"] = { }
    data["flow"]["instructions"]["instruction"]["order"]  = 0
    data["flow"]["instructions"]["instruction"]["apply-actions"]  = {}
    data["flow"]["instructions"]["instruction"]["apply-actions"]["action"]  = {}
    data["flow"]["instructions"]["instruction"]["apply-actions"]["action"]["order"]  = 0
    data["flow"]["instructions"]["instruction"]["apply-actions"]["action"]["output-action"]  = {}
    data["flow"]["instructions"]["instruction"]["apply-actions"]["action"]["output-action"]["output-node-connector"] = "NORMAL"
    data["flow"]["match"] = {}
    data["flow"]["match"]["ethernet-match"] = {}
    data["flow"]["match"]["ethernet-match"]["ethernet-type"] = {}
    data["flow"]["match"]["ethernet-match"]["ethernet-type"]["type"] = "2048"

    if protocol != None:
        data["flow"]["match"]["ip-match"] = {}
        data["flow"]["match"]["ip-match"]["ip-protocol"] = restconf.PROTOCOL_MAP[protocol]

    if mac_src != None:
        data["flow"]["match"]["ethernet-match"]["ethernet-source"] = {}
        data["flow"]["match"]["ethernet-match"]["ethernet-source"]["address"] = mac_src

    if mac_dest != None:
        data["flow"]["match"]["ethernet-match"]["ethernet-destination"] = {}
        data["flow"]["match"]["ethernet-match"]["ethernet-destination"]["address"] = mac_dest
        

    if ip4_src != None:
         data["flow"]["match"]["ipv4-source"] = ip4_src

    if ip4_dest != None:
         data["flow"]["match"]["ipv4-destination"] = ip4_dest

    if tcp_src_port != None:
        data["flow"]["match"]["tcp-source-port"] = tcp_src_port

    if tcp_dest_port != None:
        data["flow"]["match"]["tcp-destination-port"] = tcp_dest_port

    if udp_src_port != None:
        data["flow"]["match"]["udp-source-port"] = udp_src_port

    if udp_dest_port != None:
        data["flow"]["match"]["udp-destination-port"] = udp_dest_port

    if in_port != None:
        data["flow"]["match"]["in-port"] = in_port

    if out_port != None:
        data["flow"]["match"]["out_port"] = out_port
   


    topologyIdentity = restconf.TopologyIdentity(switch, 0, flow_id)

    res = restconf.addFlow(_credentials, topologyIdentity, data)

    _ids.append(topologyIdentity)

    t1 = res
    t2 = (topologyIdentity,)
    t = t1 + t2
    return t

