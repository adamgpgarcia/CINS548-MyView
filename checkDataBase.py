#!/home/pi/Desktop/CINS548-MyView/bin/python

import requests
import json
from datetime import datetime, timedelta
from scapy.all import ARP, Ether, srp
import time

#scapy scan, target IP needs to be the IP of your local network router
def scanNetwork():
    target_ip = "192.168.19.235/24"
    arp =ARP(pdst=target_ip)
    ether=Ether(dst="ff:ff:ff:ff:ff:ff")
    packet= ether/arp
    result=srp(packet,timeout=5,verbose=0)[0]
    clients=[]
    for sent, received in result:
        clients.append({'ip':received.psrc, 'mac':received.hwsrc})

    return clients

#login/logout function takes a list of mac address from scapy scan, token needs to be replaced with a current token, create new user
def login_logout(tempMac):
    url = 'http://127.0.0.1:8000/viewuser';
    token = 'token a5285613f16973e082681053075be92f70eddaec'    
    headers = { 'Content-Type' : 'application/json', 'Authorization' : token }
    
    response = requests.get(url, headers=headers)
    loadedData = response.json()
    
    for x in loadedData:
        currentItemTime = datetime.strptime(x['lastLogin'],"%Y-%m-%dT%H:%M:%SZ")
        for y in tempMac:
            #login if mac address is in the scan list
            if y["mac"] == x["MacAdd"]: 
                if x['connect'] == False:
                    now=datetime.now() + timedelta(seconds=900)
                    currentUser = x['id'];
                    updatedUser = {
                        "username" : x['username'],
                        "MacAdd" : x['MacAdd'],
                        "url" : x['url'],
                        "connect" : True,
                        "lastLogin": now.strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                    url = 'http://127.0.0.1:8000/viewuser/' + str(x['id']);
    
                    response = requests.request("PUT", url, data=json.dumps(updatedUser), headers=headers)
                    print("Login: " + str(x['username']))
                    
                   
        if x['connect'] ==True and currentItemTime <= datetime.now():
                
            updatedUser = {
                "username" : x['username'],
                "MacAdd" : x['MacAdd'],
                "url" : x['url'],
                "connect" : False,
                "lastLogin": currentItemTime.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
               
            url = 'http://127.0.0.1:8000/viewuser/' + str(x['id']);
            response = requests.request("PUT", url, data=json.dumps(updatedUser), headers=headers)
            print("Logout: " + str(x['username']))
            
    
#main part of script timed while loop
while True:
    print("ScanStart")
    tempMac = scanNetwork()
    login_logout(tempMac)
    time.sleep(15)




























