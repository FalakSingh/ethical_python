import subprocess
import argparse
import re 



def get_args():
    #making a variable for argparse object
    parser = argparse.ArgumentParser()

    #adding options/arguments for parser (dest defines the name of variable in which the arguments will be stored )
    parser.add_argument("-i","--interface", dest="interface", help="-i or --interface for Interface")
    parser.add_argument("-m", "--mac", dest= "new_mac", help="-m or --mac for New MAC")
    arguments =  parser.parse_args()
    #conditional statement to check if arguments are provided
    if not arguments.interface:
        print("[-] Please provide an Interface use -h or --help for info")
        exit()
    elif not arguments.new_mac:
        print("[-] Please provide a New MAC use -h or --help for info")
        exit()
    return arguments


def search_mac(interface):
    #storing ifconfig result in a variable
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    #searching for mac add string
    mac_add = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w" , str(ifconfig_result))
    if not mac_add:
        print("[-]Please provide with a Valid Interface")
        exit()
    return mac_add.group(0)


def mac_changer(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac ])
    subprocess.call(["ifconfig", interface, "up"])

    #checking if the mac was changed or not
    mac_check = search_mac(interface)
    if mac_check == new_mac:
        print("[+] MAC Successfully changed to:", mac_check)
    else:
        print("[-] MAC could not be changed") 
   

def main_process():

    #storing arguments returned by func in a variable
    arguments = get_args()

    #mac_add in variable arguments save values in variables
    mac_add_result = search_mac(arguments.interface)
    
    print ("[+] Current MAC Address:", mac_add_result)

    mac_changer(arguments.interface, arguments.new_mac)

main_process()