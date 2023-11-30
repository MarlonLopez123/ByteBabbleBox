import unittest
import threading
import socket
import time
import os
import signal

class TestChatServer(unittest.TestCase):
    def setUp(self):
        self.server_pid = self.get_server_pid()

        # Espera hasta que el servidor esté listo (hasta que se imprima el mensaje [*] Server listening...)
        while not self.is_server_ready():
            time.sleep(1)

    def tearDown(self):
        if self.server_pid:
            os.kill(self.server_pid, signal.SIGTERM)
            time.sleep(1)

    def get_server_pid(self):
        try:
            with open('server_pid.txt', 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return None

    def is_server_ready(self):
        with open('server_log.txt', 'r') as file:
            log_content = file.read()
            return "[*] Server listening on 0.0.0.0:12345" in log_content

    def test_client_server_interaction(self):
        # Tu código de prueba aquí
        # Puedes usar el código que ya tenías aquí
        pass

    def run_server(self):
        # Tu código del servidor aquí
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 12345))
        server.listen(5)
        print("[*] Server listening on 0.0.0.0:12345")

        # Guarda el log del servidor en 'server_log.txt'
        with open('server_log.txt', 'w') as log_file:
            while True:
                client, addr = server.accept()
                print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
                client_handler = threading.Thread(target=self.handle_client, args=(client,))
                client_handler.start()

    def handle_client(self, client_socket):
        # Tu código de manejo del cliente aquí
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            client_socket.send(data)
        client_socket.close()


if __name__ == "__main__":
    unittest.main()
