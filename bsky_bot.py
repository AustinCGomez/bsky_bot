"""This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>"""

import os
import socket
from atproto import Client

client = Client()

# Try to load existing session first
try:
    with open('session.txt', 'r') as f:
        session_string = f.read()
    client.login(session_string=session_string)
    print("Logged in with saved session")
except (FileNotFoundError, Exception) as e:
    # No session file or invalid session, do fresh login
    print("Logging in fresh...")
    client.login(
        os.environ["BLUESKY_USERNAME"],
        os.environ["BLUESKY_PASSWORD"])

    # Save the session
    session_string = client.export_session_string()
    with open('session.txt', 'w') as f:
        f.write(session_string)
    print("Session saved")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8089))
server_socket.listen(5)

while True:
    connect, address = server_socket.accept()
    data = connect.recv(1024)
    message = data.decode()

    client.send_post(text=message)
    connect.close()
 #   main()
