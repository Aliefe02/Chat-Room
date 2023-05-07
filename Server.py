import socket
import threading

FORMAT = 'utf-8'
HEADER = 64
PORT = 4321
SERVER = 'localhost'
ADDR = (SERVER, PORT)
ClientList = []
ClientHandlerList = []

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def ConnectionHandler():
    global ClientList
    i = 0
    while True:
        server.listen()
        conn, addr = server.accept()
        ClientList.append(conn)
        print(f"[SERVER] NEW CONNECTION -> {addr} connected.")
        ClientHandlerList.append( threading.Thread(target=ClientHandler,args=(conn,addr)))
        ClientHandlerList[i].start()
        i += 1 

def ClientHandler(conn,addr):
    while True:
        try:
            msgLength = conn.recv(HEADER)
            msg = conn.recv(int(msgLength.decode(FORMAT)))
            for client in ClientList:
                if client != conn:
                    client.send(msgLength)
                    client.send(msg)
        except:
            print("[SERVER] ERROR SENDING MESSAGE")
            print(f"    {addr} -> "+msg.decode(FORMAT))


print("[SERVER] READY")
ConnectionHandler()