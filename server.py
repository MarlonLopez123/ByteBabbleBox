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
    
    # Guarda el PID del servidor en 'server_pid.txt'
    with open('server_pid.txt', 'w') as file:
        file.write(str(os.getpid()))
    
    # Guarda el mensaje de inicio en 'server_log.txt'
    with open('server_log.txt', 'w') as log_file:
        log_file.write("[*] Server listening on 0.0.0.0:12345\n")

    print("[*] Server listening on 0.0.0.0:12345")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    run_server()
