import socket
import threading as t
import pygame
import pickle
import time
import zlib
import brotli
import io
class client:
    def __init__(self, ip, port):
        self.connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.connector.connect((self.ip, self.port))
        self.msg = ""
        self.messages = []
        self.a = 1
        self.closed = False
        self.b = 1
        
    def runself(self):
        t.Thread(None, self.senddata, "cthreadSend", ()).start()
        t.Thread(None, self.recvdata, "cthreadRecv", ()).start()
    def senddata(self):
        while True:
            if type(self.connector) == socket.socket:
                if not self.msg == "":
                    self.connector.send(self.msg.encode("utf-8")[:1024])
                    self.msg = ""
            else:
                exit
    def recvdata(self):
        while True:
            response = self.connector.recv(1024)
            print(response)
            response = response.decode("utf-8")
            if response == "closed":
                break
            elif response == "sending packet":
                self.connector.send("ready".encode("utf-8"))
                data = b''
                A = True
                l = int(self.connector.recv(4096).decode("utf-8"))
                self.a = l
                self.connector.send("lengot".encode("utf-8"))
                while A:
                    t =time.time()
                    if self.closed:
                        exit
                    packet = self.connector.recv(4096)
                    print(time.time()-t)
                    data += packet
                    self.b = len(data)
                    #print(len(data))
                    if len(data)>=l:
                        try:
                            print("tried")
                            self.messages.append(pickle.loads(brotli.decompress(data)))
                            A = False
                        except Exception as e:
                            print(e)
                    #print("A")
                #self.messages.append(pickle.loads(data))
                print("did it")
                self.connector.send("got packet".encode("utf-8"))
                #print(self.messages)
            else:
                self.messages.append(response)
        self.connector.close()
        print("Connection to server closed")
        exit
    def closeself(self):
        self.connector.send("close".encode("utf-8")[:1024])   

class display:
    def __init__(self, ip, port):
        self.sock = client(ip, port)
        self.sock.runself()
        self.images = []
        pygame.init()
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.scroll = 0
        self.font = pygame.font.SysFont("MS Gothic", 20)
        self.sock.closed = True
        self.getimages()
    def update(self):
        mouse = pygame.mouse.get_pos()
        mouseclick = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        self.win.fill((0, 0, 0))
        ypos = -self.scroll+10
        for x in self.images:
            txtn = self.font.render(x[0], True, (0, 255, 0))
            self.win.blit(txtn, (10, ypos))
            ypos+=25
            img = x[1]
            if type(img) == pygame.Surface:
                self.win.blit(img, (10, ypos))
                ypos+=img.get_height()+20
        if keys[pygame.K_DOWN]:
            if self.scroll<(ypos+(self.scroll-10)-self.win.get_height()):
                self.scroll+=5
        if keys[pygame.K_UP]:
            if self.scroll>0:
                self.scroll-=5
        if keys[pygame.K_p]:
            self.sock.closeself()
            self.sock.closed = True
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sock.closeself()
                self.sock.closed = True
                return False
        if keys[pygame.K_r]:
            self.scroll = 0
            if not self.getimages():
                self.sock.closed = True
                return False
        pygame.display.update()
        return True


    def getimages(self):
        #self.images = [["frame", pygame.image.load("frame.jpg")], ["frame2", pygame.image.load("frame.jpg")], ["frame3", pygame.image.load("frame.jpg")]]
        self.sock.msg = "getimages"
        while not "done" in self.sock.messages:
            self.win.fill((0, 0, 0))
            txt = self.font.render("Reloading...", True, (0, 255, 0))
            #print(self.sock.messages)
            self.win.blit(txt, ((self.win.get_width()/2)-(txt.get_width()/2), (self.win.get_height()/2)-(txt.get_height()/2)))
            q = round(self.sock.b*100/self.sock.a, 2)
            txt = self.font.render(f"{q}% done", True, (0, 255, 0))
            self.win.blit(txt, ((self.win.get_width()/2)-(txt.get_width()/2), (self.win.get_height()/2)-(txt.get_height()/2)-50))
            txt = self.font.render(f"{self.sock.b}/{self.sock.a} bytes collected", True, (0, 255, 0))
            self.win.blit(txt, ((self.win.get_width()/2)-(txt.get_width()/2), (self.win.get_height()/2)-(txt.get_height()/2)-100))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                self.sock.closeself()
                self.sock.closed = True
                return False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sock.closeself()
                    self.sock.closed = True
                    return False
            pygame.display.update()
            #print(self.sock.messages)
        print("next")
        for x in self.sock.messages:
            if type(x) == list:
                for q in x:
                    img = pygame.image.load(io.BytesIO(zlib.decompress(q[1])))
                    self.images.append([q[0], pygame.transform.scale(img, [self.win.get_width()-20, img.get_height()*(self.win.get_width()-20)/(img.get_width())])])
                self.sock.messages.remove(x)
        self.sock.messages.remove("done")
        return True

        



mydisplay = display("0ct0lingsLaptop.local", 8888)
a = True
while a:
    a = mydisplay.update()
pygame.quit()
raise SystemExit