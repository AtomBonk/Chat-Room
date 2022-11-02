import socket
import select
import sys

from _thread import *

def clientthread(conn, addr, list_of_clients):
 
    # sends a message to the client whose user object is conn
    conn.send(("Welcome to this chatroom!").encode())
 
    while True:
            try:
                message = conn.recv(2048)
                if message:
                    message_to_send = "<" + addr[0] + "> " + message
                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    print (message_to_send)
                    # Calls broadcast function to send message to all
                    broadcast(message_to_send, conn, list_of_clients)
 
                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn, list_of_clients)
 
            except:
                continue
 
"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection, list_of_clients):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
 
                # if the link is broken, we remove the client from our list
                list_of_clients = remove(clients, list_of_clients)
 
"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection, list_of_clients):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
    return list_of_clients

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_add = "127.0.0.1"
    server_port = 4333

    server.bind((server_add, server_port))

    # listen for 12 active connections
    server.listen(12)
    
    list_of_clients = []
 

    while True:
        print("chat room is running..")
        """Accepts a connection request and stores two parameters,
        conn which is a socket object for that user, and addr
        which contains the IP address of the client that just
        connected"""
        conn, addr = server.accept()
    
        """Maintains a list of clients for ease of broadcasting
        a message to all available people in the chatroom"""
        list_of_clients.append(conn)
    
        # prints the address of the user that just connected
        print (addr[0] + " connected")
    
        # creates an individual thread for every user
        # that connects
        start_new_thread(clientthread,(conn, addr, list_of_clients))    
    

if __name__ == "__main__":
    main()