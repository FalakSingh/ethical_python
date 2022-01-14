import argparse
import scapy.all as scapy

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest= "interface", help="-i or --interface for specifying Interface")
    args = parser.parse_args()
    if not args.interface:
        print("Please provide an Interface -h or --help for more info")
        exit()
    return args
#Function to get MAC of the IP from which packets are being recieved
def get_mac(ip):
    arp_rqst_packet = scapy.ARP(pdst= ip)
    ether_packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_ether_packet = ether_packet/arp_rqst_packet
    answered_packets_list = scapy.srp(arp_ether_packet, verbose = False, timeout = 1)[0]
    mac_add = answered_packets_list[0][1].hwsrc
    return mac_add

#scapy sniff function
def sniff(interface):
    scapy.sniff(iface=interface, store= False, prn=sniffed_packet)

#Function to check if the MAC of IP is actually the real MAC 
def sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                print("[-] ARP Spoof Detected...!!!")
                print("This device [" + real_mac + "] is spoofed to be this [" + response_mac + "] device" )
                print("---------------------------------------------------------------------------------")
        except IndexError:
            pass


args = get_args()
sniff(args.interface)
