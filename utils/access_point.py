## TODO: getConnectedIPs func returns IP-List

import os
import subprocess
import random
import string
import uuid

ssid = "Plantomio Controller"
whitelist = ["5c:85:7e:b0:7d:33","5c:85:7e:b0:c2:dd"] #flowercare devices whitelisted
network_i="wlan0"

def create_hostapd_conf(ssid, password):
    hostapd_conf = f"""
interface={network_i}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=1
accept_mac_file=/etc/hostapd/hostapd.accept
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
    """
    with open('/etc/hostapd/hostapd.conf', 'w') as file:
        file.write(hostapd_conf)
    
def create_dnsmasq_conf():
    dhcp_host_conf = ""
    for i,mac in enumerate(whitelist):
        if i < 254:
            dhcp_host_conf = dhcp_host_conf+"\ndhcp-host="+ mac + ",192.168.150."+ str(i+2)

    dnsmasq_conf = f"""
interface={network_i}
dhcp-range=192.168.150.2,192.168.150.30,255.255.255.0,24h
    """
#evtl dhcp-range kicken
    print(dnsmasq_conf+dhcp_host_conf)
    with open('/etc/dnsmasq.conf', 'w') as file:
        file.write(dnsmasq_conf+dhcp_host_conf)

def configure_network():
    # Set up the network interface
    subprocess.run(['ifconfig', network_i, 'up'], check=True)
    subprocess.run(['ifconfig', network_i, '192.168.150.1'], check=True)
    subprocess.run(['systemctl', 'restart', 'hostapd'], check=True)
    subprocess.run(['systemctl', 'restart', 'dnsmasq'], check=True)


def create_mac_file (whitelist):
    os.makedirs("/etc/hostapd/", exist_ok=True)

    with open("/etc/hostapd/hostapd.accept", 'w') as file:
        for mac in whitelist:
            file.write(mac)

def start_access_point():   #reqirements: sudo apt-get install hostapd dnsmasq

    # own Mac-Address is used as seed for wifi-password
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    formatted_mac = ":".join(mac[i:i+2] for i in range(0, 12, 2))
    random.seed(formatted_mac)
    password = "".join(random.choices(string.printable, k=25))
    
    print(password)

    create_mac_file(whitelist) #only works on linux
    create_hostapd_conf(ssid, password) #only works on linux
    create_dnsmasq_conf()
    configure_network() #only works on linux
    print(f'Access Point {ssid} wurde erstellt.')

def getConnectedIPs():
    return ["192.168.188.151","192.168.188.152"]
