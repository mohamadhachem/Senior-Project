import scapy.all as scapy
import socket
from datetime import datetime

def scan(ip):
    arp_req_frame = scapy.ARP(pdst = ip)

    broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
    
    result = []
    for i in range(0,len(answered_list)):
        client_dict = {"ip" : answered_list[i][1].psrc, "mac" : answered_list[i][1].hwsrc}
        result.append(client_dict)

    return result


def start(startip, endip):
    localip = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0] + '.'

    devices = []

    ip = scapy.conf.route.route("0.0.0.0")[2]
    devices.append(scan(ip))

    for i in range(startip,endip):
        ip = f'{localip}{i}'
        s = scan(ip)
        if not s == []:
            devices.append(s)

    date = datetime.now()
    date = f'{date.year}-{date.month}-{date.day} {date.hour}{date.minute}{date.second}'

    file = open(f'log_folder\\network_scan {date}.txt', 'w')

    for device in devices:
        file.write(f'Ip: {device[0]["ip"]}    Mac address: {device[0]["mac"]}\n')

    file.close()

    return devices
