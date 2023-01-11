"""
    Module for managing security
"""

import json
import re
import ssl
from argon2 import PasswordHasher
import argon2.exceptions


class Password:
    """Class that handles password checks"""

    def __init__(self):
        self.upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                      'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.specials = ['!', '?', '§', '$', '%', '&', '#', '@']
        self.allowed_mail_chars = self.upper + self.lower + self.numbers + ['@', '-', '.']
        self.forbidden = ['"', "--", "'", ";"]
        self.length = {'min': 10, 'max': 20}

    def check_password(self, password):
        """Checks the password pattern"""
        password = str(password)
        upper = 0
        lower = 0
        nums = 0
        special = 0

        for character in password:
            if character in self.upper:
                upper += 1

            if character in self.lower:
                lower += 1

            if character in self.numbers:
                nums += 1

            if character in self.specials:
                special += 1

            if character in self.forbidden:
                return False

        return self.check_password_guideline({'upper': upper, 'lower': lower,
                                              'nums': nums, 'special': special}, password)

    def check_password_guideline(self, characters, password):
        """returns bool whether the password complies with the policy"""
        if characters['upper'] >= 2 and characters['lower'] >= 2 \
                and characters['nums'] >= 2 and characters['special'] >= 2:
            return self.length['min'] <= len(password) <= self.length['max']

        return False


class ArgonHash:
    """Handles everything with Hashes"""

    def __init__(self):
        self.argon = PasswordHasher(time_cost=16, memory_cost=2 ** 15,
                                    parallelism=2, hash_len=32, salt_len=16)

    def hash(self, user_input):
        """Returns the hash from the user input"""
        # user input cast to string, because the activation code needs to be hashed to
        return self.argon.hash(str(user_input))

    def verify(self, user_hash, user_input):
        """Returns bool if the user input is equal from the Hash in database"""
        try:
            return self.argon.verify(user_hash, user_input)
        except argon2.exceptions.VerifyMismatchError:
            return False


class InputValidation:
    """Handles everything with Input Validation"""

    def __init__(self):
        self.min_len = 13

    def check_input_length(self, user_input):
        """returns bool if the length is ok"""
        return len(user_input) < self.min_len

    @staticmethod
    def check_input(user_input):
        """check if the user input is y or n"""
        user_input = user_input.upper()

        if re.match('^Y', user_input) or re.match('YES', user_input):
            return 1

        if re.match('^N', user_input) or re.match('NO', user_input):
            return 0

        return 2

    @staticmethod
    def check_json(json_string):
        """check if the json string is valid"""
        try:
            json_string = json_string.replace('False', 'false').replace(
                'True', 'true').replace('None', 'null')
            return json.loads(json_string)
        except json.decoder.JSONDecodeError:
            return False


class Communication:
    """handles everything with communication"""

    def __init__(self, socket, connect, view):
        self.socket = socket
        self.connect = connect
        self.view = view

    def run(self):
        """creates a connection to the Client"""

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(certfile='./certs/server.crt', keyfile='./certs/server.key')
        context.load_verify_locations(cafile='./certs/client.crt')

        new_socket, addr = self.socket.accept()
        conn = context.wrap_socket(new_socket, server_side=True)

        with conn:
            self.connect_and_run(addr, conn)

    def connect_and_run(self, addr, conn):
        """run the control-loop"""
        self.connect.put(True)
        print("Server is connected with port " + str(addr))
        welcome = "Hello. You are connected to the Chess Server. Your port is " \
                  + str(addr[1]) + '\n\n'
        conn.sendall(welcome.encode())

        self.view.init_socket(conn)

        self.view.print_menu(False)
