import socket
import select
import threading
import os


class Client:

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8080

    @staticmethod
    def write(s, stop):
        while True:
            message = input()
            s.sendall(message.encode())

            if stop():
                break

    def run(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            stop_threads = False

            threading.Thread(target=Client.write, args=(s, lambda: stop_threads,)).start()

            while True:

                ready = select.select([s], [], [], 1)

                if ready[0]:
                    message = s.recv(2048).decode()

                    if message == '\033[H\033[J':
                        if os.name == "posix":
                            os.system("clear")
                        else:
                            os.system("cls")

                    message = message.split("\n")

                    for i in message:
                        print(i)


if __name__ == "__main__":
    c = Client()
    c.run()
