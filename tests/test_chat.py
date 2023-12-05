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
        with open('server_pid.txt', 'r') as file:
            content = file.read().strip()
            if content:
                return int(content)
            else:
                # Handle the case when the file is empty
                return None  # or raise an appropriate exception

    def is_server_ready(self):
        try:
            with open('server_log.txt', 'r') as file:
                log_content = file.read()
                return "[*] Server listening on 0.0.0.0:12345" in log_content
        except FileNotFoundError:
            return False

    def wait_for_server(self):
        timeout = 10  # segundos
        start_time = time.time()

        while not self.is_server_ready():
            if time.time() - start_time > timeout:
                raise TimeoutError("Timed out waiting for server to start.")
            time.sleep(1)

    def test_client_server_interaction(self):
        if self.server_pid:
            # Server is running, don't start it again
            return

        # Start the server
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

        # Wait for the server to start
        self.wait_for_server()

        # Your test code here

    def run_server(self):
        # Your server code here
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 12345))
        server.listen(5)
        print("[*] Server listening on 0.0.0.0:12345")

        # Guarda el log del servidor en 'server_log.txt'
        with open('server_log.txt', 'w') as log_file:
            log_file.write("[*] Server listening on 0.0.0.0:12345\n")

            while True:
                client, addr = server.accept()
                print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
                client_handler = threading.Thread(target=self.handle_client, args=(client,))
                client_handler.start()

    def handle_client(self, client_socket):
        # Your client handling code here
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            client_socket.send(data)
        client_socket.close()


if __name__ == "__main__":
    unittest.main()
