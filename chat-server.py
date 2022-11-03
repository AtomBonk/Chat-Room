from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_RD
import logging
from threading import Thread
import sys

class ChatServer:
    def __init__(self, host, port) -> None:
        self.logger = self._setup_logger()
        self.socket = self._setup_socket(host, port)
        self.connections = []

    def run(self):
        self.logger.info('Chat server is running')

        while True:
                # accept will block and wait for incoming connections
                # returns a tuple containing a new socket object
                # with the connection and address of the client 
                # on the other end
            try:
                conn, addr = self.socket.accept()
                self.logger.debug(f'New connection: {addr}')
                self.connections.append(conn)
                self.logger.debug(f'Connections: {self.connections}')

                # upon succefully accepting a connection
                # create a new thread to relay any message from this
                # client to the other clients connected to the server
                thread = Thread(target=self.relay_messages, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except KeyboardInterrupt:
                self.logger.warning('Keyboard interrupt. Server shutting down.')
                sys.exit()

    def relay_messages(self, conn, addr):
        try:
            while True:
                # blocking call, wait to receive messages
                # breaks if client terminated for any reason 
                # otherwise relays message to all other clients
                data = conn.recv(4096)
                for connection in self.connections:
                    connection.send(data)
        except ConnectionResetError:
            self.logger.warning('Socket terminated. Removing session.')
            self.connections.remove(conn)
            sys.exit()
            

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
    