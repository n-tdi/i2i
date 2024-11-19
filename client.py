import socket
import threading as t
import pygame
import pickle
import time
import zlib
import brotli
import io

def key_to_char(Keys):
    string = ""
    if Keys[pygame.K_q]:
         string = string+ "q"
    if Keys[pygame.K_w]:
         string = string+ "w"
    if Keys[pygame.K_e]:
         string = string+ "e"
    if Keys[pygame.K_r]:
         string = string+ "r"
    if Keys[pygame.K_t]:
         string = string+ "t"
    if Keys[pygame.K_y]:
         string = string+ "y"
    if Keys[pygame.K_u]:
         string = string+ "u"
    if Keys[pygame.K_i]:
         string = string+ "i"
    if Keys[pygame.K_o]:
         string = string+ "o"
    if Keys[pygame.K_p]:
         string = string+ "p"
    if Keys[pygame.K_a]:
         string = string+ "a"
    if Keys[pygame.K_s]:
         string = string+ "s"
    if Keys[pygame.K_d]:
         string = string+ "d"
    if Keys[pygame.K_f]:
         string = string+ "f"
    if Keys[pygame.K_g]:
         string = string+ "g"
    if Keys[pygame.K_h]:
         string = string+ "h"
    if Keys[pygame.K_j]:
         string = string+ "j"
    if Keys[pygame.K_k]:
         string = string+ "k"
    if Keys[pygame.K_l]:
         string = string+ "l"
    if Keys[pygame.K_z]:
         string = string+ "z"
    if Keys[pygame.K_x]:
         string = string+ "x"
    if Keys[pygame.K_c]:
         string = string+ "c"
    if Keys[pygame.K_v]:
         string = string+ "v"
    if Keys[pygame.K_b]:
         string = string+ "b"
    if Keys[pygame.K_n]:
         string = string+ "n"
    if Keys[pygame.K_m]:
         string = string+ "m"
    return string
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
                        A = False
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
        self.closed = True

class display:
    def __init__(self, ip, port):
        self.sock = client(ip, port)
        self.sock.runself()
        self.images = []
        pygame.init()
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.scroll = 0
        self.font = pygame.font.SysFont("MS Gothic", 20)
        #self.sock.closed = False
        self.getimages()
    def update(self):
        mouse = pygame.mouse.get_pos()
        mouseclick = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        self.win.fill((0, 0, 0))
        ypos = -self.scroll+10
        for x in self.images:
            txtn = self.font.render(x[0], True, (0, 255, 0))
            txtrect = txtn.get_rect()
            self.win.blit(txtn, (10, ypos))
            txtrect.x = 10
            txtrect.y = ypos
            ypos+=25
            img = x[1]
            if type(img) == pygame.Surface:
                self.win.blit(img, (10, ypos))
                ypos+=img.get_height()+20
            if txtrect.collidepoint(mouse[0], mouse[1]) and mouseclick[0]:
                a = self.textedit(x[0])
                if not a == "closed!":
                    x[0] = a
                else:
                    self.sock.closeself()
                    return False
        if keys[pygame.K_DOWN]:
            if self.scroll<(ypos+(self.scroll-10)-self.win.get_height()):
                self.scroll+=5
        if keys[pygame.K_UP]:
            if self.scroll>0:
                self.scroll-=5
        if keys[pygame.K_LSHIFT]:
            self.sock.closeself()
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sock.closeself()
                return False
        if keys[pygame.K_r]:
            self.scroll = 0
            if not self.getimages():
                self.sock.closeself()
                return False
        pygame.display.update()
        return True

    def textedit(self, tax_fraud):
        text = tax_fraud
        pressbutton = False
        while True:
            self.win.fill((0, 0, 0))
            txt = self.font.render(text, True, (0, 255, 0))
            self.win.blit(txt, ((self.win.get_width()/2)-(txt.get_width()/2), (self.win.get_height()/2)-(txt.get_height()/2)))
            keys = pygame.key.get_pressed()
            intxt = key_to_char(keys)
            if not intxt == "":
                if not pressbutton:
                    text = text+intxt
                pressbutton = True
            elif keys[pygame.K_SPACE]:
                if not pressbutton:
                    return text
                pressbutton = True
            elif keys[pygame.K_BACKSPACE]:
                if not pressbutton:
                    text = text[0:len(text)-1]
                pressbutton = True
            else:
                pressbutton = False


            if keys[pygame.K_LSHIFT]:
                self.sock.closeself()
                return "closed!"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sock.closeself()
                    return "closed!"
                

            pygame.display.update()

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
                return False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sock.closeself()
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

mydisplay = display("0ct0lingsLaptop", 8888)
a = True
while a:
    a = mydisplay.update()
pygame.quit()
raise SystemExit