import socket
import sys

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))
message = sys.stdin.read()
clientsocket.send(message.encode())
print("Success!")
