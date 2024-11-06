import socket as skt
import threading as t
class server:
    def __init__(self, port: int, backlog: int = 1) -> None:
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.ip = skt.gethostname()+".local"
        self.port = port
        self.socket.bind((self.ip, port))
        print(f"Server created with ip {self.ip}, and port {port}")
        self.clientthreads = []
        self.messages = []
        self.maxBacklog = backlog
    def startListening(self, numclients: int):
        self.numconnect = 0
        self.listenThread = t.Thread(None, self.runServer, "Listening Thread", (numclients, )).start()
    def runServer(self, numclients):
        self.socket.listen(self.maxBacklog)
        while True:
            if self.numconnect<numclients:
                print(f"Listening on {self.ip}:{self.port}")
                client_socket, client_address = self.socket.accept()
                print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
                t.Thread(None, self.Coms, f"{client_address[0]}:{client_address[1]}", (client_socket, client_address, False)).start()
                self.numconnect+=1
            else:
                print("Max Connections Reached")
                print(f"Listening on {self.ip}:{self.port}")
                client_socket, client_address = self.socket.accept()
                print(f"Accepted connection from {client_address[0]}:{client_address[1]}. Will close soon.")
                t.Thread(None, self.Coms, f"{client_address[0]}:{client_address[1]}", (client_socket, client_address, True)).start()
                self.numconnect+=1
    def Coms(self, client_socket, client_address, close):
        error = False
        if not close:
            try:
                while True:
                    request = client_socket.recv(1024)
                    request = request.decode("utf-8")
                    if request.lower() == "close" or close:
                        break
                    self.messages.append([f"{client_address[0]}:{client_address[1]}", request])
                    print(f"Received: {request} from {client_address[0]}:{client_address[1]}.")
                    response = "accepted".encode("utf-8")
                    client_socket.send(response)
            except:
                print(f"An error occured with client {client_address[0]}:{client_address[1]}")
                error = True
        if not error:
            client_socket.send("closed".encode("utf-8"))
        self.numconnect-=1
        client_socket.close()
        print(f"Connection to {client_address[0]}:{client_address[1]} closed")
        exit
    def close(self):
        self.socket.sendall("closed".encode("utf-8"))
        self.socket.close()
newsocket = server(8888)
newsocket.startListening(2)