import unittest
import threading
import socket
import time

class TestChatServer(unittest.TestCase):
    def setUp(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()
        time.sleep(1)  # Espera un segundo para asegurarse de que el servidor esté en funcionamiento

    def tearDown(self):
        self.server_thread.join(timeout=1)  # Espera a que el servidor termine
        self.server_thread = None

    def run_server(self):
        # Tu código del servidor
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
        # Tu código de manejo del cliente
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            client_socket.send(data)
        client_socket.close()

    def test_client_server_interaction(self):
        # Prueba la interacción básica entre el cliente y el servidor
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 12345))

        message = "Hello, server!"
        client.send(message.encode('utf-8'))
        data = client.recv(1024)

        self.assertEqual(data.decode('utf-8'), message)

        client.close()

if __name__ == "__main__":
    unittest.main()
