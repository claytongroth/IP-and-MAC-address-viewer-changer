import Tkinter as tk
import tkMessageBox
import socket
import random
import subprocess


from getmac import getmac
from subprocess import Popen, PIPE
from random import seed
from random import randint
from Tkinter import *

#master = Tk()

ifaces = ''' ifconfig | awk -F':'  '/^[^ ]*: / && $1 != "lo" {print $1}' | tr '\n' ',' '''
stdout = Popen(ifaces, shell=True, stdout=PIPE).stdout
output = stdout.read()
interfaces = output.split(",")[:-1]
interface = interfaces[0]




def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def ip():
    hostname = socket.gethostname()
    ip_add = socket.gethostbyname(hostname)
    tkMessageBox.showinfo("IP Address", ip_add)

def mac():
    mac_add = getmac.get_mac_address()
    tkMessageBox.showinfo("MAC Address", mac_add)

def newMac():
    # change here...
    inter = variable.get()
    new_MAC_address = rand_mac()
    print ("newMac fired with", str(inter), new_MAC_address)

    subprocess.call(["ifconfig", str(inter), "down"])
    subprocess.call(["ifconfig", str(inter), "hw", "ether", str(new_MAC_address)])
    subprocess.call(["ifconfig", str(inter), "up"])
    _mac_add = getmac.get_mac_address()
    tkMessageBox.showinfo("New MAC Address", _mac_add)

wind = tk.Tk()
wind.config(bg="#F1C40F")
wind.title("Get/Change Your IP and Mac Address")

variable = StringVar(wind)
variable.set(interface) # default value

def callback(*args):
    print ("value changed to", variable.get())

variable.trace("w", callback)

ip_button = tk.Button(wind, text="Show IP Address", bg ="#000000", fg="#F1C40F", font=("consolas", 16, "bold"), command=ip )
ip_button.pack()

mac_button = tk.Button(wind, text="Show MAC Address", bg="#000000", fg="#F1C40F",font=("consolas", 16, "bold"),command=mac)
mac_button.pack()

newMac_button = tk.Button(wind, text="Get New MAC Address", bg="#000000", fg="#F1C40F",font=("consolas", 16, "bold"),command=newMac)
newMac_button.pack()

label = Label(wind, text='Device to Change:')
label.pack(side="left")

w = OptionMenu(wind, variable, *interfaces)
w.pack()

mainloop()

wind.mainloop()