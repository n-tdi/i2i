import socket
def run_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = socket.gethostname()+".local"
    port = port
    server_ip = "0.0.0.0"
    server.bind((server_ip, port))
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8") # convert bytes to string
        
        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if request.lower() == "close":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("closed".encode("utf-8"))
            break

        print(f"Received: {request}")

        response = "accepted".encode("utf-8") # convert string to bytes
        # convert and send accept response to the client
        client_socket.send(response)

    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()

def run_multiserver(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = ip
    port = port
    server.bind((server_ip, port))
    print(f"Listening on {server_ip}:{port}")
    server.listen(5)
    Connects = 10
    while Connects>0:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        request = client_socket.recv(1024)
        request = request.decode("utf-8") # convert bytes to string
        print(f"Received: {request}")
        response = "accepted".encode("utf-8") # convert string to bytes
        # convert and send accept response to the client
        client_socket.send(response)
        client_socket.close()
        #print("Connection to client closed")

    server.close()
run_server("127.0.0.1", 8888)