import unittest
import threading
import socket
import time
import os
import signal

class TestChatServer(unittest.TestCase):
    def setUp(self):
        self.server_pid = self.get_server_pid()

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

    def test_client_server_interaction(self):
        if self.server_pid:
            # Server is running, don't start it again
            return

        # Start the server
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()
        time.sleep(1)  # Wait for the server to start

        # Your test code here

    def run_server(self):
        # Your server code here
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 12345))
        server.listen(5)
        print("[*] Server listening on 0.0.0.0:12345")

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
