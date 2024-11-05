import socket

def run_client(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = ip
    server_port = port
    client.connect((server_ip, server_port))
    while True:
        # input message and send it to the server
        msg = input("Enter message: ")
        client.send(msg.encode("utf-8")[:1024])
        # receive message from the server
        response = client.recv(1024)
        response = response.decode("utf-8")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "closed":
            break

        print(f"Received: {response}")
    client.close()
    print("Connection to server closed")

def run_multiclient(ip, port):
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = ip
        server_port = port
        client.connect((server_ip, server_port))
        msg = input("Enter message: ")
        client.send(msg.encode("utf-8")[:1024])
        response = client.recv(1024)
        response = response.decode("utf-8")
        if msg.lower() == "close":
            break
        print(f"Received: {response}")
        client.close()
    client.close()
    print("Connection to server closed")


run_client("i2i.local", 8888)