from argon2 import PasswordHasher
import argon2.exceptions
import json
import re
import ssl

class password:
    def __init__(self):
        self.upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                      'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.specials = ['!', '?', '§', '$', '%', '&', '#', '@']
        self.allowed_mail_chars = self.upper + self.lower + self.numbers + ['@', '-', '.']
        self.forbidden = ['"', "--", "'", ";"]
        self.min_length = 10
        self.max_length = 20

    def check_password(self, pw):
        pw = str(pw)
        u = 0
        l = 0
        n = 0
        s = 0

        for e in pw:
            if e in self.upper:
                u += 1

            if e in self.lower:
                l += 1

            if e in self.numbers:
                n += 1

            if e in self.specials:
                s += 1

            if e in self.forbidden:
                return False

        if u >= 2 and l >= 2 and n >= 2 and s >= 2:
            return self.min_length <= len(pw) <= self.max_length
        else:
            return False

class argon_hash:
    def __init__(self):
        self.argon = PasswordHasher(time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)

    def hash(self, user_input):
        encoded = str(user_input).encode()
        return self.argon.hash(encoded)

    def verify(self, user_hash, user_input):
        try:
            return self.argon.verify(user_hash, user_input)
        except argon2.exceptions.VerifyMismatchError:
            return False

class input_validation:
    def __init__(self):
        self.min_len = 13

    def check_input_length(self, user_input):
        if len(user_input) < self.min_len:
            return True
        else:
            return False

    @staticmethod
    def check_input(user_input):
        user_input = user_input.upper()

        if re.match('^Y', user_input) or re.match('YES', user_input):
            return 1

        elif re.match('^N', user_input) or re.match('NO', user_input):
            return 0

        else:
            return 2

    @staticmethod
    def check_json(json_string):
        try:
            json_string = json_string.replace('False', 'false').replace(
                'True', 'true').replace('None', 'null')
            return json.loads(json_string)
        except json.decoder.JSONDecodeError:
            return False

class communication:
    def __init__(self, socket, connect, view):
        self.socket = socket
        self.connect = connect
        self.view = view

    def run(self):
        """main function - creates a connection to the Client run loop"""

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(certfile='./certs/server.crt', keyfile='./certs/server.key')
        context.load_verify_locations(cafile='./certs/client.crt')

        new_socket, addr = self.socket.accept()
        conn = context.wrap_socket(new_socket, server_side=True)

        with conn:
            self.connect.put(True)
            print("Server is connected with port " + str(addr))
            welcome = "Hello. You are connected to the Chess Server. Your port is " \
                      + str(addr[1]) + '\n\n'
            conn.sendall(welcome.encode())

            self.view.init_socket(conn)

            self.view.print_menu(False)
