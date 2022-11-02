from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import logging

class ChatServer:
    def __init__(self, host, port) -> None:
        self.logger = self._setup_logger()
        self.socket = self._setup_socket(host, port)


    def run(self):
        self.logger.info('Chat server is running')

        while True:
            # accept will wait for incoming connections
            # returns a tuple containing a new socket object
            # with the connection and address of the client on the other end
            conn, addr = self.socket.accept()
            self.logger.debug(f'New connection: {addr}')


    def _setup_socket(self, host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()
        return sock


    def _setup_logger(self):
        logger = logging.getLogger('chat_server')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger

if __name__ == "__main__":
    server = ChatServer('127.0.0.1', 4333)
    server.run()
    