from socket import socket, AF_INET, SOCK_STREAM
import logging
from threading import Thread

class ChatClient:
    def __init__(self, host, port) -> None:
        self.logger = self._setup_logger()
        self.socket = self._setup_socket(host, port)

        thread = Thread(target=self.send_messages)
        thread.daemon = True
        thread.start()

        while True:
            data = self.socket.recv(4096)
            if not data:
                break
            self.logger.info(data.decode())

    def send_messages(self):
        while True:
            user_message = input()
            self.socket.send(user_message.encode('utf-8', errors='backslashreplace'))


    def _setup_socket(self, host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        return sock


    def _setup_logger(self):
        logger = logging.getLogger('chat_client')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger


if __name__ == "__main__":
    client = ChatClient('127.0.0.1', 4333)
    