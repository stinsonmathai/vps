'''import json

with open("test.json") as config_file:
    config_data = json.load(config_file)

print (config_data['image_info']['test_image_url'])


from gtts import gTTS
tts = gTTS('hello', lang='en')
tts.save('hello.mp3')

import paramiko

ip='192.168.1.18'
port=22
username='pi'
password='4nosnits'

cmd='ls -la'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password)
stdin, stdout, stderr = ssh.exec_command(cmd)
outlines=stdout.readlines()
resp=''.join(outlines)
print(resp)


cmd2 = 'raspistill -o test234.jpg'
stdin, stdout, stderr = ssh.exec_command('cd imageCaptures/;raspistill -o rohit-pic.jpg')
outlines=stdout.readlines()
resp=''.join(outlines)
print(resp)

print('3 command !!!!!!!!!')
print(" ")

cmd = 'ls'
stdin, stdout, stderr = ssh.exec_command(cmd)
outlines=stdout.readlines()
resp=''.join(outlines)
print(resp)



from scp import SCPClient


# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())

scp.get('/home/pi/imageCaptures/rohit-pic.jpg')

scp.close()

ssh.close()'''

from tkinter import *
import tkinter as tk

class vspGUI:


    def __init__(self, master): # master is the root window that we will pass from the main program
        '''
        :param master:
        '''
        self.master = master
        master.title("Visual Positioning System")
        #master.geometry("500x300")

    def placeButtons(self, master):

        h = 5
        w = 5
        img = tk.PhotoImage(file="/Users/stinsonmathai/Documents/Stin-Work/Programming/Projects/28/graphics/man.gif")
        img = img.subsample(5)
        self.start_btn = tk.Button(master, width=w, height=h,command=lambda c=0: self.statusUpdate("we have started......."))
        self.start_btn.grid(row=1, column=1)
        self.start_btn.configure(text="START", fg="dark green")
        #todo: add the function for on click

        self.quit_btn = tk.Button(master, width=w, height=h, command=master.quit)
        self.quit_btn.grid(row=1, column=10)
        self.quit_btn.configure(text="QUIT", fg="dark green")
        # todo: add the function for on click

        self.picture_taken_label = tk.Label(master,image=img)
        self.picture_taken_label.grid(row=10, column=3)
        self.picture_taken_label = img
        # todo: add the function for on click

        self.picture_taken_description = tk.Label(master,text="picture taken")
        self.picture_taken_description.grid(row=12, column=3)
        # todo: add the function for on click

        self.x =StringVar()
        self.status_label = tk.Label(master,background='#4D4D4D',textvariable=self.x,bd=1,relief=SUNKEN,anchor=W)
        self.status_label.grid(row=35, column=0, columnspan=40, sticky=W+E)
        # todo: add the function for on click


    #TODO need to work on the status bar code below.
        '''self.button_list[]
        self.button_list[] = self.status_label'''

    def statusUpdate(self, status_text):
        self.x.set(status_text)

    def simplefunc(self):
        print("THIS WAS CALLED")




# Main function
#creating the GUI
root = Tk()
my_gui = vpsGUI(root)
my_gui.placeButtons(root)

my_gui.statusUpdate("changing labels")

root.mainloop()

