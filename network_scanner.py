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

    answered_packets_list = scapy.srp(arp_broadcast_rqst, timeout = 1, verbose= False)[0]
        
    devices_list = []
    #iterating over answered packets list and printing packet source(psrc) and hardware source(hwsrc) which are ip add and mac add respectively
    for packets in answered_packets_list:
        devices_id = {"ip": packets[1].psrc, "mac": packets[1].hwsrc}
        devices_list.append(devices_id)
    return devices_list
        

def print_result(nested_list):
    print("\n[+] " + str(len(nested_list)) + " Devices detected")
    print("---------------------------------------------")
    print("IP Address\t MAC Address")
    for device in nested_list:
        print(device["ip"] + "\t " + device["mac"])

range = str(get_args())
scan_result = scan(range)
print_result(scan_result)
