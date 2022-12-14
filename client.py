import socket
import select


class client:

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8080

    def run(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            # s.setblocking(0)

            while True:

                ready = select.select([s], [], [], 1)

                if ready[0]:
                    flag = s.recv(1024).decode()
                    message = s.recv(1024).decode()

                    print("Flag: " + str(flag))
                    print("Message: " + str(message))

                    message = message.split("\n")

                    if flag == "r":
                        print("Read")
                    elif flag == "p":
                        print("print")

                    for i in message:
                        print(i)

if __name__ == "__main__":
    c = client()
    c.run()