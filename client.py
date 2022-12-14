import socket
import select
import threading
import os
from getpass import getpass


class Client:

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8080
        self.go = False

    def write(self, s, stop):
        while True:
            if self.go:
                message = input()
                s.sendall(message.encode())
                self.go = False

            if stop():
                break

    def run(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            stop_threads = False

            threading.Thread(target=Client.write, args=(self, s, lambda: stop_threads,)).start()

            while True:

                ready = select.select([s], [], [], 1)
                self.go = False

                if ready[0]:
                    message = s.recv(2048).decode()

                    print_message = message.split("\n")

                    for i in print_message:
                        print(i)

                    if message == '\033[H\033[J':
                        if os.name == "posix":
                            os.system("clear")
                        else:
                            os.system("cls")

                        self.go = True

                    elif message == 'password: ' or message == 'Enter a new password: ':
                        password = getpass('')
                        s.sendall(password.encode())

                    else:
                        self.go = True


if __name__ == "__main__":
    c = Client()
    c.run()
