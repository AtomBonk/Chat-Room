from socket import socket, AF_INET, SOCK_STREAM
import logging
from threading import Thread
import sys

class ChatClient:
    def __init__(self, host, port) -> None:
        self.logger = self._setup_logger()
        self.socket = self._setup_socket(host, port)

        # starts a thread to wait for user input.
        thread = Thread(target=self.send_messages)
        thread.daemon = True
        thread.start()

        # recv is a blocking call.
        # receives data from server.
        # upon server termination client shuts down.
        try:
            while True:
                data = self.socket.recv(4096)
                self.logger.info(data.decode(errors='replace'))
        except ConnectionResetError:
            self.logger.warning('Server terminated. Exiting.')
            sys.exit()

    def send_messages(self):
        # tries to receive input from client user.
        # upon termination closes the socket and shuts down the client.
        try:
            while True:
                user_message = input()
                self.socket.send(user_message.encode('utf-8', errors='replace'))
        except (KeyboardInterrupt, EOFError):
            self.socket.close()
            sys.exit()
        


    def _setup_socket(self, host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            self.logger.warning('No server available. Shutting down.')
            sys.exit()
        return sock


    def _setup_logger(self):
        logger = logging.getLogger('chat_client')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger


if __name__ == "__main__":
    client = ChatClient('127.0.0.1', 4333)
    