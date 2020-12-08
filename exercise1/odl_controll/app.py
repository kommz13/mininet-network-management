#!/usr/bin/python

import requests
import json
import getopt
import sys
import signal
import Firewall as server

filename2="./firewall_flows_menu"

def f(signo, stack):
    server.cleanUp()
    exit(0)

def application(argv):
    username = "admin"
    password = "admin"
    ip = "127.0.0.1"
    port = "8181"
    opts, args = getopt.getopt(argv, "p:i:d:", ["ip=", "port=", "debug"])
    debug = False

    for opt, arg in opts:
        if opt in ("-p", "--port"):
            port = arg
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-i", "--ip"):
            ip = arg


    print("Initializing application with arguments: ")
    print("\tUsername: %s " % username)
    print("\tPassword: %s " % password)
    print("\tServer socket: %s:%s " % (ip, port))
    print("")

    server.init(ip, port, username, password)

    if debug:
        status, data = server.getTopology()
        print("Status: " + str(status))
        print("Data  : " + str(data))

    # raw_input("press enter to activate firewall")

    signal.signal(signal.SIGINT, f)

    

    ids_per_case = {}

    flow_id = 1

    while True:
        filee = open(filename2, "r")
        print(filee.read())
        line = raw_input("Type your command:")

        tokens = line.split(" ")

        flow_id = flow_id +1

        x = tokens[0]
        y = tokens[1] if len(tokens) > 1 else None

        if x == 'e' or x == "exit":
            break

        if x == "on":    
            if y == "1":
                print("adding rules of case #1: Block ICMP on switch 1")
                status, data, topologyIdentity1 = server.addBlockAction(1, 0, 1, "ICMP")          
                if not ids_per_case.get("1"):
                    ids_per_case["1"] = []
                ids_per_case["1"].append(topologyIdentity1)
            
            if y == "2":
                print("adding rules of case #2: Block any TCP connection from 10.0.0.[1-3] to 10.0.0.5 on switch 1")
                status, data, topologyIdentity2 = server.addBlockAction(1, 0, 2, "TCP", "10.0.0.0/30", "10.0.0.5/32")                   
                if not ids_per_case.get("2"):
                    ids_per_case["2"] = []
                ids_per_case["2"].append(topologyIdentity2) 

            if y == "3":
                print("adding rules of case #3: Block any TCP connection from 10.0.1.[1-5] to 10.0.0.5 on switch 2")
                status, data, topologyIdentity3 = server.addBlockAction(2, 0, 3, "TCP", "10.0.1.0/29", "10.0.0.5/32")                   
                if not ids_per_case.get("3"):
                    ids_per_case["3"] = []
                ids_per_case["3"].append(topologyIdentity3)   

            if y == "4":
                print("adding rules of case #4: Block any TCP connection from 10.0.0.4 to 10.0.0.5 on switch 2")
                status, data, topologyIdentity4 = server.addBlockAction(2, 0, 4, "TCP", "10.0.0.4/32", "10.0.0.5/32")                   
                if not ids_per_case.get("4"):
                    ids_per_case["4"] = []
                ids_per_case["4"].append(topologyIdentity4)  

            if y == "5":
                print("adding rules of case #5: Block any ICMP connection from 10.0.0.[1-3] to 10.0.1.[1-5] on switch 1")
                status, data, topologyIdentity5 = server.addBlockAction(1, 0, 5, "ICMP", "10.0.0.0/30", "10.0.1.0/29")                   
                if not ids_per_case.get("5"):
                    ids_per_case["5"] = []
                ids_per_case["5"].append(topologyIdentity5)  

            if y == "6":
                print("adding rules of case #6: Block any UDP connection from 10.0.0.[1-3] to 10.0.1.[1-5] on switch 1")
                status, data, topologyIdentity6 = server.addBlockAction(1, 0, 6, "UDP", "10.0.0.0/30", "10.0.1.0/29",udp_src_port="5566", udp_dest_port ="5566")                   

                if not ids_per_case.get("6"):
                    ids_per_case["6"] = []
                ids_per_case["6"].append(topologyIdentity6) 

            if y == "7":
                print("adding rules of case #7: Block any connection from 10.0.1.[1-5] to further network on switch 1")
                status, data, topologyIdentity7 = server.addBlockAction(2, 0, 7, None, "10.0.1.0/29","10.0.0.4/32")                   

                if not ids_per_case.get("7"):
                    ids_per_case["7"] = []
                ids_per_case["7"].append(topologyIdentity7)  

            if y == "8":
                print("adding rules of case #8: Block any connection between business hosts on switch 1")
                status, data, topologyIdentity8 = server.addBlockAction(1, 0, 8, None, "10.0.0.0/30","10.0.0.0/30")                   

                if not ids_per_case.get("8"):
                    ids_per_case["8"] = []
                ids_per_case["8"].append(topologyIdentity8)      

        if x == "off":
            print("removing rules of case #" + y)
            for ti in ids_per_case[y]:
                server.removeAction(ti)            


        if x == 'h' or x == "help":
            filee = open(filename2, "r")
            print(filee.read())

        if x == 'c' or x == "clear":
            server.cleanUp()    

            


   
    server.cleanUp()


if __name__ == '__main__':
    application(sys.argv[1:])
