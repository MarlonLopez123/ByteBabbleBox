import socket
import threading
import os

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode('utf-8')}")
        client_socket.send(data)
    client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("[*] Server listening on 0.0.0.0:12345")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    run_server()

# Guarda el PID del servidor en 'server_pid.txt'
with open('server_pid.txt', 'w') as file:
    file.write(str(os.getpid()))
