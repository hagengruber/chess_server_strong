import socket
import select
import threading
import os
from getpass import getpass
import ssl


class Client:

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8080
        self.go = False
        self.server_sni_hostname = 'Chess'
        self.server_cert = './certs/server.crt'
        self.client_cert = './certs/client.crt'
        self.client_key = './certs/client.key'
        self.conn = None

    def write(self, stop):

        while True:
            if self.go:
                message = input()
                try:
                    self.conn.sendall(message.encode())
                except OSError:
                    return
                except EOFError:
                    return

                self.go = False

            if stop():
                break

    def run(self):

        try:

            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.server_cert)
            context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                self.conn = context.wrap_socket(s, server_side=False, server_hostname=self.server_sni_hostname)
                self.conn.connect((self.host, self.port))

                stop_threads = False

                threading.Thread(target=Client.write, args=(self, lambda: stop_threads,)).start()

                while True:

                    ready = select.select([self.conn], [], [], 1)
                    self.go = False

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

                            self.go = True

                        elif 'password' in message.lower():
                            password = getpass('')
                            self.conn.sendall(password.encode())

                        elif message == 'Thanks for playing':
                            stop_threads = True
                            exit()

                        else:
                            self.go = True

        except ConnectionResetError:
            print("Connection to Server lost")
            stop_threads = True
            exit()


if __name__ == "__main__":
    c = Client()
    c.run()
