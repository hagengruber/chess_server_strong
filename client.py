"""
    Module that provides a connection to the ChessServer
"""
from socket import gethostbyname
from socket import gethostname
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from select import select
from threading import Thread
from sys import exit as sys_exit
from os import name
from os import system
from getpass import getpass
from ssl import create_default_context
from ssl import Purpose


class Client:

    """Class that provides a connection to the ChessServer"""

    def __init__(self):
        self.host = gethostbyname(gethostname())
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

            context = create_default_context(Purpose.SERVER_AUTH, cafile=self.server_cert)
            context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)

            with socket(AF_INET, SOCK_STREAM) as server_socket:

                self.conn = context.wrap_socket(server_socket, server_side=False,
                                                server_hostname='Chess')

                try:
                    self.conn.connect((self.host, self.port))
                except ConnectionRefusedError:
                    print("Server refused connection. Please check the Server status")
                    sys_exit()

                stop_threads = False

                Thread(target=Client.write, args=(self, lambda: stop_threads,)).start()

                while True:

                    ready = select([self.conn], [], [], 1)
                    self.allowed_to_write = False

                    if ready[0]:
                        message = self.conn.recv(4096).decode()

                        print_message = message.split("\n")

                        for i in print_message:
                            print(i)

                        if message == '\033[H\033[J':
                            if name == "posix":
                                system("clear")
                            else:
                                system("cls")

                            self.allowed_to_write = True

                        elif 'password' in message.lower():
                            password = getpass('')
                            self.conn.sendall(password.encode())

                        elif message == 'Thanks for playing':
                            stop_threads = True
                            sys_exit()

                        else:
                            self.allowed_to_write = True

        except ConnectionResetError:
            print("Connection to Server lost")
            stop_threads = True
            sys_exit()


if __name__ == "__main__":
    c = Client()
    c.run()
