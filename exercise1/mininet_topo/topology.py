#!/usr/bin/python

import sys
import time
import os, glob

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import RemoteController, OVSSwitch

filename1="./topology_test_menu"


def clearTempHTTP():
    for filename in glob.glob("./index.html*"):        #DELETE HTML TEMPS FROM CURL
        os.remove(filename)

def myPing(source,destination):
    x = source.cmd("ping -c 2 " + str(destination.IP()))  
    time.sleep(0.5)
    return x   

def success(source,destination,protocol):
    print(" %s -> %s : connected with %s" %
                          (str(source.IP()), str(destination.IP()), str(protocol)))      

def fail(source,destination,protocol):
    print(" %s -> %s : not connected with %s" %
                          (str(source.IP()), str(destination.IP()), str(protocol)))        

def fromto():
    print("|   from   |    to    |")                                           


sentinel=object()

def testICMP(hosts1,hosts2=sentinel):   #                                                           1-5
    if hosts2 is sentinel:
        hosts2 = hosts1
    fromto()    
    for h1 in hosts1:
        for h2 in hosts2:
            myPing(h1,h2)                                   
            if h1 != h2:
                x = myPing(h1,h2)                           
                if "time=" in x:
                    success(h1,h2,"ICMP")
                else:
                    fail(h1,h2,"ICMP")
    
                                  

def StestICMP(h1,h2):   #SINGLE TEST ICMP
    fromto()
    myPing(h1,h2)
    x = myPing(h1,h2)                           
    if "time=" in x:
        success(h1,h2,"ICMP")
    else:
        fail(h1,h2,"ICMP")    

def myHTTPserver(host):
    host.cmd("python -m SimpleHTTPServer 80 &")
    time.sleep(1)

def myHTTPclient(client,host):
    time.sleep(1)
    x = client.cmd("curl " + str(host.IP() + " 80 -m 2"))
    return x 

def testHTTP(hosts1,hosts2=sentinel):  #                                                           6-8 
    if hosts2 is sentinel:
        hosts2 = hosts1
    fromto()
    for h1 in hosts1:
        myHTTPserver(h1)
        for h2 in hosts2:
            if h1 != h2:
                x = myHTTPclient(h2,h1)
                if "<html>" in x:
                    success(h1,h2,"HTTP")
                else:
                    fail(h1,h2,"HTTP")
    if hosts1 != hosts2:
        fromto()
        for h2 in hosts2:
            myHTTPserver(h2)
            for h1 in hosts1:
                if h1 != h2:
                    x = myHTTPclient(h1,h2)
                    if "<html>" in x:
                        success(h2,h1,"HTTP")
                    else:
                        fail(h2,h1,"HTTP")
    
    # myHTTPserver(hosts1[0])
    # myHTTPclient(hosts2[0],hosts1[0]) ##TODO ALARM SimpleHTTPServer NOT REALLY SURE
    # fromto()
    # for h1 in clients:
    #     x = myHTTPclient(c1,hosts[whichhost])      
    #     if "<html>" in x:
    #         success(c1,hosts[whichhost],"HTTP")
    #     else:
    #         fail(c1,hosts[whichhost],"HTTP")
    #     clearTempHTTP()
        

def StestHTTP(c1,h1):  # SINGLE TEST HTTP
    myHTTPserver(h1)
    myHTTPclient(c1,h1) ##TODO ALARM SimpleHTTPServer NOT REALLY SURE
    fromto()
    x = myHTTPclient(c1,h1)      
    if "<html>" in x:
        success(c1,h1,"HTTP")
    else:
        fail(c1,h1,"HTTP")
    clearTempHTTP() 
    
    myHTTPserver(c1)
    myHTTPclient(h1,c1) ##TODO ALARM SimpleHTTPServer NOT REALLY SURE
    fromto()
    x = myHTTPclient(h1,c1)      
    if "<html>" in x:
        success(h1,c1,"HTTP")
    else:
        fail(h1,c1,"HTTP")
    clearTempHTTP()



def myTCPserver(host):
    host.cmd("iperf -s -p 5566 -i 1 & ")
    time.sleep(0.5)

def myTCPclient(client,host):
    x = client.cmd("iperf -c " + str(host.IP()) + " -t 1 -p 5566 ")
    time.sleep(0.1)
    return x

def testTCP(hosts1,hosts2=sentinel):   #    sentinel=object()                                                         9-13
    if hosts2 is sentinel:
        hosts2 = hosts1
    fromto()
    for h1 in hosts1:
        myTCPserver(h1)
        for h2 in hosts2:
            if h1 != h2:
                x = myTCPclient(h2,h1)
                if "connected" in x:
                    success(h1,h2,"TCP")
                else:
                    fail(h1,h2,"TCP")
    if hosts1 != hosts2:
        fromto()
        for h1 in hosts1:
            myTCPserver(h1)
            for h2 in hosts2:
                if h1 != h2:
                    x = myTCPclient(h2,h1)
                    if "connected" in x:
                        success(h2,h1,"TCP")
                    else:
                        fail(h2,h1,"TCP")

def StestTCP(h1,h2):    # SINGLE TEST TCP
    fromto()
    myTCPserver(h1)
    x = myTCPclient(h2,h1)
    if "connected" in x:
        success(h2,h1,"TCP")
    else:
        fail(h2,h1,"TCP")
    myTCPserver(h2)
    x = myTCPclient(h1,h2)
    if "connected" in x:
        success(h1,h2,"TCP")
    else:
        fail(h1,h2,"TCP")

def myUDPserver(host):
    host.cmd("iperf -s -p 5566 -u -i 1 &")
    time.sleep(0.1) #time.sleep(0.5)

def myUDPclient(client,host):
    x = client.cmd("iperf -c " + str(host.IP()) + " -u -t 2 -p 5566")
    time.sleep(0.1)
    return x

def testUDP(hosts1,hosts2=sentinel):   #        sentinel=object()                                                      13-18
    if hosts2 is sentinel:
        hosts2 = hosts1
        fromto()
    for h1 in hosts1:
        myUDPserver(h1)
        for h2 in hosts2:
            if h1 != h2:
                x = myUDPclient(h2,h1)
                if "connected" in x:
                    success(h2,h1,"UDP")
                else:
                    fail(h2,h1,"UDP")
    if hosts1 != hosts2:
        fromto()
        for h2 in hosts2:
            myUDPserver(h2)
            for h1 in hosts1:
                if h1 != h2:
                    x = myUDPclient(h1,h2)
                    if "connected" in x:
                        success(h1,h2,"UDP")
                    else:
                        fail(h1,h2,"UDP")

def StestUDP(h1,h2):    # SINGLE TEST UDP
    fromto()
    myUDPserver(h1)
    x = myUDPclient(h2,h1)
    if "connected" in x:
        success(h2,h1,"UDP")
    else:
        fail(h2,h1,"UDP")
    myUDPserver(h2)
    x = myUDPclient(h1,h2)
    if "connected" in x:
        success(h1,h2,"UDP")
    else:
        fail(h1,h2,"UDP")                        



def topology():

    if "--help" in sys.argv:    #   HELP
        print("\n[I] Help:\n\n --test  : Opens a menu with network tests\n")            #   CHECK NO FW  |  
        return
   

    total_switches = 2
    total_access_points = 1
    total_hosts = 5
    total_stations = 5

    switches = []
    accesspoints = []
    hosts = []
    stations = []
    businessHosts = []  # all hosts connected to switch 090
    clients = []  # all nodes except host4
    server = []
    internet = []

    net = Mininet_wifi(
        controller=lambda name: RemoteController(name, ip='10.0.2.15', port=6633),
        switch=lambda name, **kwargs: OVSSwitch(name, protocols="OpenFlow13", **kwargs),
        waitConnected=True
    )

    # net = Mininet_wifi()
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633 )    

    info("*** Creating nodes\n")

####  DISCLAIMER all node names are 0based but IPs and DPID are 1based  #####


    for i in range(total_switches):  # s0, s1       #switch IP start at 10.0.2.0 / switch MAC start at 00:00:00:00:00:20 / switch DPID start at 1
        print("Creating switch s" + str(i))
        thisip='10.0.2.'
        thisip+=str(i+1)
        thisip+='/8'
        thismac='00:00:00:00:00:2'
        thismac+=str(i+1)
        thisdpid='000000000000000'          ##START FROM 1 HEXADECIMAL
        thisdpid+=str(i+1)
        switches.append(net.addSwitch('s' + str(i) , ip=thisip , mac=thismac , dpid=thisdpid))

    for i in range(total_hosts):  # h0, h1 h2       #hostsudo ps IP start at 10.0.0.0 / hosts MAC start at 00:00:00:00:00:00
        print("Creating host h" + str(i))
        thisip='10.0.0.'
        thisip+=str(i+1)
        thisip+='/8'
        thismac='00:00:00:00:00:0'
        thismac+=str(i+1)
        hosts.append(net.addHost('h' + str(i) , ip=thisip , mac=thismac))

    for i in range(total_stations):  # s0 ... s5    #stations IP start at 10.0.1.0 / stations MAC start at 00:00:00:00:01:00
        print("Creating host sta" + str(i))
        thisip='10.0.1.'
        thisip+=str(i+1)
        thisip+='/8'
        thismac='00:00:00:00:00:1'
        thismac+=str(i+1)
        stations.append(net.addStation('sta' + str(i) , ip=thisip , mac=thismac ))              

    for i in range(total_access_points):  # ap0     #Access points IP start at 10.0.3.0 / Access points MAC start at 00:00:00:00:03:00 / Access points DPID starts at 101
        print("Creating access point ap" + str(i))
        thisip='10.0.3.'
        thisip+=str(i+1)
        thisip+='/8'
        thismac='00:00:00:00:00:3'
        thismac+=str(i+1)
        thisdpid='000000000000006'      ##START FROM 101 HEXADECIMAL
        thisdpid+=str(i+5)
        accesspoints.append(net.addAccessPoint(
            ('ap' + str(i)), ssid="ssid_" + str(i), mode="g", channel="5", client_isolation=True , ip=thisip , mac=thismac , dpid=thisdpid))   

    # info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    for sta in stations:
        net.addLink(sta, accesspoints[0])
        clients.append(sta)

    for i in range(1):
        server.append(hosts[3])

    for i in range(1):
        internet.append(hosts[4])

    for i in range(3):
        net.addLink(hosts[i], switches[0])
        businessHosts.append(hosts[i])
        clients.append(hosts[i])

    net.addLink(switches[0], switches[1])
    net.addLink(switches[1], accesspoints[0])

    net.addLink(hosts[3], switches[1])
    net.addLink(hosts[4], switches[1])

    clients.append(hosts[i])

    info("*** Starting network\n")
    net.build()
    c0.start()

    for ap in accesspoints:
        ap.start([c0])

    for s in switches:
        s.start([c0])

    # if '-v' not in sys.argv:
    #     ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,arp,in_port=1,'
    #             'actions=output:in_port,normal"')
    #     ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,icmp,in_port=1,'
    #             'actions=output:in_port,normal"')
    #     ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,udp,in_port=1,'
    #             'actions=output:in_port,normal"')
    #     ap1.cmd('ovs-ofctl add-flow ap1 "priority=0,tcp,in_port=1,'
    #             'actions=output:in_port,normal"')
          

    ### MENU    ######### 
          
       
    if "--test" in sys.argv:    
        while True:
            filee = open(filename1, "r")
            print(filee.read())
            line = raw_input("INPUT ('c' for CLI):")

            tokens = line.split(" ")

            x = tokens[0]

            if x == 'e' or x == "exit":
                break

            if x == "c":
                CLI(net)

            if x == "1":    #1  #ICMP BUSINESS<->BUSINESS    
                print("1)   Test with ICMP Connection between Business\n")
                testICMP(businessHosts)
            if x == "2":    #2  #ICMP CUSTOMERS<->CUSTOMERS  
                print("2)   Test with ICMP Connection between Customers\n")
                testICMP(stations)
            if x == "3":    #3  #ICMP BUSINESS<->CUSTOMERS 
                print("3)   Test with ICMP Connection between Business and Customers\n")
                testICMP(businessHosts,stations)
            if x == "4":    #4  #ICMP BUSINESS<->SERVER      
                print("4)   Test with ICMP Connection between Business and Server\n")
                testICMP(businessHosts,server)
            if x == "5":    #5  #ICMP CUSTOMERS<->SERVER
                print("5)   Test with ICMP Connection between Customers and Server\n")
                testICMP(stations,server)
            if x == "6":    #6  #HTTP BUSINESS<->INTERNET
                print("6)   Test with HTTP Connection between Business and Internet (host4)\n")
                testHTTP(businessHosts,internet)
            if x == "7":    #7  #HTTP CUSTOMERS<->INTERNET
                print("7)   Test with HTTP Connection between Customers and Internet (host4)\n")
                testHTTP(stations,internet)
            if x == "8":    #8  #HTTP SERVER<->INTERNET
                print("8)   Test with HTTP Connection between Server and Internet (host4)\n")
                testHTTP(server,internet)
            if x == "9":   #9  #TCP BUSINESS<->BUSINESS 
                print("9)   Test with TCP Connection between Business \n")
                testTCP(businessHosts)
            if x == "10":   #10  #TCP CUSTOMERS<->CUSTOMERS  
                print("10)   Test with TCP Connection between Customers \n")
                testTCP(stations)
            if x == "11":   #11  #TCP BUSINESS<->CUSTOMERS  
                print("11)   Test with TCP Connection between Business and Customers \n")
                testTCP(businessHosts,stations)
            if x == "12":   #12  #TCP BUSINESS<->SERVER   
                print("12)   Test with TCP Connection between Business and Server \n")
                testTCP(businessHosts,server)
            if x == "13":   #13  #TCP CUSTOMERS<->SERVER 
                print("13)   Test with TCP Connection between Customers and Server \n")
                testTCP(stations,server)
            if x == "14":   #14  #UDP BUSINESS<->BUSINESS 
                print("14)   Test with UDP Connection between Business \n")
                testUDP(businessHosts)
            if x == "15":   #15  #UDP CUSTOMERS<->CUSTOMERS 
                print("15)   Test with UDP Connection between Customers \n")
                testUDP(stations)
            if x == "16":   #16  #UDP BUSINESS<->CUSTOMERS   
                print("16)   Test with UDP Connection between Business and Customers \n")
                testUDP(businessHosts,stations)
            if x == "17":   #17  #UDP BUSINESS<->SERVER
                print("17)   Test with UDP Connection between Business and Server \n")
                testUDP(businessHosts,server)
            if x == "18":   #18  #UDP CUSTOMERS<->SERVER     
                print("18)   Test with UDP Connection between Customers and Server \n")
                testUDP(stations,server)
            if x == "19":   #19  #ICMP BUSINESS<->INTERNET
                print("19)   Test with ICMP Connection between Business and Internet \n")
                testICMP(businessHosts,internet)  
            if x == "20":   #20  #TCP BUSINESS<->INTERNET
                print("20)   Test with TCP Connection between Business and Internet \n")
                testTCP(businessHosts,internet) 
            if x == "21":   #21  #TCP CUSTOMERS<->INTERNET
                print("21)   Test with TCP Connection between Customers and Internet \n")
                testTCP(stations,internet)     
            if x == "22":   #22  #TCP SERVER<->INTERNET
                print("22)   Test with TCP Connection between Server and Internet \n")
                testTCP(server,internet)   
            if x == "23":   #23  # CUSTOMERS<->SERVER
                print("23)   Test all Connections between Customers and Server \n")
                testICMP(stations,server)
                testTCP(stations,server)
                testUDP(stations,server) 
                testHTTP(stations,server)        
            if x == "24":   #24  # BUSINESS<->BUSINESS
                print("24)   Test all Connections between Business hosts \n")
                testICMP(businessHosts)
                testTCP(businessHosts)
                testUDP(businessHosts) 
                testHTTP(businessHosts)    
        
    ### MENU    ######### 

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
