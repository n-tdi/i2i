import socket as skt
import threading as t
import BetterGlob as bg
import pygame
import pickle
import zlib
import brotli

DIRECTORY = bg.getdirectb("thing.txt")
print(DIRECTORY)
'''
set start_x or cam_detected to 1 in raspi boot/firmware/config.txt
'''
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
        self.datacomp = 0
        self.betterdataing = False
    def startListening(self, numclients: int):
        self.numconnect = 0
        self.listenThread = t.Thread(None, self.runServer, "Listening Thread", (numclients, )).start()
        self.data_get_better()
    def data_get_better(self):
        if not self.betterdataing:
            self.betterdataing = True
            self.data = None
            self.datacomp = 0
            for x in range(1, 12):
                t.Thread(None, self.get_bettter_data, "hehehehe"+str(x), (x, )).start()
    def get_bettter_data(self, datacomp):
        x = []
        for y in bg.glob.glob(DIRECTORY+"*".replace("\\", "/")):
            if not y.replace(".jpg", "") == y:
                pimg = pygame.image.load(y)
                img = open(y, "rb")
                print("a")
                img = img.read()
                print("b")
                x.append([y.replace(".jpg", ""), zlib.compress(img)])#pygame.image.tobytes(img, 'RGB'), [img.get_width(), img.get_height()]])
                #x.append(brotli.compress(pickle.dumps([y.replace(".jpg", "").replace(DIRECTORY.replace("\\", "/"), ""), pygame.image.tobytes(img, 'RGB'), [img.get_width(), img.get_height()]]), brotli.MODE_GENERIC, 5))
        pickled_data = brotli.compress(pickle.dumps(x), brotli.MODE_GENERIC, datacomp)
        if self.datacomp<=datacomp:
            self.datacomp = datacomp
            self.data = pickled_data
            if self.datacomp == 11:
                self.betterdataing = False
        exit
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
                    if request.lower() == "getimages":
                        print("sending images")
                        if len(bg.glob.glob(DIRECTORY+"*".replace("\\", "/"))) >0:
                            answer = "got packet"
                            print("c")
                            while not answer == "got packet":
                                answer = client_socket.recv(1024).decode("utf-8")
                            client_socket.send("sending packet".encode("utf-8"))
                            print("D")
                            answer = client_socket.recv(1024).decode("utf-8")
                            while not answer == "ready":
                                answer = client_socket.recv(1024).decode("utf-8")
                            if answer == "ready":
                                pickled_data = self.data
                                print("b")
                                client_socket.send(str(len(pickled_data)).encode("utf-8"))
                                while not answer == "lengot":
                                    answer = client_socket.recv(1024).decode("utf-8")
                                client_socket.sendall(pickled_data)
                                print("sent data")
                                #client_socket.send("endpacket".encode("utf-8"))
                            while not answer == "got packet":
                                answer = client_socket.recv(1024).decode("utf-8")
                        client_socket.send("done".encode("utf-8"))
                    else:
                        self.messages.append([f"{client_address[0]}:{client_address[1]}", request])
                        print(f"Received: {request} from {client_address[0]}:{client_address[1]}.")
                        response = "accepted".encode("utf-8")
                        client_socket.send(response)
            except Exception as e:
                print(f"An error occured with client {client_address[0]}:{client_address[1]}")
                print(e)
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
print(bg.glob.glob(DIRECTORY+"*".replace("\\", "/")))