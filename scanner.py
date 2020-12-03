#!/usr/bin/python3
import os
import logging
import logging.handlers
from logging.handlers import SysLogHandler
from scapy.all import sniff, Ether

# custom_action used by scapy.sniff to take action based on packet
def custom_action(packet):
    if packet[0].src in addressList:
         #TODO: still active
         return f"{packet[0].src}"

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
    myfilter = "arp"
    #populate addressList from sqlite3 or rest
    addressList = [
        "b8:27:eb:e4:13:ed",
    ]

    logger.debug("MyView: starting scanner")
    sniffed = sniff(iface=myinterface,prn=custom_action,filter=myfilter)
