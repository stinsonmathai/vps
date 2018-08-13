import http.client
import uuid
import base64
import json
from label_image_stin import *
from gtts import gTTS
import paramiko
import uuid
from scp import SCPClient
from tkinter import *
import tkinter as tk
import os
from PIL import Image, ImageTk



def readConfigFile(mode):
    # this function does the following:
    # 1. Opens the client or server config file
    # 2. reads the xml info
    # 3. returns the json data.

    if mode == "client":
        client_config_file = "/Users/stinsonmathai/programming/machineLearning/API-Server/vps-client-config.json"
        with open(client_config_file) as config_file_handle:
            config_data = json.load(config_file_handle)
        print("STATUS: Reading Client Config File")
        return config_data
    elif mode == "server":
        client_config_file = "/Users/stinsonmathai/programming/machineLearning/API-Server/vps-server-config.json"
        with open(client_config_file) as config_file_handle:
            config_data = json.load(config_file_handle)
        print("STATUS: Reading Server Config File")
        return config_data

def encodeFile(f_name):
    #this function does the following:
    # 1. gets the image from the filename provided
    # 2. encodes it to base 64
    # 3. returns the encoded data
    with open(f_name, "rb") as inputFile:
        encoded_input_file_data = base64.b64encode(inputFile.read())
    print("STATUS: Encoding the Image file to Base64 for Transmission from Client to Server")
    return encoded_input_file_data


def send_PUT_API(encodedImage,http_connection_socket):
    conn = http.client.HTTPConnection(http_connection_socket)
    conn.request("PUT", "/test", encodedImage)
    print("STATUS: Sending PUT Call")

    r1 = conn.getresponse()
    print("STATUS: Received Response from Server/APP")

    status = r1.status
    reason = r1.reason
    resp_body = r1.read()
    
    if status == 200:
        print (status,reason)
        resp_load = json.loads(resp_body)
        for key, value in resp_load.items():
            print(key, value)
        answer = "The Machine Guessed the image to be "+key+" with "+str(value)+"% confidence"
    else:
        print(status," - ", reason)
        answer = "There was an error"

    conn.close()
    return answer


def save_image(imagestring):
    config_data = readConfigFile("server")
    locationToSave = config_data['file_info']['location_to_save']
    unique_filename = str(uuid.uuid4())
    filetosave = locationToSave + unique_filename + ".jpg"
    with open(filetosave, "wb") as fh:
        fh.write(base64.decodebytes(imagestring))
        print("STATUS: Saving the image file from Client: ", filetosave)
    return filetosave


def find_best_guess(resp_json):
    resp_load = json.loads(resp_json)
    print("STATUS: Sorting for BEST GUESS from Machine Learning results")
    key_max = max(resp_load.keys(), key=(lambda k: resp_load[k]))
    #todo figure out how to read this above line.
    ret_json = {key_max: resp_load[key_max]}
    final_ret = json.dumps(ret_json)
    print("STATUS: BEST GUESS has been determined")
    return final_ret



class RequestClass:

    def on_put(self,req, resp):
        print("STATUS: Received PUT message from Client")
        body = req.stream.read()
        f_name = save_image(body)
        config_data = readConfigFile("server")
        mod_file = config_data['tensorflow_info']['mod_file']
        lab_file = config_data['tensorflow_info']['lab_file']
        print("STATUS: Determining POSSIBLE GUESSES using Machine Learning @Server")
        tresults, tlabels = stin(mod_file,lab_file,f_name)
        #todo: change the "stin" funcion above

        results = []
        results = [float(round((i*100),3)) for i in tresults]
        content=dict(zip(tlabels, results))
        resp_load = json.dumps(content)
        print("@SERVER: full response --> ",resp_load)
        best_guess = find_best_guess(resp_load)
        print("@SERVER: best guess -->", best_guess)
        resp.body = best_guess

def getRaspberryPiImage():
    # Get the image from raspbberry PI after loggin into it.
    print("STATUS: Getting Image from Raspberry PI")
    ip = '192.168.1.18'
    port = 22
    username = 'pi'
    password = '4nosnits'

    unique_filename = str(uuid.uuid4())
    unique_filename = unique_filename + ".jpg"

    cmd = 'cd imageCaptures/;raspistill -vf -hf -o ' + unique_filename

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    outlines = stdout.readlines()
    resp = ''.join(outlines)
    print(resp)

    # SCPCLient takes a paramiko transport as its only argument
    scp = SCPClient(ssh.get_transport())

    file_to_get = '/home/pi/imageCaptures/' + unique_filename
    scp.get(file_to_get)

    scp.close()
    ssh.close()
    return unique_filename


#todo add voice to text
'''def text_to_voice(info):
    tts = gTTS('hello', lang='en')
    tts.save('hello.mp3')
'''

class vpsGUI:

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
        size = 256, 256
        self.start_btn = tk.Button(master, width=w, height=h,command=lambda c=0: self.runClientSide(master))
        self.start_btn.grid(row=1, column=1)
        self.start_btn.configure(text="START", fg="dark green")


        self.quit_btn = tk.Button(master, width=w, height=h, command=master.quit)
        self.quit_btn.grid(row=1, column=10)
        self.quit_btn.configure(text="QUIT", fg="dark green")

        self.picture_taken_description = tk.Label(master,text="picture taken")
        self.picture_taken_description.grid(row=12, column=3)


        self.y = StringVar()
        self.final_response = tk.Label(master, background='#4D4D4D', textvariable=self.y, bd=1, relief=SUNKEN, anchor=W)
        self.final_response.grid(row=15, column=0, columnspan=40, sticky=W + E)


        self.x =StringVar()
        self.status_label = tk.Label(master,background='#4D4D4D',textvariable=self.x,bd=1,relief=SUNKEN,anchor=W)
        self.status_label.grid(row=25, column=0, columnspan=40, sticky=W+E)


    def statusUpdate(self, status_text):
        #Updates the status bar on the GUI.
        self.x.set(status_text)

    def responseUpdate(self, r_text):
        # Updates the RESPONSE bar on the GUI.
        self.y.set(r_text)

    def updateTestImage(self, file_path,master):
        #TODO: this config does not work for ImageTK  only for tk.  so jpg is not going to work
        #TODO: How do we delete a label and put a new one.
        #img = Image.open(file_path)
        #img = img.thumbnail((300,300), Image.ANTIALIAS)
        img = Image.open(file_path)
        dim = (400, 400)
        newimg = img.resize(dim)
        img = ImageTk.PhotoImage(newimg)
        self.picture_taken_label = tk.Label(master)
        self.picture_taken_label.grid(row=10, column=3)
        self.picture_taken_label.config(image=img)
        self.picture_taken_label = img


    def runClientSide(self,master):
        # Runs the Step for the Client side.
        # This is called when the START Button on the GUI is clicked.
        self.statusUpdate("client is now running....")
        captured_image_filename = getRaspberryPiImage()
        #captured_image_filename = "tulip.jpg"  # this is done for testing purpose from swiss alps
        client_config_data_json = readConfigFile("client")
        file_info = client_config_data_json['image_info']['test_image_url'] + captured_image_filename
        self.updateTestImage(file_info,master)
        encoded_data_for_transmission = encodeFile(file_info)
        answer = send_PUT_API(encoded_data_for_transmission,
                              client_config_data_json['http_info']['http_connection_socket'])
        print(answer)
        self.responseUpdate(answer)
