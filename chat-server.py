import socket
import select
import sys

from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


if len(sys.argv) != 3:
    print("\nIncorrect usage! You need to call the script like this:")
    print("SCRIPT_NAME.py IP_ADDRESS PORT_NUM")
    exit()
