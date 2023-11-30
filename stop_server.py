import signal
import os

def stop_server():
    with open('server_pid.txt', 'r') as file:
        pid = int(file.read().strip())

    try:
        os.kill(pid, signal.SIGTERM)  # Envía la señal SIGTERM al proceso del servidor
        print("Server stopped successfully.")
    except ProcessLookupError:
        print("Server process not found.")

if __name__ == "__main__":
    stop_server()
