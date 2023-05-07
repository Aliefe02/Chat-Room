import socket
import threading
 
FORMAT = 'utf-8'
HEADER = 64
NAME = input("Enter name > ")
SERVER = input('Enter server ip > ')
PORT = int(input('Enter server port > '))
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def recv():
    while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                print(msg)
        except Exception as e:
            if '[WinError 10054]' in str(e):
                print('[CONNECTION LOST!]')
            else:
                print(e)

def send(msg):
    try:
        msg = NAME + " -> " +msg
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
    except Exception as e:
        print(e)
        print('[ERROR SENDING MESSAGE!]')

def SendMsg():
    while True:
        send(input())

MessageSender = threading.Thread(target=SendMsg,args=())
MessageSender.start()

Receiver = threading.Thread(target=recv,args=())
Receiver.start()
