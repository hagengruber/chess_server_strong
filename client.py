"""
    Module that provides a connection to the ChessServer
"""
import socket
import select
import threading
import sys
import os
from getpass import getpass
import ssl


class Client:

    """Class that provides a connection to the ChessServer"""

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8080
        self.allowed_to_write = False
        self.server_cert = './certs/server.crt'
        self.client_cert = './certs/client.crt'
        self.client_key = './certs/client.key'
        self.conn = None

    def write(self, stop):
        """Sends the user input to the Server"""

        while True:
            if self.allowed_to_write:
                message = input()
                try:
                    self.conn.sendall(message.encode())
                except OSError:
                    return
                except EOFError:
                    return

                self.allowed_to_write = False

            if stop():
                break

    def run(self):
        """main function"""

        try:

            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.server_cert)
            context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

                self.conn = context.wrap_socket(server_socket, server_side=False,
                                                server_hostname='Chess')

                try:
                    self.conn.connect((self.host, self.port))
                except ConnectionRefusedError:
                    print("Server refused connection. Please check the Server status")
                    sys.exit()

                stop_threads = False

                threading.Thread(target=Client.write, args=(self, lambda: stop_threads,)).start()

                while True:

                    ready = select.select([self.conn], [], [], 1)
                    self.allowed_to_write = False

                    if ready[0]:
                        message = self.conn.recv(4096).decode()

                        print_message = message.split("\n")

                        for i in print_message:
                            print(i)

                        if message == '\033[H\033[J':
                            if os.name == "posix":
                                os.system("clear")
                            else:
                                os.system("cls")

                            self.allowed_to_write = True

                        elif 'password' in message.lower():
                            password = getpass('')
                            self.conn.sendall(password.encode())

                        elif message == 'Thanks for playing':
                            stop_threads = True
                            sys.exit()

                        else:
                            self.allowed_to_write = True

        except ConnectionResetError:
            print("Connection to Server lost")
            stop_threads = True
            sys.exit()


if __name__ == "__main__":
    c = Client()
    c.run()
