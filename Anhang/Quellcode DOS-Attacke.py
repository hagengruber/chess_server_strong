import socket
import time
import multiprocessing as m
import psutil
import select


class DDOS:

    def __init__(self):
        self.spieler = ""
        self.zeit = "Zeit bis KI ersten Zug macht"
        self.cpu = "CPU Auslastung"

    def send(self, s, message):
        time.sleep(0.5)
        s.sendall(message)

    def move(self, s, p_move):
        p_move = p_move + '\r\n'
        self.send(s, p_move.encode())

        while True:

            try:
                ready = select.select([s], [], [], 1)

                if ready[0]:
                    mess = s.recv(4096)
                else:
                    continue

                mess = mess.decode()
            except UnicodeDecodeError:
                continue

            if 'desired' in mess:
                break

    def client(self, host, port, thread):

        print("Start Thread " + str(thread))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.recv(1024)

            self.send(s, b"1\r\n")
            s.recv(1024)
            self.send(s, b"florian.hagengruber@stud.th-deg.de\r\n")
            s.recv(1024)
            self.send(s, b"aPassword\r\n")
            s.recv(1024)

            while True:

                self.send(s, b"2\r\n")
                s.recv(1024)
                self.send(s, b"Y\r\n")
                while True:

                    try:
                        ready = select.select([s], [], [], 1)

                        if ready[0]:
                            mess = s.recv(4096)
                        else:
                            continue

                        mess = mess.decode()
                    except UnicodeDecodeError:
                        continue

                    if 'desired' in mess:
                        break
                self.move(s, "g1e1")
                self.move(s, "h1f1")
                self.move(s, "g5f5")
                self.move(s, "h4f6")
                self.move(s, "f6d6")
                self.move(s, "h6d2")

                self.send(s, b"--save\r\n")
                s.recv(1024)
                
                print("Thread: " + str(thread) + " - No Problem")

    def av_time(self, host, port):

        av_time = []

        for _ in range(5):
            start = time.time()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.recv(1024)

                self.send(s, b"1\r\n")
                s.recv(1024)
                self.send(s, b"florian.hagengruber@stud.th-deg.de\r\n")
                s.recv(1024)
                self.send(s, b"aPassword\r\n")
                s.recv(1024)
                self.send(s, b"2\r\n")
                s.recv(1024)
                self.send(s, b"Y\r\n")

                while True:

                    try:
                        ready = select.select([s], [], [], 1)

                        if ready[0]:
                            mess = s.recv(4096)
                        else:
                            continue

                        mess = mess.decode()
                    except UnicodeDecodeError:
                        continue

                    if 'desired' in mess:

                        break

                self.move(s, "g1e1")

            av_time.append(time.time() - start)

        sum = 0
        for i in av_time:
            sum += i

        return sum / len(av_time)

    def av_cpu(self):

        sum = 0
        for _ in range(5):
            sum += psutil.cpu_percent()
            time.sleep(0.3)

        return sum / 5

    def create_statistic(self, num_of_clients, host, port):
        
        print("Create statistics for " + str(num_of_clients) + " Clients")
        
        self.spieler += ";" + str(num_of_clients) + " Spieler"
        self.zeit += ";" + str(self.av_time(host, port))
        self.cpu += ";" + str(self.av_cpu())

        f = open("statistic.csv", "w")
        f.write(self.spieler + '\n')
        f.write(self.zeit + '\n')
        f.write(self.cpu + '\n')
        f.close()

    def run(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 8080
        clients = []
        sprungweite = 20
        start = 50
        stats = sprungweite

        while True:
            clients.append(m.Process(target=DDOS.client, args=(self, host, port, len(clients) + 1,)))
            clients[-1].start()

            if len(clients) >= start:

                stats += 1
                if stats >= sprungweite:
                    print("Jump to statistics")
                    self.create_statistic(len(clients), host, port)
                    stats = 0


if __name__ == "__main__":
    d = DDOS()
    d.run()
