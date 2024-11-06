import socket as skt
import threading as t
class server:
    def __init__(self, port: int) -> None:
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        ip = skt.gethostname()+".local"
        server.bind((ip, port))
        print(f"Server created with ip {ip}, and port {port}")
        self.clients = []
        self.messages = []
    def startListening(self, numclients: int):
        pass
