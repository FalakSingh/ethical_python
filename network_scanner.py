import scapy.all as scapy
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--range", dest = "ip_range", help= "-r or --range for providing ip range")
    args = parser.parse_args()

    return args.ip_range
    

def scan(ip):
    #creating arp and braodcast packets and giving arp packet ip range to send packets to
    arp_packet = scapy.ARP(pdst = ip)
    broadcast_packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")

    arp_broadcast_rqst = broadcast_packet/arp_packet

    answered_packets_list = scapy.srp(arp_broadcast_rqst, timeout = 1)[0]

    #iterating over answered packets list and printing packet source(psrc) and hardware source(hwsrc) which are ip add and mac add respectively
    for packets in answered_packets_list:
        print("[+] IP Address:", packets[1].psrc)
        print("[+] MAC Address:", packets[1].hwsrc)
        print("----------------------------------------------------")


range = str(get_args())
scan(range)