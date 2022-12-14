from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import logging
from threading import Thread
import sys
import datetime
import psycopg2
import keys

class ChatServer:
    def __init__(self, host, port) -> None:
        self.logger = self._setup_logger()
        self.socket = self._setup_socket(host, port)
        self.connections = []
        self.connect_postgres()

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
                # blocking call, waits to receive messages
                # breaks if client terminated for any reason 
                # otherwise relays message to all connected clients
                # store message into postgres DB
                data = conn.recv(4096)
                self.insert_postgres(data)

                for connection in self.connections:
                    addr_prefix = ("<" + addr[0] + ":" + str(addr[1]) + ">").encode('utf-8')
                    now_prefix = (" <" + datetime.datetime.now().strftime("%D %T") + "> ").encode('utf-8')
                    connection.send(addr_prefix + now_prefix + data)  
        except(ConnectionResetError, BrokenPipeError):
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


    def insert_postgres(self, data):
        #establishing the connection
        conn = psycopg2.connect(
        database=keys.pgDB, 
        user=keys.pgUser, 
        password=keys.pgPassword, 
        host=keys.pgHost, 
        port= keys.pgPort
        )

        conn.autocommit = True
        cursor = conn.cursor()

        message = data.decode()
        cursor.execute("INSERT INTO Messages VALUES (%s);", (message,))
        self.logger.info('MESSAGE ADDED TO DB' + message)

    def connect_postgres(self):

        #establishing the connection
        conn = psycopg2.connect(
        database=keys.pgDB, 
        user=keys.pgUser, 
        password=keys.pgPassword, 
        host=keys.pgHost, 
        port=keys.pgPort
        )

        conn.autocommit = True
        cursor = conn.cursor()

        self.logger.info("Connected successfully.")

        # Creating table if it doesn't already exist.
        cursor.execute("CREATE TABLE IF NOT EXISTS Messages (Message VARCHAR(255))")


if __name__ == "__main__":
    server = ChatServer('0.0.0.0', 4333)
    server.run()
    