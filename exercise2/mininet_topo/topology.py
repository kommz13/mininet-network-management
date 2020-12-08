#!/usr/bin/python

import sys
import time
import os
import glob

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import RemoteController, OVSSwitch

filename1 = "./topology_test_menu"


def clearTempHTTP():
    for filename in glob.glob("./index.html*"):  # DELETE HTML TEMPS FROM CURL
        os.remove(filename)


sentinel = object()


def initServer(host, id):
    print("Initializing server #%s " % str(id))
    r = host.cmd("cd webroot" + str(id))
    print("Initialization Response: %s" % r)


def startServer(host, id):
    print("Starting server #%s " % str(id))
    r = host.cmd(
        "python -m SimpleHTTPServer 12875 1> /dev/null 2> /dev/null %s &" % (str(id)))
    print("Start Response: %s" % r)


def stopServer(host, id):
    print("Stoping server #%s" % str(id))
    y = host.cmd(
        "ps -aef | grep SimpleHTTPServer | grep 12875 | grep %s$ | grep python | awk '{print $2}' | tail -1" % str(id))
    # x = host.cmd("kill `ps -aef | grep SimpleHTTPServer | grep 2 | grep python | awk '{print $2}'`")
    print("y = " + y)
    r = host.cmd("kill -9 %s " % y)
    print("Kill Response: %s" % r)


def curlServer(client, server):
    time.sleep(1)
    x = client.cmd("curl %s:12875 -m 2" % (server.IP()))
    print("Response is %s " % x)

def curlCluster(client):
    time.sleep(1)
    x = client.cmd("curl 10.0.1.1:12875 -m 2")
    print("Response is %s " % x)

def topology():
    total_switches = 1
    total_clients = 1
    total_servers = 3

    switches = []
    clients = []
    servers = []

    servers_running = []

    net = Mininet_wifi(
        controller=lambda name: RemoteController(
            name, ip='10.0.2.15', port=6633),
        switch=lambda name, **kwargs: OVSSwitch(
            name, protocols="OpenFlow13", **kwargs),
        waitConnected=True
    )

    # net = Mininet_wifi()
    c0 = net.addController(
        'c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # s0, s1       #switch IP start at 10.0.2.0 / switch MAC start at 00:00:00:00:00:20 / switch DPID start at 1
    for i in range(total_switches):
        print("Creating switch s" + str(i))
        thisip = '10.0.2.'
        thisip += str(i+1)
        thisip += '/8'
        thismac = '00:00:00:00:00:2'
        thismac += str(i+1)
        thisdpid = '000000000000000'  # START FROM 1 HEXADECIMAL
        thisdpid += str(i+1)
        switches.append(net.addSwitch(
            's' + str(i), ip=thisip, mac=thismac, dpid=thisdpid))

    # h0, h1 h2       #hostsudo ps IP start at 10.0.0.0 / hosts MAC start at 00:00:00:00:00:00
    for i in range(1, 1 + total_clients):
        print("Creating client h" + str(i))
        thisip = '10.0.0.'
        thisip += str(i)
        thisip += '/8'
        thismac = '00:00:00:00:00:0'
        thismac += str(i)
        clients.append(net.addHost('h' + str(i), ip=thisip, mac=thismac))

    # s0 ... s5    #stations IP start at 10.0.1.0 / stations MAC start at 00:00:00:00:01:00
    for i in range(1 + total_clients, 1 + total_clients + total_servers):
        print("Creating server h" + str(i))
        thisip = '10.0.1.'
        thisip += str(i)
        thisip += '/8'
        thismac = '00:00:00:00:00:1'
        thismac += str(i)
        servers.append(net.addHost('h' + str(i), ip=thisip, mac=thismac))

    # info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    for c in clients:
        net.addLink(c, switches[0])
    for srv in servers:
        net.addLink(srv, switches[0])

    # turn server online
    for i in range(0, total_servers):
        initServer(servers[i], i+2)
        startServer(servers[i], i+2)
        servers_running.append(True)

    info("*** Starting network\n")
    net.build()
    c0.start()

    for s in switches:
        s.start([c0])

    # menu:
    # 1. start server 2 (10.0.1.2)
    # 2. start server 3 (10.0.1.3)
    # 3. start server 4 (10.0.1.4)
    # 4. stop server 2 (10.0.1.2)
    # 5. stop server 3 (10.0.1.3)
    # 6. stop server 4 (10.0.1.4)
    # 7. curl to server 2 (10.0.1.2)
    # 8. curl to server 3 (10.0.1.3)
    # 9. curl to server 4 (10.0.1.4)
    # 10. curl cluster (10.0.1.5)

    while True:
        print("+-----------------------------------+")
        print("|  menu:                            |")

        if not servers_running[0]:
            print("|   1. start server 2 (10.0.1.2)    |")

        if not servers_running[1]:    
            print("|   2. start server 3 (10.0.1.3)    |")
        
        if not servers_running[2]:
            print("|   3. start server 4 (10.0.1.4)    |")

        if servers_running[0]:
            print("|   4. stop server 2 (10.0.1.2)     |")

        if servers_running[1]:
            print("|   5. stop server 3 (10.0.1.3)     |")

        if servers_running[2]:
            print("|   6. stop server 4 (10.0.1.4)     |")
            
        print("|   7. curl to server 2 (10.0.1.2)  |")
        print("|   8. curl to server 3 (10.0.1.3)  |")
        print("|   9. curl to server 4 (10.0.1.4)  |")
        print("|   10. curl cluster (10.0.1.1)     |")
        print("+-----------------------------------+")

        line = raw_input("INPUT ('c' for CLI):")

        tokens = line.split(" ")

        x = tokens[0]

        if x == 'e' or x == "exit":
            break

        if x == 'c':
            CLI(net)
        if x == "1":
            print("1)   start server 2 (10.0.1.2)\n")
            startServer(servers[0], 2)
            servers_running[0] = True
        if x == "2":
            print("2)   start server 3 (10.0.1.3)\n")
            startServer(servers[1], 3)
            servers_running[1] = True
        if x == "3":
            print("3)   start server 4 (10.0.1.4)\n")
            startServer(servers[2], 4)
            servers_running[2] = True
        if x == "4":
            print("4)   stop server 2 (10.0.1.2)\n")
            stopServer(servers[0], 2)
            servers_running[0] = False
        if x == "5":
            print("5)    stop server 3 (10.0.1.3)\n")
            stopServer(servers[1], 3)
            servers_running[1] = False
        if x == "6":
            print("6)    stop server 4 (10.0.1.4)\n")
            stopServer(servers[2], 4)
            servers_running[2] = False
        if x == "7":
            print("7)   curl to server 2 (10.0.1.2)\n")
            curlServer(clients[0], servers[0])
        if x == "8":
            print("8)   curl to server 3 (10.0.1.3)\n")
            curlServer(clients[0], servers[1])
        if x == "9":
            print("9)   curl to server 4 (10.0.1.4) \n")
            curlServer(clients[0], servers[2])
        if x == "10" or x == "0":
            print("10)  curl cluster (10.0.1.1) \n")
            curlCluster(clients[0])

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
