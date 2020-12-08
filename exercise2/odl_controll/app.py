#!/usr/bin/python

import requests
import json
import getopt
import sys
import signal
import time
import Firewall as server

filename2="./failover_flows_menu"

def f(signo, stack):
    server.cleanUp()
    exit(0)

def routeToServer(i):
    print(" >>> Routing to server %s" % i)

def autoMode():
    print("Auto mode started !!!")

    while True:
        print("Checking for online servers")
        time.sleep(10)
        break

    print("Auto mode finished !!!")


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

    signal.signal(signal.SIGINT, f)


    filee = open(filename2, "r")
    menu = filee.read()
    filee.close()

    while True:
        print(menu)
        x = raw_input("Type your command:")

        if x == 'e' or x == "exit":
            break

        if x == "1" or x == "2" or x == "3":
            routeToServer(x)
        if x == "4":
            autoMode()

        if x == 'h' or x == "help":
            print(menu)

        if x == 'c' or x == "clear":
            server.cleanUp()    


   
    server.cleanUp()


if __name__ == '__main__':
    application(sys.argv[1:])
