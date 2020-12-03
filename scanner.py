#!/usr/bin/python3
import os
import logging
import logging.handlers
from logging.handlers import SysLogHandler
from scapy.all import sniff

# custom_action used by scapy.sniff to take action based on packet
def custom_action(packet):
    for p in packet:
        if p[1].src in addressList:
            #TODO: still active
            print("still active")

    #end custom_action

if __name__ == "__main__":
    # Instantiate logger
    # adapted from https://www.kite.com/python/docs/logging.handlers.SysLogHandler
    logger = logging.getLogger('mylogger')
    #logger.setLevel(logging.ERROR)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(facility=SysLogHandler.LOG_DAEMON, address='/dev/log')
    logger.addHandler(handler)
    myinterface = "wlan0"
    myfilter = "tcp"
    #populate addressList from sqlite3 or rest
    addressList = [
        "10.0.0.232",
    ]

    logger.debug("MyView: starting scanner")
    sniffed = sniff(iface=myinterface,prn=custom_action,filter=myfilter)
